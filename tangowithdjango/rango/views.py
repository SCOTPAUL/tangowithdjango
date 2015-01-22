from django.shortcuts import HttpResponse, render
from models import Category

def index(request):
    # Retrieve the 5 highest rated categories
    # If fewer than 5 exist, that amount will be retrieved instead
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")

