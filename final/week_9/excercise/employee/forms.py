from django import forms
from .models import *

class EmployeeForm(forms.Form):

    class DateInput(forms.DateInput):
        input_type = 'date'
        input_formats = ('%Y-%m-%d')

    Gender_Choice = (
        (None, "Select Gender"),
        (1, "Male"),
        (2,"Female"),
        (3,"LGBT")
    )


    first_name = forms.CharField(label="First_Name" , max_length=155)
    last_name = forms.CharField(label="Last_Name", max_length=155)
    gender = forms.ChoiceField(label="Gender", choices=Gender_Choice)
    birth_date = forms.DateField(label="Birth_Date", widget=DateInput)
    hire_date = forms.DateField(label="Hire_Date",  widget=forms.DateInput(attrs={'type': 'date'}))
    salary = forms.DecimalField(label="Salary", max_digits=10, decimal_places=2, initial=0)
    position = forms.ModelChoiceField(
        label="Position",
        queryset = Position.objects.all()
    )

    