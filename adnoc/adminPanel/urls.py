from django.urls import path
from . import views

urlpatterns = [
    path("adminLogin",views.adminLogin,name="adminLogin"),
    path("adminLogout",views.adminLogout,name="adminLogout"),
    path("rechargeReq/",views.rechargeReq,name="rechargeReq"),
    path("rechargereqVerification/<int:rid>",views.rechargereqVerification,name="rechargereqVerification"),
    path("removeRechargeRequest/<int:rid>", views.removeRechargeRequest, name="removeRechargeRequest"),
    path("removePurchaseRequest/<int:pid>", views.removePurchaseRequest, name="removePurchaseRequest"),
    path("totalRecharge/",views.totalRecharge,name="totalRecharge"),
    path("purchaseReq/",views.purchaseReq,name="purchaseReq"),
    path("prodApproved/<int:pid>",views.prodApproved,name="prodApproved"),
    path("purchaseProd/",views.purchaseProd,name="purchaseProd"),
    path("withdrawReq/",views.withdrawReq,name="withdrawReq"),
    path("approvedWithdrawRequest/<int:wid>",views.approvedWithdrawRequest,name="approvedWithdrawRequest"),
    path("removeWithdrawRequest/<int:wid>",views.removeWithdrawRequest,name="removeWithdrawRequest"),
    path("withdrawHistory/",views.withdrawHistory,name="withdrawHistory"),
    path("walletHistory/",views.walletHistory,name="walletHistory"),
    path("userDetails/",views.userDetails,name="userDetails"),
    path("userBankDetails/<int:uid>",views.userBankDetails,name="userBankDetails"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("transactionHistory/",views.transactionHistory,name="transactionHistory"),
    path("editUserDetails/<int:uid>",views.editUserDetails,name="editUserDetails"),
    path("addUpiAccount/",views.addUpiAccount,name="addUpiAccount"),
] 
