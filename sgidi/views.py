from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic


# Create your views here.


def index_view(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect('/login/')


def ideias_view(request):
    if request.user.is_authenticated():
        return render(request, 'ideias.html')
    else:
        return HttpResponseRedirect('/login/')
