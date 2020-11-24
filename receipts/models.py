from django.db import models
from budgets.models import Budget

class ReceiptManager(models.Manager):
    # Similar to OwnerManager, this handles create/edit/delete
    # for Receipt objects in our database
    def create_receipt(self, receiptName, receiptAmount, receiptCategory, receiptDate, receiptDescription, budgetTitle, **extra_fields):
        BudgetObject = Budget.objects.get(title=budgetTitle)
        # This refers to our foreignkey in the database
        if not receiptName:
            raise ValueError("Receipts must have a name")
        if receiptCategory not in ("misc", "bill", "cons", "food"):
            raise ValueError("Receipts must belong to a valid category of :")

        receipt = self.model(
            receiptName = receiptName,
            # Receipts should have a name
            receiptAmount = receiptAmount,
            # Every receipt should have an associated amount
            receiptCategory = receiptCategory,
            # Every receipt will belong to a category of expenditure
            receiptDate = receiptDate,
            # Used for our chart that we will graph
            receiptDescription = receiptDescription,
            # Perhaps a description
            budget = BudgetObject,
            # This refers to our foreignkey in the database
            **extra_fields
        )

        receipt.save()
        return receipt

    def update_receipt(self, id, receiptName, receiptAmount, receiptCategory, receiptDate, receiptDescription):
        if not receiptName:
            raise ValueError("Receipts must have a name")
        if receiptCategory not in ("misc", "bill", "cons", "food"):
            raise ValueError("Receipts must belong to a valid category of :")

        # This function will edit our receipts
        # By replacing an original instance with validated
        # request data
        receiptInstance = Receipt.objects.get(id=id)
        # Grab the specific instance in DB
        receiptInstance.receiptName = receiptName
        receiptInstance.receiptAmount = receiptAmount
        receiptInstance.receiptCategory = receiptCategory
        receiptInstance.receiptDate = receiptDate
        receiptInstance.receiptDescription = receiptDescription
        # Overwrite each portion except ID.
        receiptInstance.save()
        return receiptInstance

class Receipt(models.Model):
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


    budget = models.ForeignKey(Budget, related_name="receipts", on_delete=models.CASCADE)
    # Has a foreignkey relationship to our
    # Owner model
    receiptName = models.CharField(
        max_length=20,
        blank=False
    )
    receiptAmount = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        blank=False
    )

    receiptCategory = models.CharField(
        max_length=4,
        choices=TYPES_OF_RECEIPTS,
        blank=False
    )

    receiptDate = models.DateField(
        blank=True
    )
    # The second kwarg here denotes the required
    # Amount of decimal places
    # First kwarg denotes max total digits
    # Arbitrary, can be more than 11... but a million dollar
    # Receipt seems more than enough
    receiptDescription = models.CharField(
        max_length=128,
        blank=True
    )
    # A short description of owner's receipt
    objects = ReceiptManager()

    def __unicode__(self):
        return '%s: %s' %(self.receiptName, self.receiptDescription)
