from django.shortcuts import render,HttpResponse
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def index(request):
    return render(request, "index.html")


def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    return render(request, "tweet_list.html", {"tweets": tweets})


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForm()
    return render(request, "tweet_form.html", {"form": form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForm(instance=tweet)
    return render(request, "tweet_form.html", {"form": form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect("tweet_list")
    return render(request, "tweet_confirm_delete.html", {"tweet": tweet})


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("pass1")
        confirm_password = request.POST.get("pass2")
        
        #Email sending
        subject = "Welcome to GauX"
        message = f"Dear {username}\nWelcome to Gaux!\nThank you for signing up and joining our community. We're thrilled to have you on board!\n\nWith GauX, you can share your thoughts, connect with others, and explore a world of ideas, all in real-time. Start tweeting and discover the power of your voice in our vibrant and growing community.\nIf you have any questions or need assistance, our support team is here to help. Feel free to reach out to us anytime.\n\nOnce again, welcome {username}! We look forward to seeing your tweets.\nBest regards,Gaurav\niamgauravsahu7@gamil.com\ngauravsahu.vercel.app"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = {email}
        send_mail(subject,message,from_email,recipient_list,fail_silently=False)
        
        
        if confirm_password != password:
            messages.warning(request, "Password mismatch")
            return redirect("/signup")
        try:
            if User.objects.get(username=username):
                messages.info(request, "User already exists")
                return redirect("/signup")
        except:
            pass
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        messages.info(request, "Please Log In")
        return redirect("/")

    return render(request, "signup.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")
        user = authenticate(username=username, password=password)
        if user != None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("/tweet")
        else:
            messages.error(request, "Login unsucessfull")
            return redirect("/")
    return render(request, "login.html")
    

def logout_page(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("/")

def search(request):
    query=request.GET['search']
    if len(query)>100:
        allPosts=Tweet.objects.none()
    else:
        allPostUser = Tweet.objects.filter(user__username__icontains=query)
        allPostText=Tweet.objects.filter(text__icontains=query)
        allPosts=allPostUser.union(allPostText)
    if allPosts.count() == 0:
        messages.warning(request, 'No search results found')
    params={'allPosts':allPosts, 'query':query}
        
    return render(request,'search.html', params)