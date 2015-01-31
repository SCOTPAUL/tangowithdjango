from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from models import Category, Page
from forms import CategoryForm, PageForm, UserForm, UserProfileForm


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


def register(request):
    # Used for telling the template if a user has registered yet
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # Hash the user's password and update
            # the user with this hashed password
            user.set_password(user.password)
            user.save()

            # Now deal with the UserProfile instance
            profile = profile_form.save(commit=False)
            profile.user = user

            # If a profile picture was provided, get this
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now that the picture has been dealt with, save
            profile.save()

            # Now the user has been registered
            registered = True

        # Invalid form
        else:
            print user_form.errors, profile_form.errors

    # If the request is not a POST, show the forms
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {'user_form': user_form,
                                                   'profile_form': profile_form,
                                                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # If user is correctly authenticated...
        if user:
            if user.is_active:
                login(request, user)

                # Send user back to homepage
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        # Bad login details were provided.
        else:
            print "Invalid login details: {0}, {1}".format(username, password)

            invalid_detail_message = "Invalid login details supplied: "
            if username == "" or password == "":
                invalid_detail_message += "Username or password fields were empty."
            else:
                invalid_detail_message += "Username or password were incorrect."

            return HttpResponse(invalid_detail_message)

    # Not a POST, so display the form
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    restricted_text = "Since you are logged in, you can see this text!"
    return render(request, 'rango/restricted.html', {'restricted_text': restricted_text})


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')



