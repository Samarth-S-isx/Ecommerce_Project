from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json


# Create your views here.


def index(request):
    products = Product.objects.all()
    n = len(products)
    nslides = n//4+ceil((n/4)-(n//4))
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = ceil((n/4))
        allProds.append([prod, range(1, nslides), nslides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        number = request.POST.get('number', '')
        query = request.POST.get('query', '')
        print("cont", name, email, number, query)
        contact = Contact(name=name, email=email, number=number, query=query)
        contact.save()
    return render(request, 'shop/contact.html')


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('items_json', '')
        fname = request.POST.get('fname', '')
        sname = request.POST.get('sname', '')
        email = request.POST.get('email', '')
        number = request.POST.get('number', '')
        address1 = request.POST.get('address1', '')
        # address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zipcode = request.POST.get('zipcode', '')
        # print("prod", fname, sname)
        order = Order(items_json=items_json, fname=fname, sname=sname, email=email,
                      number=number, city=city, state=state, zipcode=zipcode, address1=address1)
        order.save()
        thank = True
        params = {
            'id': order.order_id,
            'thank': thank
        }
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="the Order has been placed")
        update.save()

        return render(request, 'shop/checkout.html', params)
    return render(request, 'shop/checkout.html')


def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')
        # return HttpResponse(f"{order_id}and{email}")
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timeestamp})
                    response = json.dumps(
                        {'status': "success", 'updates': updates, 'itemjson': order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "wrong"}')
        except Exception as e:
            return HttpResponse(f'exception {e} idhar aa ra')
    return render(request, 'shop/tracker.html')


def searchprod(query, item):
    if query.lower() in item.product_name.lower() or query.lower() in item.desc.lower() or query.lower() in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    products = Product.objects.all()
    allProds = []
    prod = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prodcat = Product.objects.filter(category=cat)
        for item in prodcat:
            if searchprod(query, item):
                prod.append(item)
            else:
                continue
    n = len(prod)
    nslides = ceil((n/4))
    if len(prod) != 0:
        allProds.append([prod, range(1, nslides), nslides])
    params = {'allProds': allProds, 'msg': ''}
    if len(prod) == 0 or len(query) < 4:
        params = {'msg': "Please Enter valid Search"}
    return render(request, 'shop/search.html', params)


def prodview(request, id):
    product = Product.objects.filter(id=id)
    return render(request, 'shop/prodview.html', {'product': product[0]})
