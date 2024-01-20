from django.urls import path, re_path, register_converter
from . import views
from . import  converters


register_converter(converters.FourDigitYearCinverter, 'year4')

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),

    path('about/', views.about, name='about'),

    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),

    path('cat/<int:cat_id>/', views.categories, name='cat_id'),
    path('cat/<slug:cat_slug>/', views.categories_by_slug, name='cat'),
    path('archive/<year4:year>/', views.archive, name='archive'),


]


