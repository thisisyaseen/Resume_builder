from django.db import models

class Employee(models.Model):
    name = models.TextField()
    designation = models.TextField()
    professional_summary = models.TextField()
    technical_skill_set = models.TextField()


class Project(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    technology_used = models.CharField(max_length=100)
    description = models.TextField()
    role_responsibilities = models.TextField()

class EmployeeProject(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
