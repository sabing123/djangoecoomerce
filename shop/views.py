from django.shortcuts import render
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json

# Create your views here.
from django.http import HttpResponse


def index(request):
    # products = Product.objects.all()
    # print(products)
    # params = {'no_of_slides':nslides,'range':range(1, nslides), 'product': products}
    # allProds = [[products, range(1,nslides),nslides],
    #             [products, range(1, nslides),nslides]]

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nslides), nslides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def searchMatch(query, item):
    # retrun true only of the query matches the item
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nslides), nslides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg':"please enter valid keywords"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method == "POST":
        fname = request.POST.get('fname', '')
        email = request.POST.get('email', '')
        pnumber = request.POST.get('phonenumber', '')
        country = request.POST.get('country', '')
        subject = request.POST.get('subject', '')
        contact = Contact(fullname=fname, email=email, pnumber=pnumber, country=country, subject=subject)
        contact.save()
    return render(request, 'shop/contact.html', {'Thank You!': thank})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].item_json], default=str)
                return HttpResponse(response)

            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def productview(request, myid):
    # fetch the product using id
    product = Product.objects.filter(id=myid)
    print(product)
    return render(request, 'shop/prodview.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        item_json = request.POST.get('itemsJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(item_json=item_json, amount=amount, name=name, email=email, address=address, city=city,
                       state=state,
                       zip_code=zip_code, phone=phone)
        order.save()

        update = OrderUpdate(order_id=order.order_id, update_desc="The Order has been placed")
        update.save()

        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})

    return render(request, 'shop/checkout.html')
