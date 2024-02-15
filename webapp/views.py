from django.shortcuts import render, redirect
from .forms import CreateUser, LogIn, CreateRecord, UpdateRecord

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages

# Create your views here.

# HomePage
def home(request):
    return render(request, 'webapp/index.html')

# Register a user
def register(request):
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registration successful')
            return redirect('my-login')
    
    context = {'form': form}
    return render(request, 'webapp/register.html', context=context)

# log in a user
def my_login(request):
    form = LogIn()

    if request.method == 'POST':
        form = LogIn(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'successfuly logged in')
                return redirect('dashboard')
    
    context = {'form': form}
    return render(request, 'webapp/my-login.html', context=context)

# user logout
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'successfuly logged out')
    return redirect('my-login')

# dashboard
@login_required(login_url='my-login')
def dashboard(request):
    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)

# adding a record
@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecord()
    if request.method == 'POST':
        form = CreateRecord(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record created successfully')
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'webapp/create-record.html', context=context)

# update a record 
@login_required(login_url='my-login')
def update_record(request, pk):
    record = Record.objects.get(id=pk)
    form = UpdateRecord(instance=record)
    if request.method == 'POST':
        form = UpdateRecord(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully')
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'webapp/update-record.html', context=context)

# read a record 
@login_required(login_url='my-login')
def read_record(request, pk):
    all_records = Record.objects.get(id=pk)
    context = {'record': all_records}
    return render(request, 'webapp/view-record.html', context=context)

# delete a record 
@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, 'Record deleted successfully')
    return redirect('dashboard')