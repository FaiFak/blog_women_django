from django.urls import path, re_path, register_converter
from women import views

urlpatterns = [
    path('', views.WomenHome.as_view(), name="home"),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    # path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', views.show_category, name='category'),
    path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
    # path('tag/<slug:tag_slug>', views.show_tag_postlist, name='tag'),
    path('tag/<slug:tag_slug>', views.WomenTagPostList.as_view(), name='tag'),
]
