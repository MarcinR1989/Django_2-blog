# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from django.core.mail import send_mail


# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
    # print("context_object_name:", context_object_name)
    # print("context_object_name:", type(context_object_name))


# def post_list(request):...
#     object_list = Post.published.all()  # pobranie wszystkich postów gdzie status='published'
#     paginator = Paginator(object_list, 3)  # trzy posty na każdej stronie
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # jeżeli zmienna page nie jest liczbą całkowitą
#         # wówczas pobierana jest pierwsza strona wyników.
#         posts = paginator.page(1)
#     except EmptyPage:
#         # Jeżeli zmienna page ma wartość większą niż numer ostatniej strony
#         # wyników, wtedy pobierana jest ostatnia strona wyników
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/post/list.html',
#                   {'page': page,
#                    'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for a given post
    comments = post.comment_set.filter(active=True)  # TODO wg ksiązki powinno być 'comments = post.comments.filter(active=True)'

    if request.method == 'POST':
        # Comment has been published
        comment_form = CommentForm(data=request.POST)  # TODO 'data=' do wyjebania ???
        if comment_form.is_valid():
            # Utworzenie obiektu Comment, ale jeszcze nie zapisuję go w bazie danych
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # Słownik zawierający pola formularza i ich wartości
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd["name"]} ({cd["email"]}) encourages you to read {post.title}.'
            message = f'Read post "{post.title}" on {post_url}\n\n Comment added by {cd["name"]}: {cd["comments"]}'
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        # print(form.errors)
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
