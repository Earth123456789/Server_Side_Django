from django.urls import path

from employee.views import *

urlpatterns = [
    path("employee/", EmployeeView.as_view(), name="employee"),
    path("position/", PositionView.as_view(), name="position"),
    path("project/", ProjectView.as_view(), name="project"),
    path("project/edit/<int:project_id>/", EditProject.as_view(), name="edit_project"),
    path("project/<int:project_id>/", ProjectDetailView.as_view(), name="detail"),
    path("project/<int:project_id>/edit/<int:employee_id>/", EditStaff.as_view(), name="edit_staff")
]