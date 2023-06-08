from django.urls import path
from .views import DepartmentListCreateView,DepartmentRUDView,PersonnelListCreateView,PersonnelRUDView,DepartmentPersonnelView 

urlpatterns =[
    path('departments/', DepartmentListCreateView.as_view()),
    path('departments/<int:pk>/', DepartmentRUDView.as_view()),
    path('personnel/', PersonnelListCreateView.as_view()),
    path('personnel/<int:pk>/', PersonnelRUDView.as_view()),
    path('departments/<str:department>/', DepartmentPersonnelView.as_view()),

]