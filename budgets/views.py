from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from owners.models import Owner
from . models import Budget
from . serializers import BudgetSerializer

class listAndCreateBudgets(GenericAPIView):
    # This view will be used to create and list our budgets

    serializer_class = BudgetSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        ownerID = self.kwargs['ownerID']
        return Budget.objects.filter(owner__id=ownerID)
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def get(self, request, *args, **kwargs):
        content = {
            'status': 'request was permitted'
        }
        return self.list(request, content, *args, **kwargs)
    def post(self, request, ownerID, format='json'):
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            ownerID = self.kwargs['ownerID']
            budgetOwner = Owner.objects.get(id=ownerID).username
            budget = serializer.save(owner=budgetOwner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class updateAndDeleteBudgets(GenericAPIView):
    serializer_class = BudgetSerializer
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
    def get_queryset(self):
        ownerID = self.kwargs['ownerID']
        budgetID = self.kwargs['budgetID']
        return Budget.objects.filter(owner__id=ownerID).get(id=budgetID)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = BudgetSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer, instance=instance)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    def perform_update(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        budgetID = self.kwargs['budgetID']
        instance = Budget.objects.get(id=budgetID)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def perform_destroy(self, instance):
        instance.delete()
