from django.urls import path
from . import views


urlpatterns = [
    path('', views.listAndCreateReceipts.as_view()),
    # We will use this endpoint to fetch, and create our receipts
    path('<int:receiptID>/', views.updateAndDeleteReceipts.as_view()),
]
