from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-session/', views.add_session, name='add_session'),
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/edit/<int:session_id>/', views.edit_session, name='edit_session'),
    path('sessions/delete/<int:session_id>/', views.delete_session, name='delete_session'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('predict/', views.predict_productivity, name='predict'),
]