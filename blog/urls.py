from django.urls import path

from . import views

# pozwala na organizacje urli na aplikacje

app_name = "blog"

urlpatterns = [
    # name gdy wykorzystujemy np reverse
    path("list", views.post_list, name="post_list"),
    # path converters https://docs.djangoproject.com/en/2.0/topics/http/urls/#path-converters.
    path(
        "<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    path("", views.PostListView.as_view(), name="post_list_cls"),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("my-posts/", views.MyPostListView.as_view(), name="my_posts"),
    path("add/", views.PostCreateView.as_view(), name="post_add"),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]
