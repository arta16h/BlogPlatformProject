from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Category, Comment
from users.models import Author
from .forms import PostCreationForm, CommentUpdateForm, CommentCreationForm
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy


# Create your views here.


def home(request):
    context = {}
    if request.GET.get('search'):
        search = request.GET['search']
        cd = Post.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
        context = {'searched': cd}

    return render(request, 'index.html', context)


def post_list(request):
    all_posts = Post.objects.all()
    return render(request, "Blog/post_list.html", {"all_posts": all_posts})

class PostDetailView(DetailView):
    model = Post
    template_name = "Blog/post.html"

    def get_context_data(self, **kwargs):
        context = self.get_context_data(**kwargs)
        post = self.get_object()
        context["comment"] = post.comment_set.all()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment = request.POST.get("com")
        author_name = request.POST.get("username")

        if comment and author_name:
            author = Author.objects.get_or_create(name=author_name)
            Comment.objects.create(post=post, author=author, content=comment)
            return redirect("post_details", post.pk)

        return self.get(request, *args, **kwargs)


# def post_details(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = post.comment_set.all()
#     if request.method == 'POST':
#         comment = request.POST.get('comm')
#         author = request.POST.get('username')
#         if comment != None and author != None:
#             if Author.objects.filter(name=author).exists():
#                 Comment.objects.create(post=post, author=author, content=comment)
#             else:
#                 author = Author.objects.create(name=author)
#                 Comment.objects.create(post=post, author=author, content=comment)
#             return redirect('post_details', pk)

#     return render(request, "Blog/post.html", {"post": post, "comments": comments})

class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'Blog/comment_update.html'

    def form_valid(self, form):
        super().form_valid(form)
        return redirect('post_details', self.object.post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        return context
    

# def comment_update(request, pk):
#     comment = Comment.objects.get(id=pk)
#     if request.method == "POST":
#         form = CommentUpdateForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             comment.content = cd['content']
#             comment.save()
#             return redirect('post_details', comment.post.id)
#     else:
#         form = CommentUpdateForm(initial=
#                                  {'content': comment.content}
#                                  )

#     return render(request, 'Blog/comment_update.html', {'form': form, 'comm': comment})


def category_list(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        Category.objects.create(name=name, description=description)

    all_category = Category.objects.all()

    return render(request, "Blog/category_list.html", {"all_category": all_category})


def category_details(request, pk):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid:
            f = form.save(commit=False)
            category = Category.objects.get(id=pk)
            f.category = category
            f.save()

        return redirect('blog:category_details', pk)
    else:
        form = PostCreationForm()
        category = Category.objects.get(id=pk)
        authors = Author.objects.all()
        posts = category.post_set.all()
    return render(request, "Blog/category_details.html",
                  {"category": category, 'posts': posts, 'authors': authors, 'form': form})
