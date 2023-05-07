
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# At Lec 32
# After 42 " ,Contact "
from . models import Product,Contact,Order,OrderUpdate
from math import ceil

import json

def index(request):
    
    #  Showing Only Single Slide.. LEC 32 
    ''' products = Product.objects.all()
        n = len(products)
        nSlides = ceil(n/4)
        params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
        return render(request, 'shop/index.html', params)
    '''


    ''' To see what product.objects.all() returns / product.objects.values('category') returns'''
    ''' python manage.py shell 
        from shop.models import product
        product.objects.values('product_name')
    '''

    # LEC 34 Showing prod Category-wise..

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = ceil(n / 4) 
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)



# Before Lec 32
# def index(request):
#     return render(request, 'shop/index.html')

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    # for getting <input> value use request.GET.get/.post
    # we use name="search" to fetch the input value 

    query= request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)




def about(request):
    return render(request, 'shop/about.html')


# After 42
def contact(request):
    thank=False
    if request.method=="POST":
        # print(request)
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        # print(name,email,phone, desc )
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, "shop/contact.html",{'thank':thank})




def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                # Object of OderUpdate has been made when It was placed (at chechout) , rest you can make at admin page(in database )
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                # We are using default=str because json wants everything in str but item.timestamp is of 'datetime' type
                # We are using items_json to fetch info. about the placed-order (we cann't use cart because it contains all the items but we want only placed onces)
                response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response) # BEfore Lec 53: response == [ {"text": "The order has been placed Successfully..", "time": "2023-05-01"}, {"text": "Your order is dispatched at 16:00 From Warehouse..", "time": "2023-05-01"}]
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def productView(request,myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)
    # .filter returns a list, but we know that there will be a single ele that has unique id..
    return render(request, 'shop/prodView.html',{'product':product[0]})

# def checkout(request):
#     if request.method=="POST":
#         items_json= request.POST.get('itemsJson', '')
#         name=request.POST.get('name', '')
#         email=request.POST.get('email', '')
#         address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
#         city=request.POST.get('city', '')
#         state=request.POST.get('state', '')
#         zip_code=request.POST.get('zip_code', '')
#         phone=request.POST.get('phone', '')

#         order = Order(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone)
#         order.save()

#         # After LEC 50
#         update= OrderUpdate(order_id= order.order_id, update_desc="The order has been placed Successfully..")
#         update.save()

#         thank=True
#         id=order.order_id
#         return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
        
#     return render(request, 'shop/checkout.html')

# Now removing thank and adding a dismiss mesaage using django message framework

from django.contrib import messages

def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        state=request.POST.get('state', '')
        zip_code=request.POST.get('zip_code', '')
        phone=request.POST.get('phone', '')

        if len(name)<2 or len(email)<3 or len(address)<5 or len(phone)<10 or len(state)<3 or len(city)<3 or len(zip_code)<4  :
            messages.error(request, "Please fill the form correctly")
        else:

            order = Order(items_json= items_json, name=name, email=email, address= address, city=city, state=state, zip_code=zip_code, phone=phone)
            order.save()

            update= OrderUpdate(order_id= order.order_id, update_desc="Your  order has been placed Successfully..")
            update.save()
            messages.success(request, "Your message has been successfully sent")
        
        return render(request, 'shop/checkout.html')
        
    return render(request, 'shop/checkout.html')