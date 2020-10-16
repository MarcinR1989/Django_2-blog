# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .forms import EmailPostForm
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    return render(request, 'blog/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data  # Słownik zawierający pola formularza i ich wartości
        else:
            # print(form.errors)
            form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post,
                                                        'form': form})