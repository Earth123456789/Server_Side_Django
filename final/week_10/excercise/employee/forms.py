from django import forms
from .models import *
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone

class DateInput(forms.DateInput):
    input_type = 'date'

class EmployeeForm(ModelForm):
    
    Gender_Choice = (
         (None, "Select Gender"),
         ("M", "Male"),
         ("F","Female"),
         ("LGBT","LGBT")
    )

    gender = forms.ChoiceField(label="Gender", choices=Gender_Choice)

    class Meta:

        model = Employee
        fields = [
            'first_name', 
            'last_name',
            'gender',
            'birth_date',
            'hire_date',
            'salary',
            'position'
            ]
        
        widgets = {
            "birth_date" : forms.DateInput(attrs={'type': 'date'}),
            "hire_date": DateInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        hire_date = cleaned_data.get("hire_date")
        if hire_date and hire_date > timezone.now().date():
            raise ValidationError("Hire date cannot be in the future.")
        
        return cleaned_data
    
class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = [
            'name',
            'due_date',
            'start_date',
            'manager',
            'description',
            'staff'
            ]
        
        widgets = {
            "due_date" : forms.DateInput(attrs={'type': 'date'}),
            "start_date": DateInput()
        }


    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        due_date = cleaned_data.get("due_date")
        if start_date and due_date and start_date > due_date:
            raise ValidationError("start date cannote be much than due date.")
        return cleaned_data
    
    ## ใช้เพื่อทำให้ staff ใน form ไม่เป็น required (ปกติจะเป็น required คือต้องการข้อมูล staff)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].required = False
       



