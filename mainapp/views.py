from django.shortcuts import render


def index(request):
    return render(request, 'mainapp/index.html')


def details(request):
    return render(request, 'mainapp/details.html')
    
    
def products(request):
    return render(request, 'mainapp/products.html')
    
    
def contacts(request):
    return render(request, 'mainapp/contacts.html')
