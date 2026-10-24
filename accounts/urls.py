from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path("signup/", views.signup, name="signup"),

    path("login/", views.login_view, name="login"),

    path("logout/", views.logout_view, name="logout"),

    path(
        "customer/dashboard/",
        views.customer_dashboard,
        name="customer_dashboard",
    ),

    path(
        "mechanic/dashboard/",
        views.mechanic_dashboard,
        name="mechanic_dashboard",
    ),

]