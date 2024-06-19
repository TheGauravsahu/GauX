from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from tweet.views import signup, login_page , logout_page, search

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tweet/", include("tweet.urls")),
    path("signup/", signup, name="signup"),
    path("", login_page, name="login_page"),
    path("logout/", logout_page, name="logout_page"),
    path('search/', search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
