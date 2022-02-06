#from django.shortcuts import render
#from django.http import HttpResponse
# Create your views here.

#def index(request):
#    return HTTPResponse('This is the index page.')
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.models import product
from django import forms
from django.forms.models import model_to_dict
from django.db.models import Q
import datetime
from dateutil.parser import parse

@login_required(login_url='/login/')
def index(request):
    return render(request, 'dashboard/index.html')

@login_required(login_url='/login/')
def products(request):
    if request.method == 'POST':
            name = request.POST['product_name']
            manufacturer = request.POST['manufacturer_name']
            try:
                expiry = request.POST['product_expiry']
                if expiry.find("-") != 4:
                    raise Exception("Format must be 2020-01")
                for testing in expiry.split("-"):
                    int(testing)
                expiry = expiry + "-01"
                
            except:
                context = {"errors" :"Format must be 2020-01"}
                return render(request, 'dashboard/products.html',context)
                #raise forms.ValidationError("Invalid code")
            price = request.POST['product_price']
            qunatity = request.POST['product_qunatity']
            new_product = product(product_name = name,manufacturer_name = manufacturer,product_qunatity=qunatity,product_expiry=expiry,product_price=price)
            sucess = {"sucess_msg" :"Product Added Sucessfully"}
            new_product.save()
            return render(request, 'dashboard/products.html',sucess)
    if request.method=='GET':
        return render(request, 'dashboard/products.html')



@login_required(login_url='/login/')
def manage(request):
    return render(request, 'dashboard/manage.html')

@login_required(login_url='/login/')
def view(request):
    if request.method == 'POST':
        query = request.POST['search']
        searched_products = product.objects.filter( Q(product_name__icontains=query) | Q(manufacturer_name__icontains=query) )
        context = {'searched_products': searched_products}
        return render(request, 'dashboard/view.html',context)


@login_required(login_url='/login/')
def edit(request,id=0):
    if request.method == 'GET':
        try:
            searched_products = product.objects.get(product_id=id)
        except:
            return render(request, 'dashboard/error.html')
        context = model_to_dict(searched_products)
        context['product_expiry'] = str(parse(context['product_expiry'].strftime("%d %b, %Y")).year)+"-"+str(parse(context['product_expiry'].strftime("%d %b, %Y")).month)
        return render(request, 'dashboard/edit.html',context)
    
    if request.method == 'POST':
            name = request.POST['product_name']
            manufacturer = request.POST['manufacturer_name']
            try:
                expiry = request.POST['product_expiry']
                if expiry.find("-") != 4:
                    raise Exception("Format must be 2020-01")
                for testing in expiry.split("-"):
                    int(testing)
                expiry = expiry + "-01" 
            except:
 
                context = {"errors" :"Format must be 2020-01"}
                return render(request, 'dashboard/products.html',context)
                #raise forms.ValidationError("Invalid code")
            price = request.POST['product_price']
            qunatity = request.POST['product_qunatity']
            try:
                searched_products = product.objects.filter(product_id=id)
            except:
                return render(request, 'dashboard/error.html')
            searched_products = product(product_name = name,manufacturer_name = manufacturer,product_qunatity=qunatity,product_expiry=expiry,product_price=price)
            sucess = {"sucess_msg" :"Product Updated Sucessfully"}
            searched_products.save()
            return render(request, 'dashboard/products.html',sucess)


@login_required(login_url='/login/')
def delete(request,id=0):
    if request.method == 'GET':
        try:
            searched_products = product.objects.get(product_id=id)
        except:
            return render(request, 'dashboard/error.html')
        context = model_to_dict(searched_products)
        context['product_expiry'] = str(parse(context['product_expiry'].strftime("%d %b, %Y")).year)+"-"+str(parse(context['product_expiry'].strftime("%d %b, %Y")).month)
        return render(request, 'dashboard/delete.html',context)  
    if request.method == 'POST':
        try:
            searched_products = product.objects.get(product_id=id)
        except:
            return render(request, 'dashboard/error.html')
        searched_products.delete()
        sucess = {"sucess_msg" :"Product Deleted Sucessfully"}
        return render(request, 'dashboard/manage.html',sucess)

def add(request,id=0):
    if request.method == 'GET':
        return render(request, 'dashboard/add.html',context)
    
    searched_products = []
    sucess = {"sucess_msg" :""}
    if request.method == 'POST' :
        if request.POST.get('search', False):
            query = request.POST['search']
            searched_products = product.objects.filter( Q(product_name__icontains=query) | Q(manufacturer_name__icontains=query) )
            

        if request.POST.get('qunatity', False):
            try:
                qunatity = int(request.session[str(id)])
            except:
                request.session[str(id)] = 0
                qunatity = 0

            cart_product = product.objects.get(product_id=int(id))
            print(int(request.POST['qunatity']))
            print(cart_product.product_qunatity)
            if (int(request.POST['qunatity']) + qunatity) < cart_product.product_qunatity:
                if qunatity == 0:
                    qunatity  = int(request.POST['qunatity'])
                if qunatity > 0:
                    qunatity  = qunatity + int(request.POST['qunatity'])
                del request.session[str(id)]
                request.session[id] = qunatity
                sucess = {"sucess_msg" :"Product Added to Cart"}
            else:
                del request.session[str(id)]
                sucess = {"error_msg" :"Qunatity Limited on Stock"}
            searched_products = {}

        cart = []
        cart_product = {}
        total_price = 0
        for key, value in request.session.items():
            if "_auth" not in str(key):
                try:
                    cart_product = product.objects.get(product_id=int(key))
                    total_item_price = ( cart_product.product_price * value )
                    total_price = total_price + total_item_price
                except:
                    return render(request, 'dashboard/error.html')
                cart.append((cart_product,value,total_item_price))
        print(total_price)
        context = {'searched_products': searched_products , 'cart':cart, 'sucess':sucess, 'total_price':total_price }
        return render(request, 'dashboard/add.html',context)

@login_required
def del_cart(request,id=0):
        searched_products = []
        del request.session[str(id)]
        cart = []
        cart_product = {}
        for key, value in request.session.items():
            if "_auth" not in str(key):
                try:
                    cart_product = product.objects.get(product_id=int(key))
                except:
                    
                    return render(request, 'dashboard/error.html')
                cart.append((cart_product,value))
        print(cart)
        context = {'searched_products': searched_products , 'cart':cart }
        return render(request, 'dashboard/add.html',context)

@login_required
def checkout(request):
    if request.method == 'GET' :
        total_price = 0
        cart = []
        for key, value in request.session.items():
            if "_auth" not in str(key):
                print(key, value)
                try:
                    cart_product = product.objects.get(product_id=int(key))
                    total_item_price = ( cart_product.product_price * value )
                    total_price = total_price + total_item_price
                except:
                    print("hsa")
                    return render(request, 'dashboard/error.html')
                cart.append((cart_product,value,total_item_price))

        context = {'cart':cart, 'total_price':total_price }
        return render(request, 'dashboard/checkout.html',context)

    if request.method == 'POST' :
        keys = []
        for key, value in request.session.items():
            if "_auth" not in str(key):
                print(key, value)
                try:
                    keys.append(key)
                    cart_product = product.objects.get(product_id=int(key))
                    cart_product.product_qunatity = (cart_product.product_qunatity-value)
                    cart_product.save()
                except:
                    print("hsa")
                    return render(request, 'dashboard/error.html')
        for key in keys:
            del request.session[str(key)]
        sucess = {"sucess_msg" :"Transction Completed Sucessfully"}
        return render(request, 'dashboard/index.html',sucess)
