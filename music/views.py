from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello_world(request):
    return HttpResponse('Witaj świecie!')


def main_page(request):
    return render(request, template_name='index.html')
