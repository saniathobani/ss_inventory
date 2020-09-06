from django.forms import ModelForm

from .models import Lot, Expenses

class LotForm(ModelForm):
    class Meta:
        model = Lot
        fields = '__all__'


class ExpensesForm(ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'