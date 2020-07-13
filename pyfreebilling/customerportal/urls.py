from django.urls import path

from . import views

app_name = "customerportal"
urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("customer", views.CustomerView.as_view(), name="customer_list"),
    path("customer/detail/<int:pk>/", views.CustomerDetailView.as_view(), name="customer_detail"),
    path("cdr", views.CDRView.as_view(), name="cdr"),
    path("customerendpoint/detail/<int:pk>/", views.CustomerEndpointDetailView.as_view(), name="customerendpoint_detail"),
]
