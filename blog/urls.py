from django.urls import path
from . import views
from .views import  post_share, post_comment, post_detail

app_name = 'blog'

urlpatterns = [
    # path('', views.PostView.as_view(), name='post'),
    path('',views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),

    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),

]