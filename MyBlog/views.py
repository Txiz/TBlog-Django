import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from MyBlog.models import Category, Article, Tag, RotationChart


def global_variable(request):
    all_category = Category.objects.all().order_by('index')
    all_tag = Tag.objects.all()
    hot_article = Article.objects.all().order_by('-views')[:10]
    picture_list = RotationChart.objects.filter(is_active=False)
    picture_active = RotationChart.objects.filter(is_active=True)
    return locals()


# 首页
def index(request):
    all_article = Article.objects.all().order_by('id')
    paginator = Paginator(all_article, 5)
    page = request.GET.get('page')
    try:
        all_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        all_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        all_list = paginator.page(paginator.num_pages)
    return render(request, 'my_blog/index.html', locals())


# 列表页
def list_page(request, list_id):
    category_name = Category.objects.get(id=list_id)
    all_list = Article.objects.filter(category_id=list_id).order_by('id')
    paginator = Paginator(all_list, 5)
    page = request.GET.get('page')
    try:
        all_list = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        all_list = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        all_list = paginator.page(paginator.num_pages)
    return render(request, 'my_blog/list.html', locals())


# 内容页
def show_page(request, article_id):
    article = Article.objects.get(id=article_id)
    article.body = markdown.markdown(article.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    previous_blog = Article.objects.filter(create_time__gt=article.create_time, category=article.category.id).first()
    next_blog = Article.objects.filter(create_time__lt=article.create_time, category=article.category.id).last()
    article.views = article.views + 1
    article.save()
    return render(request, 'my_blog/show.html', locals())


# 标签页
def tag_page(request, tag):
    all_list = Article.objects.filter(tag__name=tag).order_by('id')
    tag_name = Tag.objects.get(name=tag)
    page = request.GET.get('page')
    paginator = Paginator(all_list, 5)
    try:
        all_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        all_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        all_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'my_blog/tag.html', locals())


# 搜索页
def search_page(request):
    search_key = request.GET.get('search')
    all_list = Article.objects.filter(title__contains=search_key)
    page = request.GET.get('page')
    paginator = Paginator(all_list, 5)
    try:
        all_list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        all_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        all_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'my_blog/search.html', locals())
