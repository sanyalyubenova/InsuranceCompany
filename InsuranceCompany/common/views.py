from django.shortcuts import render
from templates import common
# Create your views here.

def home(request):
    return render(request, template_name='common/home.html')

def about(request):
    pass

def contact(request):
    pass
