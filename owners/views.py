from django.shortcuts import render

from rest_framework import generics, status, authentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from . models import Owner
from . serializers import OwnerSerializer

class listAndCreateOwners(GenericAPIView):
    # At this view, we'll be able to fetch and create Owners
    serializer_class = OwnerSerializer
    # The serializer associated with the view
    def get_queryset(self):
        # a helper function to grab all Owner instances
        return Owner.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
        # returns the list function
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # grabs all instances
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # returns the fetched data with a status code

    def post(self, request, format='json'):
        # the creating portion of this view
        # Passed data must be in json format
        return self.create(request)
    def create(self, request):
        serializer = OwnerSerializer(data=request.data)
        # Passes the request data to our serializer
        if serializer.is_valid():
            # If data passed to our serializer is valid
            self.perform_create(serializer)
            # then create Ownerinstance with request data
            Token.objects.get_or_create(user=(Owner.objects.get(username=serializer.data['username'])))
            # This function utilizes rest_frameworks'
            # authentication protocol to create a token for
            # Our new user
            # We will use this token in future API calls
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # Return parsed data back with a status message
            # stating that Owner instance has been successfully created
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # In the event of a failure, the failed data will be passed back
        # With an associated fail status code
    def perform_create(self, serializer):
        serializer.save()

class updateAndDeleteOwners(GenericAPIView):
    # This view will be used to handle updating/deleting
    # The specific owner instance and providing
    # owner-specific data
    serializer_class = OwnerSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def get_queryset(self):
        # Slightly different than our helper function from up
        # Above. This one grabs the particular instance where
        ownerID = self.kwargs['ownerID']
        # It matches our request data to ownerID
        return Owner.objects.get(id=ownerID)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        instance = Owner.objects.get(id=self.kwargs['ownerID'])
        # We grab the instance that we want to change
        # from the url.
        serializer = OwnerSerializer(data=request.data)
        # We pass request data into the serializer
        if serializer.is_valid():
            # And if it is valid we overwrite the instance
            # With the request data
            self.perform_update(serializer, instance)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            print("serializer.errors: ", serializer.errors)
    def perform_update(self, serializer, instance):
        serializedData = serializer
        owner = Owner.objects.edit_owner(instance, serializedData['username'], serializedData['email'])
        # This is the function that actually handles
        # The editing of the owner details
    def delete(self, request, **kwargs):
        return self.destroy(request, **kwargs)
    def destroy(self, request, **kwargs):
        instance = self.get_queryset()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def perform_destroy(self, instance):
        instance.delete()

class grabOwnerViaToken(GenericAPIView):
    # This view is used for login functionality
    # When the user logs we will pull the
    # Associated user data from token
    # Token will be passed back from server at our
    # /api/owners/token/ endpoint
    def post(self, request, *args, **kwargs):
        return self.grab_user(request.data)
    def grab_user(self, tokenString):
        # Once we get the token from the token endpoint
        # we pass that token into a get request to return the token
        # instance that matches that token
        # we then pull the associated user instance from that
        return self.serializeInstance(Token.objects.get(key=tokenString).user)
    def serializeInstance(self, userInstance):
        # We then grab the user instance and
        # Serialize it and pass back the data of the
        # Specific user
        serializer = OwnerSerializer(userInstance)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
