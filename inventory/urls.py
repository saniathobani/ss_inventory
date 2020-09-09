from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name= 'home'),
    path('login/', views.loginPage, name= 'login'),
    path('logout', views.logoutUser, name='logout'),
    path('expenses/', views.expenses, name= 'expenses'),
    path('create_expenses/', views.createExpenses, name= 'create_expenses'),
    path('update_expenses/<int:pk>/', views.updateExpenses, name= 'update_expenses'),
    path('delete_expenses/<int:pk>/', views.deleteExpenses, name= 'delete_expenses'),
    path('e_search/', views.eSearch, name= 'e_search'),
    path('search/', views.search, name= 'search'),
    path('create_lot/', views.createLot, name= 'create_lot'),
    path('update_lot/<str:pk>/', views.updateLot, name= 'update_lot'),
    path('delete_lot/<str:pk>/', views.deleteLot, name= 'delete_lot'),
   
]