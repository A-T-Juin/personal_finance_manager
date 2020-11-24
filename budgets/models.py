from django.db import models
from owners.models import Owner

class BudgetManager(models.Manager):
    def create_budget(self, title, description, startDate, endDate, budgetGoal, ownerName,**extra_fields):
        ownerObject = Owner.objects.get(username=ownerName)
        # we inform our model that the owner field will later be
        # an owner instance
        if not title:
            raise ValueError("Budget must have a title")
        if not startDate:
            raise ValueError("Budget must have a start date")
        if not endDate:
            raise ValueError("Budget must have an end date")
        if not budgetGoal:
            raise ValueError("Budget must have a budget goal!")
        # These are a list of errors we will raise if these conditions
        # are not met

        Budget = self.model(
            title = title,
            description = description,
            startDate = startDate,
            endDate = endDate,
            owner = ownerObject,
            budgetGoal = budgetGoal,
            **extra_fields
        )
        # The fields that our Model will have

        Budget.save()
        return Budget

    def update_budget(self, id, title, description, endDate, budgetGoal):
        BudgetInstance = Budget.objects.get(id=id)
        BudgetInstance.title = title
        BudgetInstance.description = description
        # We do not include the startDate argument since
        # The startDate argument will be read only
        BudgetInstance.endDate = endDate
        BudgetInstance.budgetGoal = budgetGoal
        BudgetInstance.save()
        return BudgetInstance

class Budget(models.Model):
    owner = models.ForeignKey(Owner, related_name="budgets", on_delete=models.CASCADE)
    # This is indicates that the Owner instance is a foreignKey
    # Relationship 1:N
    title = models.CharField(
        max_length=20,
        blank=False
    )
    description = models.CharField(
        max_length=128,
        blank=True
    )
    startDate = models.DateField(
        blank=False
    )
    # The auto_now makes it so that the date is automatically
    # Generated
    endDate = models.DateField(
        blank=False
    )
    budgetGoal = models.DecimalField(
        max_digits = 11,
        decimal_places = 2,
        blank=False
    )
    objects = BudgetManager()

    def __unicode__(self):
        return '%s: %s' %(self.title, self.description)
