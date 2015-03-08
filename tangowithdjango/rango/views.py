from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from models import Category, Page, UserProfile
from forms import CategoryForm, PageForm, UserProfileForm
from bing_search import run_query


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
        pages = Page.objects.filter(category=category).order_by('-views')

        context_dict['pages'] = pages
        context_dict['category'] = category

        if request.method == 'POST':
            if 'query' in request.POST:
                query = request.POST['query'].strip()

                if query:
                    context_dict['result_list'] = run_query(query)
        else:
            # If GET, increment view count
            category.views += 1
            category.save()

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


def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            try:
                page = Page.objects.get(pk=page_id)
                page.views += 1
                page.save()
                return redirect(page.url)

            except Page.DoesNotExist:
                pass

    return redirect(index)


@login_required
def profile(request):
    try:
        user = request.user
        user_profile = UserProfile.objects.get(user=user)

        context_dict = {'username': user.username,
                        'email': user.email,
                        'website': user_profile.website,
                        'picture': user_profile.picture,
                        }

        return render(request, 'rango/profile.html', context_dict)

    except UserProfile.DoesNotExist:
        redirect(index)


@login_required
def register_profile(request):
    if request.method == 'POST':
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(request.POST, instance=user_profile)
        except UserProfile.DoesNotExist:
            form = UserProfileForm(request.POST)

        if form.is_valid():
            new_user_profile = form.save(commit=False)
            new_user_profile.user = request.user

            if 'picture' in request.FILES:
                new_user_profile.picture = request.FILES['picture']

            new_user_profile.save()
            return index(request)

        else:
            print form.errors

    else:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            form = UserProfileForm(instance=user_profile)
        except UserProfile.DoesNotExist:
            form = UserProfileForm()

    return render(request, 'registration/profile_registration.html', {'form': form})


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