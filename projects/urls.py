from django.urls import path
from . import views

    


urlpatterns = [
    path('',views.projects,name="projectss"),
    path('project/<str:kd>/',views.project,name="project"),
    path('project-forms',views.projectforms,name="project-forms"),
    path('update-project/<str:pk>/',views.updateforms,name="update-project"),
    path('delete-project/<str:pk>/',views.deleteForms,name="delete-project"),
]