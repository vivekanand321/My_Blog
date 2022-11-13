from enum import unique
from django.urls import path
from . import views
urlpatterns = [
    path("",views.Starting_Page.as_view(),name="starting-page"),
    path("posts",views.AllPostsView.as_view(),name="posts-page"),
    path("posts/<slug:slug>",views.SinglePostView.as_view(),name="post-detail-page"),#/posts/my-first-post,using slug type to confirm the format which enter,
    # slug type may be int or str.
    path("read-later",views.ReadLaterView.as_view(),name="read-later")
]
