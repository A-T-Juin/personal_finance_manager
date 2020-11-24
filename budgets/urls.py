from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.listAndCreateBudgets.as_view()),
    # This endpoint will allow us to create and list our budgets
    path('<int:budgetID>/', views.updateAndDeleteBudgets.as_view()),
    # This endpoint will allow us to edit and delete our budgets
    path('<int:budgetID>/receipts/', include('receipts.urls')),
]
