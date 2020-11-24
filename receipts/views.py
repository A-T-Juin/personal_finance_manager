from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from budgets.models import Budget
from . models import Receipt
from . serializers import ReceiptSerializer

class listAndCreateReceipts(GenericAPIView):
    serializer_class = ReceiptSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    def get_queryset(self):
        budgetID = self.kwargs['budgetID']
        return Receipt.objects.filter(budget__id=budgetID)
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
        # return self.list(request, *args, **kwargs)
    def post(self, request, format='json', **kwargs):
        print("request.data: ", request.data)
        serializer = ReceiptSerializer(data=request.data)
        print("serializer: ", serializer)
        if serializer.is_valid():
            budgetID = self.kwargs['budgetID']
            BudgetInstance = Budget.objects.get(id=budgetID).title
            receipt = serializer.save(budget=BudgetInstance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class updateAndDeleteReceipts(GenericAPIView):
    serializer_class = ReceiptSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    def get(self, request, *args, **kwargs):
        print("self.kwargs: ", self.kwargs)
        return self.list(request, *args, **kwargs)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
    def get_queryset(self):
        receiptID = self.kwargs['receiptID']
        return Receipt.objects.get(id=receiptID)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = ReceiptSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer, instance=instance)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    def perform_update(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        receiptIdentifier = self.kwargs['receiptID']
        instance = Receipt.objects.get(id=receiptIdentifier)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def perform_destroy(self, instance):
        instance.delete()
