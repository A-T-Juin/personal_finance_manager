from rest_framework import serializers
from . models import Receipt

FOOD_AND_DRINK = 'food'
BILLS = 'bill'
CONSUMER_GOODS = "cons"
MISC = "misc"
TYPES_OF_RECEIPTS = (
    (FOOD_AND_DRINK, "Food and Drinks"),
    (BILLS, "Bills"),
    (CONSUMER_GOODS, "Consumer Goods"),
    (MISC, "Miscellaneous"),
)

class ReceiptSerializer(serializers.ModelSerializer):
    # Serializer is used to convert from parsed data
    # To complex data and viceversa
    # Defines what fields client can work with

    receiptName = serializers.CharField(
        required = True,
        max_length = 20
    )

    receiptAmount = serializers.DecimalField(
    # Functions the same way as in our modelfield
        max_digits = 11,
        decimal_places = 2
    )

    receiptCategory = serializers.ChoiceField(TYPES_OF_RECEIPTS)

    receiptDate = serializers.DateField(
        required = False,
    )

    receiptDescription = serializers.CharField(
        max_length = 128,
        required = False,
        allow_blank = True
    )

    class Meta:
        model = Receipt
        fields = (
            'id',
            'receiptName',
            'receiptAmount',
            'receiptCategory',
            'receiptDate',
            'receiptDescription'
        )
    def save(self, *args, **kwargs):
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        print("validated_data: ", validated_data)
        if "instance" in validated_data:
            self.instance = self.update(validated_data['instance'], validated_data)
        else:
            self.instance = self.create(validated_data)
            return self.instance

    def create(self, validated_data):
        print("validated_data: ", validated_data)
        if "receiptDescription" in validated_data:
            receiptInstance = Receipt.objects.create_receipt(validated_data['receiptName'], validated_data['receiptAmount'], validated_data['receiptCategory'], validated_data['receiptDate'], validated_data['receiptDescription'], validated_data['budget'])
            return receiptInstance
        else:
            validated_data['receiptDescription'] = ""
            receiptInstance = Receipt.objects.create_receipt(validated_data['receiptName'], validated_data['receiptAmount'], validated_data['receiptCategory'], validated_data['receiptDate'], validated_data['receiptDescription'], validated_data['budget'])
            return receiptInstance

    def update(self, instance, validated_data):
        if "receiptDescription" in validated_data:
            receiptInstance = Receipt.objects.update_receipt(instance.id, validated_data['receiptName'], validated_data['receiptAmount'], validated_data['receiptCategory'], validated_data['receiptDate'], validated_data['receiptDescription'])
            return receiptInstance
        else:
            validated_data["receiptDescription"] = ""
            receiptInstance = Receipt.objects.update_receipt(instance.id, validated_data['receiptName'], validated_data['receiptAmount'], validated_data['receiptCategory'], validated_data['receiptDate'], validated_data['receiptDescription'])
            return receiptInstance
