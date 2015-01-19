from django.shortcuts import HttpResponse, render

def index(request):
    context_dict = {'boldmessage': "I am bold font from the context"}
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a><br/><p>This tutorial has been put together by Paul Cowie, 2082442</p>")

