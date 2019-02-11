from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('init/', views.init, name='init'),
    path('handlePostResult/', views.handle_post_result, name='handlePostResult'),
    path('checkStatus/<slug:payment_reference_number>', views.check_status, name='checkStatus'),
    path('reversePayment/', views.reverse_payment, name='reversePayment'),
    path('refundPayment/', views.refund_payment, name='refundPayment'),
]