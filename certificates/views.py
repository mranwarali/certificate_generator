from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from reportlab.pdfgen import canvas
import io
from .models import Certificate

def create_certificate(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        issue_date = request.POST.get('issue_date')

        # Save the certificate data to the database
        certificate = Certificate(name=name, content=content, issue_date=issue_date)
        certificate.save()

        # Generate the PDF certificate using ReportLab
        certificate_pdf = generate_certificate_pdf(name, content, issue_date)

        # Save the PDF file and update the certificate entry with the file path
        fs = FileSystemStorage()
        filename = f"{name}_certificate.pdf"
        file_path = fs.save(filename, certificate_pdf)
        certificate.pdf_file = file_path
        certificate.save()

        return redirect('view_certificate', certificate_id=certificate.id)

    return render(request, 'create_certificate.html')

def generate_certificate_pdf(name, content, issue_date):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    # Customize the certificate layout here using ReportLab
    p.drawString(100, 800, f"Certificate Name: {name}")
    p.drawString(100, 780, f"Issue Date: {issue_date}")
    p.drawString(100, 760, "Content:")
    p.drawString(100, 740, content)
    p.save()
    buffer.seek(0)
    return buffer


# certificates/views.py

def view_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(pk=certificate_id)
        return render(request, 'view_certificate.html', {'certificate': certificate})
    except Certificate.DoesNotExist:
        return HttpResponse("Certificate not found.")

def verify_certificate(request):
    if request.method == 'POST':
        certificate_id = request.POST.get('certificate_id')
        try:
            certificate = Certificate.objects.get(pk=certificate_id)
            certificate.is_verified = True
            certificate.save()

            return redirect('view_certificate', certificate_id=certificate.id)

        except Certificate.DoesNotExist:
            return HttpResponse("Certificate not found.")

    return render(request, 'verify_certificate.html')
