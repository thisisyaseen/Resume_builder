from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.contrib import messages
from django.db.models import Q
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from .models import Employee, Project


class EmployeeSearchView(View):
    def get(self, request):
        return render(request, 'employee_search.html')

    def post(self, request):
        search_query = request.POST.get('search_query')

        
        try:
            employee = Employee.objects.get(id=int(search_query))
        except (ValueError, Employee.DoesNotExist):
            employee = Employee.objects.filter(name__icontains=search_query).first()

        if employee:
            return redirect('resume_download', employee_id=employee.id)
        else:
            messages.error(request, 'Employee not found.')
            return redirect('employee_search')


def generate_resume_pdf(request, employee_id):
    
    employee = Employee.objects.get(id=employee_id)

    
    name = employee.name
    designation = employee.designation
    professional_summary = employee.professional_summary.split('\n')
    technical_skill_set = employee.technical_skill_set.split('\n')

    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=0,
        textColor=colors.black,
        
    )
    name_paragraph = Paragraph(f'<font size="12">Name: <b>{name}</b> </font>', name_style)

    
    designation_style = ParagraphStyle(
        'DesignationStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=0,
    )
    designation_paragraph = Paragraph(f'<font size="12">Designation: {designation}</font>', designation_style)

    content = [name_paragraph, Spacer(1, 1), designation_paragraph, Spacer(1, 12)]

    
    content.append(Paragraph('Professional Summary:', styles['Heading2']))
    for summary in professional_summary:
        content.append(Spacer(1, 3))
        content.append(Paragraph(summary.strip(), styles['Normal']))
    content.append(Spacer(1, 12))

    
    content.append(Paragraph('Technical Skill Set:', styles['Heading2']))
    skill_set_style = ParagraphStyle(
        'SkillSetStyle',
        parent=styles['Normal'],
        leftIndent=0,
        bulletIndent=0,  # Remove bulletIndent to avoid bullet points
    )
    skill_set = []
    for skill in technical_skill_set:
        skill_set.append(Paragraph(skill.strip(), skill_set_style))
    content.append(ListFlowable(skill_set, bulletType='bullet', bulletColor=colors.black, leftIndent=30))
    content.append(Spacer(1, 12))

    
    content.append(Paragraph('Professional Projects:', styles['Heading2']))

    projects = employee.project_set.all()
    for index, project in enumerate(projects, start=1):
        project_title = project.title
        technology_used = project.technology_used
        description = project.description
        role_responsibilities = project.role_responsibilities

        
        content.append(Spacer(1, 6))
        content.append(Paragraph(f'<b>Project {index}: {project_title}</b>', styles['Heading2']))
        content.append(Spacer(1, 6))
        content.append(Paragraph(f' • Technology used:    {technology_used}', styles['Normal'],))
        content.append(Spacer(1, 6))
        content.append(Paragraph(f'<b>Description:</b> <b>{project_title}</b> {description}', styles['Normal']))
        content.append(Spacer(1, 6))
        content.append(Paragraph('<b>Role and Responsibilities:</b>', styles['Normal']))

        role_style = ParagraphStyle(
            'RoleStyle',
            parent=styles['Normal'],
            leftIndent=0,
            bulletIndent=0,
            bulletFontName='Helvetica-Bold',
            bulletFontSize=8,
            bulletColor=colors.black,
        )
        roles = role_responsibilities.split('\n')
        role_list = []
        for role in roles:
            role_list.append(Paragraph(role.strip(), role_style))
        content.append(ListFlowable(role_list, bulletType='bullet', bulletColor=colors.black, leftIndent=30))
        content.append(Spacer(1, 12))

   
    doc.build(content)

    return response
