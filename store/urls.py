from . import views
from django.urls import path

urlpatterns = [
	path('',views.store,name='store'),
	path('cart/',views.cart,name='cart'),
	path('checkout/',views.checkout,name='checkout'),
	path('update_item/',views.updateItem,name='update'),
	path('process_order/',views.processOrder,name='process_order'),
	path('login_page/',views.loginpage,name='login_page')
]
