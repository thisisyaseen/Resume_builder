from django.contrib import admin
from .models import Employee, Project

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1

class EmployeeAdmin(admin.ModelAdmin):
    inlines = [ProjectInline]
    list_display = ['name', 'designation']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_employee_name', 'technology_used']

    def get_employee_name(self, obj):
        return obj.employee.name

    get_employee_name.short_description = 'Employee Name'
    get_employee_name.admin_order_field = 'employee__name'

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Project, ProjectAdmin)
