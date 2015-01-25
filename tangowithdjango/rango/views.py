from django.shortcuts import HttpResponse, render
from models import Category, Page

def index(request):
    # Retrieve the 5 highest rated categories
    # If fewer than 5 exist, that amount will be retrieved instead
    category_list = Category.objects.order_by('-likes')[:5]

    # Retrieve the 5 or fewer pages with the most views
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}
    return render(request, 'rango/index.html', context_dict)


def category(request, category_name_slug):
    context_dict = {}

    try:
        # Attempt to get the category instance with category_name_slug as its slug
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all the pages related to the category
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        # Couldn't find the category, so do nothing
        pass

    return render(request, 'rango/category.html', context_dict)


def about(request):
    context_dict = {'aboutmessage': "This tutorial has been put together by Paul Cowie, 2082442"}
    return render(request, 'rango/about.html', context_dict)
