from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import *
from django.db.models import *
from .forms import *
from django.db import transaction

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
    
   
class EditProjectView(View):

    def get(self, request):
        # สร้าง form เปล่าๆ แล้ว render
        form = ProjectForm()
        return render(request, "project_form.html", {"form": form})
    
    def post(self, request):
        # รับ post เพื่อแปลงข้อมูลให้เป็น form
        form = ProjectForm(request.POST)
        # แปลงข้อมูลที่ได้รับจาก post

        if form.is_valid():
            form.save()
            return redirect("project")  
         
        print(form.errors)
        return render(request, "project_form.html", {"form": form})
    
    def delete(self, request, project_id):
        project = Project.objects.get(pk = project_id)
        project.delete()
        return JsonResponse({'status':'delete_susecss'}, status=200)
    
class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects.get(pk = project_id)
        form = ProjectForm(instance=project)
        staffs = project.staff.all()
        context = {
            'project' : project,
            'form': form,
            'staffs' : staffs
        }
        return render(request, "project_detail.html", context)
    
    def post(self, request, project_id):
        project = Project.objects.get(pk = project_id)
        # for updating article instance set instance=article
        form = ProjectForm(request.POST, instance=project)
        # save if valid                                   
        if form.is_valid():                                                                   
            form.save()                                                                          
            return redirect("detail", project_id=project.id)
    
        staffs = project.staff.all()
        context = {
            'project': project,
            'form': form,
            'staffs': staffs
        }
        return render(request, "project_detail.html", context)
    
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
        # สร้าง form เปล่าๆ แล้ว render
        form = EmployeeForm()
        return render(request, "employee_form.html", {"form": form})
    
    @transaction.atomic
    def post(self, request):
        # รับ post เพื่อแปลงข้อมูลให้เป็น form
        form = EmployeeForm(request.POST)
        # แปลงข้อมูลที่ได้รับจาก post
        if form.is_valid():
            employee = form.save()
            EmployeeAddress.objects.create(
                employee=employee,
                location=form.cleaned_data['location'],
                district=form.cleaned_data['district'],
                province=form.cleaned_data['province'],
                postal_code=form.cleaned_data['postal_code']
            )
            return redirect("employee")   
             
        return render(request, "employee_form.html", {"form": form})

            
        
