from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder
from django.contrib import messages
from .forms import UserRegisterForm
# Create your views here.
def store(request):

	data=cartData(request)
	CartItems=data['CartItems']

	products=Product.objects.all()
	context={'products':products,'CartItems':CartItems}
	return render(request, 'store/store.html', context)

def cart(request):

	data=cartData(request)
	CartItems=data['CartItems']
	order=data['order']
	items=data['items']
		
	context={'items':items,'order':order,'CartItems':CartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	
	data=cartData(request)
	CartItems=data['CartItems']
	order=data['order']
	items=data['items']

	context={'items':items,'order':order,'CartItems':CartItems}	
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data=json.loads(request.body)
	productId=data['productId']
	action=data['action']
	print('Action:',action)
	print('Product:',productId)   
	
	customer=request.user.customer
	product=Product.objects.get(id=productId)
	order,created=Order.objects.get_or_create(customer=customer,complete=False)
	orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

	if action=="add":
		orderItem.quantity=(orderItem.quantity + 1)
	elif action=="remove":
		orderItem.quantity=(orderItem.quantity - 1)	
	orderItem.save()
	if orderItem.quantity <=0:
		orderItem.delete()	
	return JsonResponse('Item was added',safe=False)

def processOrder(request):
	transaction_id=datetime.datetime.now().timestamp()
	data=json.loads(request.body)
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		
	else:
		customer,order=guestOrder(request,data)

	total=float(data['form']['total'])
	order.transaction_id=transaction_id
	if total==order.get_cart_total:
		order.complete=True
	order.save()

	if order.shipping ==True:
		ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['city'],
				state=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
				)

	return JsonResponse('payment submitted',safe=False)



def register(request):
	if request.method=='POST':
		form=UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created succesfully, Login as {username}!')
			return redirect('login')
	else:
		form=UserRegisterForm()
	return render(request, 'store/create.html', {'form': form})
