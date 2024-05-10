from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from med_alert_app import views
urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("", views.home, name='home'),
    path("uploadfiles/", views.upload_file, name='uploadfiles'),
    path("viewfiles/", views.view_files, name='viewfiles'),
    path("reportdetails/<int:report_id>/", views.report_details, name="report_details"),
    path('update_report_status/<int:report_id>/', views.update_report_status, name='update_report_status'),
    path("userviewfiles/", views.user_view_files, name='userviewfiles'),
    path("resolvereport/<int:report_id>/", views.admin_resolve, name='resolvereport'),
    path('reportdeleted/<int:report_id>/', views.report_deleted, name='reportdeleted'),
    path('edit_report/<int:report_id>/', views.edit_report, name='edit_report'),
    path('navbar_view_report/', views.navbar_view_report, name='navbar_view_report'),
    # path('create_report/', views.max_date_time, name='create_report'),

]