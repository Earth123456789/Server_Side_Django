from django.urls import path

from Form import views

urlpatterns = [
    path("", views.get_name, name="get_name"),
    path("contact/", views.contact_us, name="contact"),
    path('thanks/', views.thanks, name='thanks'),
]