from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from blog import views
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
