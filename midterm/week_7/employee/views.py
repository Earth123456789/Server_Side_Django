from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import *
from django.db.models import *


class EmployeeView(View):

    def get(self, request):
        employees = Employee.objects.order_by("id")
        employee_count = Employee.objects.order_by("id").count()
        context = {"employees": employees,
                   "employee_count": employee_count }
        return render(request, "employee.html", context)

class PositionView(View):

    def get(self, request):
        positions = Position.objects.annotate( count = Count('employee') ).order_by('id')
        context = {"positions": positions }
        return render(request, "position.html", context)

class ProjectView(View):

    def get(self, request):
        projects = Project.objects.order_by('id')
        context = {"projects": projects }
        return render(request, "project.html", context)

class ProjectDetailView(View):

    def get(self, request, project_id):
        project = Project.objects.get(id = project_id)
        staffs = project.staff.all()
        context = {
            "project": project,
            "staffs": staffs,
            "start_date" : project.start_date.strftime("%Y-%m-%d"),
            "due_date" : project.due_date.strftime("%Y-%m-%d")    
                }
        return render(request, "project_detail.html", context)
    
    def delete(self, request, project_id):
        project = Project.objects.get(id = project_id)
        project.delete()
        return JsonResponse({'status':'delete_susecss'}, status=200)

class EditStaff(View):
    def put(self, request, project_id, employee_id):
        project = Project.objects.get(id = project_id)
        employee = Employee.objects.get(id = employee_id)
        project.staff.add(employee)
        return JsonResponse({'status':'add_susecss'}, status=200)
    
    def delete(self, request, project_id, employee_id):
        project = Project.objects.get(id = project_id)
        employee = Employee.objects.get(id = employee_id)
        project.staff.remove(employee)
        return JsonResponse({'status':'remove_susecss'}, status=200)

