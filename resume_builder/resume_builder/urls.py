from django.urls import path
from resume_app.views import EmployeeSearchView, generate_resume_pdf
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='employee_search', permanent=False)),
    path('employee-search/', EmployeeSearchView.as_view(), name='employee_search'),
    path('resume-download/<int:employee_id>/', generate_resume_pdf, name='resume_download'),
    path('admin/', admin.site.urls),
]
