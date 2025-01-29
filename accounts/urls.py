from django.urls import path # type: ignore
from accounts import views
from django.contrib.auth import views as auth_views # type: ignore



urlpatterns= [
    path('register/', views.register, name='register'),
    path('signin/', views.signin, name='signin'),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signout, name='signout'),
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password-reset-confirm'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('follow/<int:id>/', views.follow_unfollow, name='follow_unfollow'),
    path('edit_profile/<int:id>/', views.edit_profile, name='edit_profile'),
    path('edit_banner/', views.edit_banner, name='edit_banner'),
    path('delete_acc/<int:id>/', views.delete_acc, name='delete_acc'),
    path('search/', views.search, name='search'),


    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name= 'forgot-password.html'), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete')
]