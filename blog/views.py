from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm,SearchForm
from blog.models import Post, Status
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank



def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/post_list.html', {
        'posts': posts,
        'tag': tag,
    })



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

    # Логика для схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)  # Получаем ID тегов текущего поста
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)\
                                  .annotate(same_tags=Count('tags'))\
                                  .order_by('-same_tags', '-publish')[:4]  # Ограничиваем количество постов

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            form = CommentForm()  # Очищаем форму после успешного сохранения

    return render(request, 'blog/post/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,  # Теперь переменная всегда определена
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


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search = SearchVector('title', 'content'),
            ).filter(search=query)

    return render(request,
                  'blog/post/search.html',
            {'form': form,
                    'query': query,
                    'results': results
             })



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



def post_search(request):
    form = SearchForm()  # Исправлено
    query = None
    result = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'content', config='russian')  # Добавлен config
            search_query = SearchQuery(query, config='russian')

            result = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')  # Исправлено '-runk' на '-rank'

    return render(request, 'blog/post/search.html', {
        'form': form,
        'query': query,
        'result': result
    })



