from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.listAndCreateOwners.as_view()),
    # This endpoint lists all of our Owners
    # And all of their information
    # Endpoint for creating Owners
    path('token/', obtain_auth_token),
    # This endpoint is used for obtaining auth token
    # This is our main authorizing service
    path('passtoken/', views.grabOwnerViaToken.as_view()),
    # We pass the token that we received from above here
    # This token returns the specific Owner instance
    # With the related information of Owner
    path('<int:ownerID>/', views.updateAndDeleteOwners.as_view()),
    # Receives Owner's ID and at this endpoint we can
    # Change various details of the owner
    path('<int:ownerID>/budgets/', include('budgets.urls')),
]
