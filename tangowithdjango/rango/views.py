from django.shortcuts import HttpResponse, render

def index(request):
    context_dict = {'boldmessage': "I am bold font from the context"}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {'aboutmessage': "This tutorial has been put together by Paul Cowie, 2082442"}
    return render(request, 'rango/about.html', context_dict)
