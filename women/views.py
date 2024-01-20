from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template.loader import render_to_string
from .models import Women, Category, TagPost
from .forms import AddPostForm
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse_lazy
from .utils import DataMixin
from  django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

menu = [
    {'title':'О сайте', 'url_name':'about'},
    {'title':'Добавить статью', 'url_name':'add_page'},
    {'title':'Обратная связь', 'url_name':'contact'},
    {'title':'Войти', 'url_name':'login'},
    ]

class WomenHome(DataMixin, ListView):
 #   model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    cat_selected = 0
    title_page = 'Главная страница'

    def get_queryset(self):
        return  Women.poblished.all().select_related('cat')


#def index(request):
#    posts = Women.poblished.all().select_related('cat')
#    data = {'title': 'главная страница?',
#            'menu':menu,
#            'float':25.24,
#            'list':[1,2,'abg', True],
#            'set':{1,2,3,5,6,1},
#            'dict':{'key_1':'value_1', 'key_2':'value_2'},
#            'posts':posts,
#            'cat_selected':0,
#            }
#    return render(request, 'women/index.html', context=data)

class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )

    def get_queryset(self):
        return Women.poblished.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')


class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
 #   allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Women.poblished.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')



class ShowPost(DataMixin, DetailView):
 #   model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.poblished, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, FormView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'women.add_women'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        w.save()
        return super().form_valid(form)

 #   def form_valid(self, form):
 #       form.save()
 #       return super().form_valid(form)



class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'women.change_women'


def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required
def about(request):
    if request.method == "POST":
        handle_uploaded_file(request.FILES['file_upload'])

    return render(request, 'women/about.html', {'title': 'О сайте', 'menu':menu})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
          #  print(form.cleaned_data)
     #      try:
 #              Women.objects.create(**form.cleaned_data)
           #    form.save()
         #      return redirect('home')
       #    except:
        #      form.add_error(None, 'Ошибка добавления поста')
    else:
        form = AddPostForm()


    data = {
        'title': 'Добавление статьи',
        'menu': menu,
        'form': form
    }
    return render(request, 'women/addpage.html', data)


#@permission_required(perm='women.view_women', raise_exception=True)
def contact(request):
    return render(request, 'women/connection.html',  {'title': 'Контакты'})


def login(request):
    return HttpResponse('Авторизация')

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'women/post.html', data)


def categories(request, cat_id):
    return HttpResponse(f'page2<p>id: {cat_id}</p>')



def categories_by_slug(request, cat_slug):
    print(request.GET)
    return HttpResponse(f'page2<p>slug: {cat_slug}</p>')

def archive(request, year):
    if year>2023:
        raise Http404()
    return HttpResponse(f'<h1>Архив по годам</h1><p> {year}</p>')

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts =Women.poblished.filter(cat_id=category.pk).select_related('cat')

    data = {'title': f'Рубрика: {category.name}',
            'menu': menu,
            'posts': posts,
            'cat_selected': category.pk,
            }
    return render(request, 'women/index.html', context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts=tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'women/index.html', context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

