from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 网站首页
    path('list-<int:list_id>.html', views.list_page, name='list'),  # 列表页
    path('show-<int:article_id>.html', views.show_page, name='show'),  # 内容页
    path('tag/<tag>', views.tag_page, name='tag'),  # 标签列表页
    path('s/', views.search_page, name='search'),  # 搜索列表页
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
