
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def main_page(request):
    return render (request,'pages/main-page.html')


def home(request):
    return render (request,'pages/home.html')


def pin(request):
    if request.user.is_authenticated:
        print("hello")
        return redirect('home')
    else:
        if request.method == "POST":
            accno = request.POST.get('accno')
            passs = request.POST.get('pin')
            print(accno)
            print(passs)
            # Use the authenticate method correctly
            cust = authenticate(request, username=accno, password=passs)
            print(cust)
            if cust is not None:
                # Use login instead of login_view
                login(request, cust)
                messages.success(request, 'Account logged in')
                return redirect('home')
                # return redirect('home/')  # Redirect to the main_page or your desired URL
            else:
                
                return redirect('main_page')
                # messages.error(request, 'Username or PIN incorrect')

        return render(request, 'pages/pin.html')
    # return render (request,'pages/pin.html')




def sign_up(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('usrname')
        email = request.POST.get("email")
        usr_pass = request.POST.get("password")
        cnic = request.POST.get('cnic')
        mobile = request.POST.get("mno")
        city = request.POST.get("city")
        address = request.POST.get("address")

        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(username = username,first_name = name , last_name= name , email = email)
        user_obj.set_password(usr_pass)
        user_obj.save()
        newusr = User.objects.get(username=username)
        print(newusr)
        user_acc = AccDetail.objects.create(buser=user_obj,user_cnic=cnic,user_mobile=mobile,user_city=city,user_address=address)
        user_acc.save()
        
        getuser = AccDetail.objects.get(user_cnic=cnic)
        fromusermodel = User.objects.get(username=username)
        
        depotableupdate= Deposit.objects.create(duser=fromusermodel,usr_data=getuser,userbalance=0.0)
        depotableupdate.save()
        
        messages.success(request, f'Account Created\n Name:{name}    Username:{username}\n Password: {usr_pass}   Account Number: {getuser.user_account_number}')
        return redirect('success')
    return render(request,'pages/signUp.html')



def balance(request):
    usrdata = Deposit.objects.filter(duser=request.user)
    if request.method == "POST":
        famu = float(request.POST.get('amount'))
        tbalance,created = Deposit.objects.get_or_create(duser=request.user)
        if tbalance.userbalance >= famu:
            obj,created = Deposit.objects.get_or_create(duser=request.user)
            obj.userbalance -= famu
            obj.save()
            messages.success(request, f'Amount: {famu}  withdrawled  successfully.')
            return redirect('success')
        else:
            messages.success(request, f'Amount: {famu} cannot be withdrawled.')
            return redirect('error')
        
    context = {"usrdata":usrdata}
    return render (request,'pages/balance.html',context)


def deposit(request):
    if request.method == "POST":
        
        amount = float(request.POST.get("depo"))
        if amount <= 10000:

            obj,created = Deposit.objects.get_or_create(duser=request.user)
            obj.userbalance += amount
            obj.save()

            messages.success(request, f'Amount: {amount}  Deposited  successfully.')
                
            return redirect('success')
        else:
            messages.success(request, 'Amount is not Correct')
            return redirect('error')

    return render (request,'pages/deposit.html')




def withdrawl(request):
    if request.method == "POST":
        wamu = float(request.POST.get("wamu"))
        tbalance,created = Deposit.objects.get_or_create(duser=request.user)
        if tbalance.userbalance >= wamu:
            obj,created = Deposit.objects.get_or_create(duser=request.user)
            obj.userbalance -= wamu
            obj.save()
            # depo = Deposit.objects.create(duser=request.user,userbalance=amount)

            # depo.save()
            messages.success(request, f'Amount: {wamu}  withdrawled  successfully.')
                
            return redirect('success')
        else:
            messages.success(request, f'Amount: {wamu}  cannot be withdrawled.')
                
            return redirect('error')
        
    
    
    return render (request,'pages/withdrawl.html')
def transfer(request):
    usrdata = Deposit.objects.filter(duser=request.user)
    if request.method == "POST":
       
        amount = float(request.POST.get('amount'))
        acc = request.POST.get('acc')
        print(amount)
        accno = []
        accnumbers = AccDetail.objects.all()
        for i in accnumbers:
            accno.append(i.user_account_number)
            
        tbalance,created = Deposit.objects.get_or_create(duser=request.user)

        if tbalance.userbalance >= amount:
            
            if acc in accno:
                # print('yes')
                othusr = AccDetail.objects.get(user_account_number=acc)
                print(othusr.buser)
                current_user_deposit = Deposit.objects.get(duser=request.user)
                current_user_deposit.userbalance -= amount
                current_user_deposit.save()
            
                # Add the amount to the other user's balance
                other_user_deposit, created = Deposit.objects.get_or_create(duser=othusr.buser)
                other_user_deposit.userbalance += amount
                other_user_deposit.save()
                messages.success(request, f'Amount: {amount}  Transfered  successfully.')
                return redirect('success')
            else:
                messages.success(request, 'Account:  Number do not Match.')
                return redirect('error')
                
        else:
            messages.success(request, 'Balance Low')
            return redirect('error')

    context = {"usrdata":usrdata}
    return render (request,'pages/transfer.html',context)
def succ_ess(request):
    return render (request,'pages/success.html')

def err_or(request):
    return render (request,'pages/error.html')

def user_logout(request):
    logout(request)
    return redirect('main_page')