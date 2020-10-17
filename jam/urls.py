from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('blog', views.blog),
    path('create', views.create),
    path('register', views.register),
    path('logout', views.logout),
    path('profile', views.profile),
    path('create_blog_post', views.create_blog_post),
    path('like/<int:id>', views.like),
    path('comment/<int:id>', views.comment),
    path('delete_comment/<int:id>', views.delete_comment),
    path('delete_post/<int:id>', views.delete_post),
    path('edit_post/<int:id>', views.edit_post),
    path('edit_post_success/<int:id>', views.edit_post_success),
    path('gig_wall', views.gig_wall),
    path('create_gig', views.create_gig),
    path('delete_gig/<int:id>', views.delete_gig),
]