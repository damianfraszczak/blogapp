from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from blog.forms import CommentForm, EmailPostForm, PostForm
from blog.models import Post
from users.models import Company

# https://docs.djangoproject.com/en/2.0/topics/class-based-views/intro/.


class PostListView(ListView):
    # can use model = Post and default manager will be used
    queryset = Post.published.all()
    # default list object_list
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

    def get_queryset(self):
        site = get_current_site(self.request)
        tenant = get_object_or_404(Company, site=site)
        ## to sie rowna to samo co request.tenant dzieki middleware
        tenant = getattr(self.request, "tenant", None)
        return super().get_queryset().filter(author__company=tenant)


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"posts": posts, "page": page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post = post
                new_comment.author = request.user
                new_comment.save()
                return redirect(request.path_info)
        else:
            return redirect("login")
    else:
        form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "new_comment": new_comment,
        },
    )


def post_share(request, post_id):
    sent = False
    post = get_object_or_404(Post, id=post_id, status="published")
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # budowanie url absolutnego
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) recommends you reading {post.title}"
            )
            message = f"Read {post.title} at {post_url}\n\n{cd['name']} comments: {cd['comments']}"

            message = render_to_string(
                "blog/post/share_email.txt",
                {
                    "post": post,
                    "post_url": post_url,
                    "name": cd["name"],
                    "email": cd["email"],
                    "comments": cd["comments"],
                },
            )

            send_mail(subject, message, "admin@myblog.com", [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/post/my_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post/post_form.html"
    success_url = reverse_lazy("blog:my_posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post/post_form.html"
    success_url = reverse_lazy("blog:my_posts")

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post/post_confirm_delete.html"
    success_url = reverse_lazy("blog:my_posts")

    def test_func(self):
        return self.get_object().author == self.request.user
