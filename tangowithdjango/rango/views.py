from django.shortcuts import render
from models import Category, Page
from forms import CategoryForm, PageForm

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


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            # Show the user the index page
            return index(request)

        else:
            # Print form errors to the terminal
            print form.errors

    else:
        # If the request was not a post, display the Category creation form
        form = CategoryForm()

    # If form is invalid, render the form with any error messages
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                return category(request, category_name_slug)
        else:
            print form.errors

    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)
