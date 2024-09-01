from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.db.models import *
from .forms import *

class EmployeeView(View):
    def get(self, request):
        employees = Employee.objects.order_by('-hire_date')
        employee_count = Employee.objects.count()
        context = {
            'employees' : employees,
            'employee_count' : employee_count
        }
        return render(request, "employee.html", context)

class PositionView(View):
    def get(self, request):
        positions = Position.objects.annotate( count = Count('employee') ).order_by('id')
        context = {
            'positions' : positions
        }
        return render(request, "position.html", context)

class ProjectView(View):
    def get(self, request):
        projects = Project.objects.order_by('id')
        context = {
            'projects' : projects
        }
        return render(request, "project.html", context)
    
   

class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects.get(pk = project_id)
        staffs = project.staff.all()
        context = {
            'project' : project,
            'staffs' : staffs
        }
        return render(request, "project_detail.html", context)

class EditProject(View):

    def delete(self, request, project_id):
        project = Project.objects.get(pk = project_id)
        project.delete()
        return JsonResponse({'status':'delete_susecss'}, status=200)
    
class EditStaff(View):
    
    def put(self, request, project_id, employee_id):
        project = Project.objects.get(pk = project_id)
        employee = Employee.objects.get(pk = employee_id)
        project.staff.add(employee)
        return JsonResponse({'status':'add_susecss'}, status=200)
    
    def delete(self, request, project_id, employee_id):
        project = Project.objects.get(pk = project_id)
        employee = Employee.objects.get(pk = employee_id)
        project.staff.remove(employee)
        return JsonResponse({'status':'delete_susecss'}, status=200)


class EditEmployeeView(View):

    def get(self, request):
        form = EmployeeForm()
        return render(request, "employee_form.html", {"form": form})
     
    def post(self, request):
        form = EmployeeForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            gender = form.cleaned_data["gender"]
            birth_date = form.cleaned_data["birth_date"]
            hire_date = form.cleaned_data["hire_date"]
            salary = form.cleaned_data["salary"]
            position =  form.cleaned_data["position"]

            print("First_name: ", first_name)
            print("Last_name: ", last_name)
            print("Gender: ", gender)
            print("Birth_date: ", birth_date)
            print("Hire_date: ", hire_date)
            print("Salary: ", salary)
            print("Position: ", position)

            Employee.objects.create(
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                birth_date=birth_date,
                hire_date=hire_date,
                salary=salary,
                position=position
            )
            return redirect("employee")   
             
        return render(request, "employee.html", {"form": form})
            
        
