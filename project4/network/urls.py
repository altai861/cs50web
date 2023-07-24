
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('new_post', views.new_post, name="new_post"),
    path('edit/<int:post_id>', views.edit_post, name="edit"),
    path('profile/edit/<int:post_id>', views.edit_post, name="edit"),
    path('profile/<str:username>', views.profile, name='profile'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('unfollow/<str:username>', views.unfollow, name='unfollow'),
    path('delete/<int:post_id>', views.delete, name='delete'),
    path('following', views.following, name='people_I_follow'),
    path('like/<int:post_id>', views.like, name="like"),
    path('unlike/<int:post_id>', views.unlike, name="unlike"),
    path('profile/like/<int:post_id>', views.like, name="like"),
    path('profile/unlike/<int:post_id>', views.unlike, name="unlike"),

]
