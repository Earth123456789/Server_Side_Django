from django import forms
from .models import *

class EmployeeForm(forms.Form):

    class DateInput(forms.DateInput):
        input_type = 'date'
        input_formats = ('%Y-%m-%d')

    Gender_Choice = (
        (1, "Male"),
        (2,"Female"),
        (3,"LGBT")
    )


    first_name = forms.CharField(max_length=155)
    last_name = forms.CharField(max_length=155)
    gender = forms.ChoiceField(choices=Gender_Choice)
    birth_date = forms.DateField(widget=DateInput)
    hire_date = forms.DateField(widget=DateInput)
    salary = forms.DecimalField(max_digits=10, decimal_places=2)
    position = forms.ModelChoiceField(
        queryset = Position.objects.all()
    )

    