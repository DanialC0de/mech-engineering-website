from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import News

def all_news(request):
    """نمایش همه اخبار با فیلتر و جستجو"""
    news_list = News.objects.filter(is_published=True)
    
    category = request.GET.get('category')
    if category:
        news_list = news_list.filter(category=category)
    
    search_query = request.GET.get('search')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) | 
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    paginator = Paginator(news_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'category': category,
        'search_query': search_query,
        'categories': News.CATEGORY_CHOICES,
    }
    return render(request, 'index-pages/news.html', context)


def news_detail(request, pk):
    """نمایش جزئیات یک خبر"""
    news = get_object_or_404(News, pk=pk, is_published=True)
    
    # اخبار مرتبط (همان دسته‌بندی، به جز خود خبر)
    related_news = News.objects.filter(
        category=news.category, 
        is_published=True
    ).exclude(pk=news.pk)[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'index-pages/details-pages/new.html', context)