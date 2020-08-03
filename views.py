from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, UserForm
from .filters import OrderFilter
from .decorators import unaunthenticated_user , allowed_users, admin_only


from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@unaunthenticated_user
def registrationPage(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request, 'Account is created for ' + username)
            return redirect('login_page')



    context = {'form':form}
    return render(request,'registration.html', context)

@unaunthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username, password=password)

#its the login user
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    return render(request, 'login.html')

#its the logout user method

def logoutuser(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='login_page')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'customers':customers, 'orders':orders,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending }
    return render(request, 'index.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['Customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    print('ORDERS',  orders)

    context = {'orders':orders}
    return render(request, 'user.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def product(request):
    product = Product.objects.all()
    return render(request, 'product.html', {'product':product})

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def vendor(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()

    orders_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer,'orders':orders,
    'orders_count':orders_count,'myFilter':myFilter}
    return render(request, 'vendor.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):

    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        #print('its working:', request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}
    return render(request, 'order_form.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form =  OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'order_form.html', context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'delete.html', context)
