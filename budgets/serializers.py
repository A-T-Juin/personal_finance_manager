from rest_framework import serializers
from . models import Budget
from receipts.serializers import ReceiptSerializer

class BudgetSerializer(serializers.ModelSerializer):
    # Serializer is used to convert from parsed data
    # To complex data and viceversa
    # Defines what fields client can work with

    title = serializers.CharField(
        required = True,
        max_length = 20
    )

    description = serializers.CharField(
        max_length = 128,
        required = False
    )

    startDate = serializers.DateField(
        required = True
    )

    endDate = serializers.DateField(
        required = True
    )

    budgetGoal = serializers.DecimalField(
    # Functions the same way as in our modelfield
        max_digits = 11,
        decimal_places = 2,
        required = True
    )


    receipts = ReceiptSerializer(many=True, read_only=False, required=False)
    # Our serializer field that we indicate as an array

    class Meta:
        model = Budget
        fields = (
            'id',
            'title',
            'description',
            'startDate',
            'endDate',
            'budgetGoal',
            'receipts'
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
        # The if-else clause in create/update is used to
        # allow empty descriptions, as they are not required
        if "description" in validated_data:
            BudgetInstance = Budget.objects.create_budget(validated_data['title'], validated_data['description'], validated_data['startDate'], validated_data['endDate'], validated_data['budgetGoal'], validated_data['owner'])
            return BudgetInstance
        else:
            validated_data['description'] = ""
            BudgetInstance = Budget.objects.create_budget(validated_data['title'], validated_data['description'], validated_data['startDate'], validated_data['endDate'], validated_data['budgetGoal'], validated_data['owner'])
            return BudgetInstance

    def update(self, instance, validated_data):
        if "description" in validated_data:
            BudgetInstance = Budget.objects.update_budget(instance.id, validated_data['title'], validated_data['description'], validated_data['endDate'], validated_data['budgetGoal'])
            return BudgetInstance
        else:
            validated_data['description'] = ""
            BudgetInstance = Budget.objects.update_budget(instance.id, validated_data['title'], validated_data['description'], validated_data['endDate'], validated_data['budgetGoal'])
            return BudgetInstance
