from django.urls import path # type: ignore
from django.conf.urls.static import static # type: ignore
from social import settings
from . import views

urlpatterns = [
    path('', views.feeds, name='feeds'),
    path('create-post/', views.create_post, name='create-post'),


    path('post/<int:id>/like/', views.like_post, name='like_post'),
    path('post/<int:id>/comment/add/', views.add_comment, name='add_comment'),
    path('edit_post/<int:id>/', views.edit_post, name='edit_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),
    path('post_detail/<int:id>/', views.post_detail, name='post_detail'),
    path('followers/', views.followers_page, name='followers_page'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)