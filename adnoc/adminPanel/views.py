from django.shortcuts import render, get_object_or_404
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from adnoc_app.models import *
from .models import *
from django.core.paginator import Paginator
from adnoc_app.utils import addTransaction
from datetime import datetime
from django.db.models import F


def adminLogin(request):
    if request.method == 'POST':
        mob = request.POST.get('mob')
        passw = request.POST.get('passwd')
        try:
            user = authenticate(mobile_number= mob, password = passw)
            if user != None:
                login(request,user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid mobile number and password')
                return render(request,'adminLogin.html')

        except AdnocUser.DoesNotExist:
            messages.error(request, 'Invalid mobile number and password')
            return render(request,'adminLogin.html')
        

    return render(request,'adminLogin.html')

def adminLogout(request):
    logout(request)
    return redirect('adminLogin')



@login_required(login_url='adminLogin')
def rechargeReq(request):
    userRech = UserRecharge.objects.filter(is_valid=False).order_by("-recharge_date")
    paginator = Paginator(userRech, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,"rechargeReq.html",{"page_obj":page})


@login_required(login_url='adminLogin')
def rechargereqVerification(request, rid):
    try:
        recharge = UserRecharge.objects.get(id=rid)
        recharge.is_valid = True
        recharge.save()
        reqObj = AdnocUser.objects.get(id=recharge.user_id.id)
        reqObj.recharge_amount = reqObj.recharge_amount + recharge.recharge_amount
        reqObj.save()

        recharge.is_credited = True
        recharge.save()
        tran = transactions.objects.get(user_id=recharge.user_id.id,amount=recharge.recharge_amount)
        print(tran)
        tran.payment_status = 1
        tran.tag = "Recharge of "+str(recharge.recharge_amount)+" was successful"
        tran.save()

        return redirect('rechargeReq')
    except Exception as e:
        print(e)
        pass


@login_required(login_url='adminLogin')
def removeRechargeRequest(request, rid):
    try:
        recharge = UserRecharge.objects.get(id=rid)
        # get the traction for this and update the transaction status
        tran = transactions.objects.get(user_id=recharge.user_id.id,amount=recharge.recharge_amount)
        print(tran)
        tran.payment_status = 2
        tran.tag = "Recharge of "+str(recharge.recharge_amount)+" was failed"
        tran.save()
        recharge.delete()
        return redirect('rechargeReq')
    except Exception as e:
        print(e)
        pass
@login_required(login_url='adminLogin')
def removePurchaseRequest(request, pid):
    try:
        prod = Purchase.objects.get(id=pid)
        # get the traction for this and update the transaction status
        tran = transactions.objects.get(user_id=prod.user_id.id,amount=prod.prod_id.prod_price)
        print(tran)
        tran.payment_status = 2
        tran.tag = "Purchase of "+str(prod.prod_id.prod_name)+" was failed"
        tran.save()
        prod.delete()
        return redirect('purchaseReq')
    except Exception as e:
        print(e)
        pass



@login_required(login_url='adminLogin')
def totalRecharge(request):
    userRech = UserRecharge.objects.filter(is_valid=True).order_by("-recharge_date")
    paginator = Paginator(userRech, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,"userRecharge.html",{"page_obj":page})



@login_required(login_url='adminLogin')
def purchaseReq(request):
    prodPurchase = Purchase.objects.filter(is_approved=False).order_by("-purchase_date")
    paginator = Paginator(prodPurchase, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,"purchaseReq.html",{"page_obj":page})


@login_required(login_url='adminLogin')
def prodApproved(request, pid):
    try:
        prod = Purchase.objects.get(id=pid)
        prod.is_approved = True
        prod.save()
        # get the transaction for this and update the transaction status
        tran = transactions.objects.get(user_id=prod.user_id.id)
        print(tran)
        tran.payment_status = 1
        tran.save()
        return redirect('purchaseReq')
    except Exception as e:
        print(e)
        pass


@login_required(login_url='adminLogin')
def purchaseProd(request):
    prodPurchase = Purchase.objects.filter(is_approved=True).order_by("-purchase_date")
    paginator = Paginator(prodPurchase, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,"productPurchase.html",{"page_obj":page})



@login_required(login_url='adminLogin')
def withdrawReq(request):
    withdrawReq = WithdrawRequest.objects.filter(status="Pending").order_by("-request_date")
    paginator = Paginator(withdrawReq, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,"withdrawReq.html",{"page_obj":page})

@login_required(login_url='adminLogin')
def approvedWithdrawRequest(request, wid):
    withdrawReq = WithdrawRequest.objects.get(id=wid)
    withdrawReq.status = "success"
    withdrawReq.save()
    return redirect('withdrawReq')


@login_required(login_url='adminLogin')
def removeWithdrawRequest(request, wid):
    withdrawReq = WithdrawRequest.objects.get(id=wid)
    user = AdnocUser.objects.get(id = withdrawReq.user_id.id)
    user.withdrawable_amount = user.withdrawable_amount + withdrawReq.amount
    user.save()
    withdrawReq.status = "failed"
    withdrawReq.save()
    print(withdrawReq)
    return redirect('withdrawReq')


@login_required(login_url='adminLogin')
def withdrawHistory(request):
    withdrawReq = WithdrawRequest.objects.all()
    paginator = Paginator(withdrawReq, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "withdrawHistory.html",{"page_obj":page})


@login_required(login_url='adminLogin')
def walletHistory(request):
    product_purchase = Purchase.objects.filter(is_approved=True)
    product_list = []
    today_date = datetime.now()
    print(product_purchase)
    for purchase in product_purchase:
        try: 
            product = Product.objects.get(id = purchase.prod_id.id)
            user = AdnocUser.objects.get(id= purchase.user_id.id)
            wallet_product = WalletHistory.objects.filter(user_purchase__id = purchase.id,transaction_date__date = today_date)
            print("wallert",wallet_product)
            if not wallet_product.exists():
                print("yess")
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
                    # print("refered by ",refByUser)
                    if user.refered_by is not None:
                        refByUser=AdnocUser.objects.get(mobile_number=user.refered_by.mobile_number)
                        refByUser.withdrawable_amount=refByUser.withdrawable_amount+(product.daily_inc*0.005)
                        refByUser.save()
                        addTransaction(amount=product.daily_inc,userId=refByUser,credited=True,tag=" commision credited",status=1) 
                    addTransaction(amount=product.daily_inc,userId=user,credited=True,tag="Daily income credited for "+product.prod_name,status=1)        
        except Exception as e:
            print(e)

    
    return render(request,"wallet.html",{"status":"Successfully give daily income to user"})


@login_required(login_url='adminLogin')
def userDetails(request):
    userData = AdnocUser.objects.filter(is_superuser = False).order_by('-date_joined')
    paginator = Paginator(userData, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,"userDetails.html",{"page_obj":page})


@login_required(login_url='adminLogin')
def userBankDetails(request, uid):
    try:
        bankDetails = get_object_or_404(userBank, user_id=uid)
        data ={
            'accname' : bankDetails.accname,
            'accnum' : bankDetails.accnum,
            'ifsc' : bankDetails.ifsc,
            'acctype' : bankDetails.acctype,
            'mobnum' : bankDetails.mobnum,
        }

    except:
        data = {}
    return JsonResponse(data)



@login_required(login_url='adminLogin')
def dashboard(request):
    user = AdnocUser.objects.all()
    userRech = UserRecharge.objects.filter(is_valid=True)
    return render(request,"dashboard.html",{"user":user,"userRech":userRech})


@login_required(login_url='adminLogin')
def transactionHistory(request):
    tran = transactions.objects.all().order_by("-trans_date")
    paginator = Paginator(tran, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request,"transactionHistory.html",{"page_obj":page})


def editUserDetails(request, uid):
    user =AdnocUser.objects.get(id=uid)
    if request.method == "POST":
        uname = request.POST.get("username")
        mobnum = request.POST.get("mobnum")
        recamt = request.POST.get("recamt")
        withamt = request.POST.get("withamt")
        user.username = uname
        user.mobile_number = mobnum
        user.recharge_amount = recamt
        user.withdrawable_amount = withamt
        user.save()

        return redirect('userDetails')
    return render(request, "editUserDetails.html",{'user':user})


def addUpiAccount(request):
    upiObj=UPIAccount.objects.get()
    if request.method == "POST":
        upi=request.POST.get("upi")
        upiObj.upiId=upi
        upiObj.save()
        messages.success(request, 'UPI ID Updated')
        return redirect("addUpiAccount")
    return render(request,"manageUpi.html",{"upiObj":upiObj})
