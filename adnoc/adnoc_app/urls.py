from django.urls import path
from . import views

urlpatterns = [
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("forgotpass/",views.ForgotPass,name="forgotpass"),
    path("resetpass/<str:num>",views.ResetPass,name="resetpass"),
    path("otp/<str:num>",views.otp,name="otp"),
    path("logout/",views.userLogout,name="logout"),
    path("blog/",views.Blog,name="blog"),
    path("contact/",views.contactUs,name="contact"),
    path("about/",views.about,name="about"),
    path("home/",views.home,name="home"),
    path("products/",views.ViewProducts,name="viewprod"),
    path("purchase/<int:pid>",views.PurchaseProducts,name="purchaseprod"),
    path("myplans",views.myplans,name="myplan"),
    path('adnocviewsdb',views.adnocviewsdb, name="adnocviewsdb"),
    path("myTransactions",views.mytransactions,name="mytrans"),
    path("mybank",views.mybank,name="mybank"),
    path("myteam",views.myTeam,name="myteam"),
    path("recharge/",views.Recharge,name="recharge"),
    path("",views.UserProfile,name="profile"),
    path("withdrawreq/",views.withDrawReq,name="withdrawreq"),
    path("withdrawhistory/",views.withDrawHistory,name="withdrawhistory"),
    path("profitList/",views.profitList,name="profitList"),

    # path("wallethistory/",views.walletHistory,name="wallethistory"),

    # admin urls
    path("updateUserRecharge/",views.adminRechargeRequest,name="adminRechargeRequest"),

]
