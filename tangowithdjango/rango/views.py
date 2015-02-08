from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.shortcuts import render
from models import Category, Page, User
from forms import CategoryForm, PageForm, UserForm, UserProfileForm, UserResetPassword
from datetime import datetime


def index(request):
    # Retrieve the 5 highest rated categories
    # If fewer than 5 exist, that amount will be retrieved instead
    category_list = Category.objects.order_by('-likes')[:5]

    # Retrieve the 5 or fewer pages with the most views
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    # Get number of visits to the site
    # If the cookie does not exist, set visits to 1
    visits = request.session.get('visits', 1)
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')

    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if(datetime.now() - last_visit_time).days > 0:
            visits += 1

            # Flag last_visit cookie to be updated
            reset_last_visit_time = True

    else:
        # last_visit cookie doesn't exist, flag it for resetting
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits
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
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    context_dict = {'aboutmessage': "This tutorial has been put together by Paul Cowie, 2082442",
                    'visits': count}

    return render(request, 'rango/about.html', context_dict)


@login_required
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


@login_required
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


@login_required
def restricted(request):
    restricted_text = "Since you are logged in, you can see this text!"
    return render(request, 'rango/restricted.html', {'restricted_text': restricted_text})