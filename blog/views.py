from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from blog.models import Post, Status
from django.views.decorators.http import require_POST

class PostView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/post/post_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.published.all()


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post,
                             status=Status.PUBLISHED,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            form = CommentForm()

    return render(request, 'blog/post/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status= Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}'s comments: {cd['comments']}"

            # Отправляем email (но с выводом в консоль)
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])

            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Status.PUBLISHED)
    comment = None
    form = CommentForm(data= request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {
                      'post': post,
                      'form': form,
                      'comment': comment,
                  })



