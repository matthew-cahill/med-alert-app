from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from med_alert_app.models import *
from django.contrib.auth import logout
from .forms import UploadFileForm
from .models import Document
from django.http import JsonResponse
from .models import Report
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import AnonymousUser
from .forms import ReportForm


# Create your views here.
def home(request):
    complete = 0
    if request.session.get('complete') == 1:
        complete = 1
        request.session['complete'] = 0
    if request.user.is_authenticated:
        if SiteAdmin.objects.filter(user=request.user).exists():
            return render(request, 'adminpage.html', {'user': request.user, 'complete': complete})
        else:
            return render(request, 'userpage.html', {'user': request.user, 'complete': complete})
    else:
        return render(request, 'login.html', {'complete': complete})


def logout_view(request):
    logout(request)
    return redirect('home')

def upload_file(request):
    if request.session.get('complete') == 1:
        request.session['complete'] = 0
    if request.method == 'POST':
        user = request.user if not isinstance(request.user, AnonymousUser) else None
        offenders_names = request.POST.get('offenders_names')
        location = request.POST.get('location')
        date_time_of_offense = request.POST.get('date_time_of_offense')
        offense_description = request.POST.get('offense_description')
        action_desired = request.POST.get('action_desired')
        date_time_of_offense = datetime.strptime(date_time_of_offense, '%Y-%m-%dT%H:%M')

        # Get current local date time
        current_datetime = datetime.now()
        if date_time_of_offense > current_datetime:
            # Redirect to a page indicating invalid input
            return render(request, 'invalid_input.html')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document()
            if 'file' in request.FILES:
                newdoc.upload = request.FILES['file']
            else:
                # Set default value for 'upload' field
                newdoc.upload = 'path/to/default/file.pdf'
            newdoc.save()

            # Redirect to the document list after POST
            report = Report.objects.create(offenders_names=offenders_names, location=location,
                                           date_time_of_offense=date_time_of_offense,
                                           offense_description=offense_description,
                                           action_desired=action_desired, user=user)
            report.save()
            newdoc.report = report
            newdoc.save()
            # Set session variable to indicate successful submission
            request.session['complete'] = 1
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UploadFileForm()  # An empty form

    # Render list page with the documents and the form
    return render(
        request,
        'uploadfiles.html',
        {'form': form}
    )


def view_files(request):
    if request.session.get('complete') == 1:
        request.session['complete'] = 0
    documents = Document.objects.all().order_by('-report__upload_time')
    document_details = []
    for document in documents:
        object_key = document.upload.name
        url = create_presigned_url('your-bucket-name', object_key)
        document_details.append({
            'document': document,
            'url': url
        })
    return render(request, "viewfiles.html", {'document_details': document_details, 'user': request.user})

def report_details(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    documents = Document.objects.filter(report=report)
    return render(request, "report_details.html", {'report': report, 'documents': documents})


# Helper function to view S3 files
def create_presigned_url(bucket_name, object_name, expiration=3600):
    if object_name.startswith('path/to/default/'):
        return None  # Return None for default file paths
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except NoCredentialsError:
        print("No AWS credentials found")
        return None
    return response


def update_report_status(request, report_id):
    report = Report.objects.get(pk=report_id)
    report.been_viewed = True
    report.edited = False
    report.save()
    return HttpResponseRedirect(reverse('report_details', args=(report_id,)))
    #return HttpResponse('Invalid method')


def user_view_files(request):
    if request.session.get('complete') == 1:
        request.session['complete'] = 0
    user = request.user
    documents = Document.objects.filter(report__user=user).order_by('-report__upload_time')
    presigned_urls = [create_presigned_url('med-alert-bucket', document.upload.name) for document in documents]
    return render(request, 'userviewfiles.html', {'documents': zip(documents, presigned_urls), 'user': request.user})


def admin_resolve(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    documents = Document.objects.filter(report=report)
    if request.method == 'POST':
        resolved_action = request.POST.get('resolved_action', '')
        report.resolved_action = resolved_action
        report.completed = True
        report.save()
        # Redirect to a success page or back to the resolvereport.html page
        return HttpResponseRedirect('/viewfiles')  # Change '/success/' to your desired URL

    return render(request, "resolvereport.html", {'report': report, 'documents': documents})


def report_deleted(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    # Delete the report or perform any other actions
    report.delete()
    # Redirect to the "reportdeleted" page
    return render(request, 'reportdeleted.html')


def edit_report(request, report_id):
    report = get_object_or_404(Report, pk=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.edited = True
            report.save()

            # Handle file upload if a file was provided
            if 'file' in request.FILES:
                upload = request.FILES['file']
                # Check if the report already has a document, and update it
                document, created = Document.objects.get_or_create(report=report)
                document.upload = upload
                document.save()

            return HttpResponseRedirect(reverse('report_details', args=[report_id]))
    else:
        form = ReportForm(instance=report)

    return render(request, 'edit_report.html', {'form': form})


def navbar_view_report(request):
    if SiteAdmin.objects.filter(user=request.user).exists():
        return view_files(request)
    else:
        return user_view_files(request)
