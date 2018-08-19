from django.shortcuts import render


def index(request):
    featured = []
    trending = []
    for i in range(1, 5):
        product = {
            'image': 'img/product-{}.jpg'.format(i),
            'title': 'Product {}'.format(i),
        }
        featured.append(product)

    for i in range(1, 7):
        product = {
            'image': 'img/product-{}1.jpg'.format(i),
            'title': 'Product {}'.format(i),
        }
        trending.append(product)

    context = {
        'featured': featured,
        'trending': trending,
    }
    return render(request, 'mainapp/index.html', context)


def details(request):
    products = []
    for i in range(1, 4):
        product = {
            'image': 'img/product-{}1.jpg'.format(i),
            'title': 'Product {}'.format(i),
        }
        products.append(product)

    context = {
        'products': products,
    }
    return render(request, 'mainapp/details.html', context)
    
    
def products(request):
    products = []
    for i in range(1, 7):
        product = {
            'image': 'img/product-{}1.jpg'.format(i),
            'title': 'Product {}'.format(i),
        }
        products.append(product)

    context = {
        'products': products,
    }
    return render(request, 'mainapp/products.html', context)
    
    
def contacts(request):
    return render(request, 'mainapp/contacts.html')
