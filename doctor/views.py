from django.shortcuts import render,redirect
from . models import *
from patient.models import *
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def PatientList(request):
    doc=Doctor.objects.all()
    doctorid = request.session.get('docid')
    
    appointments = Appointment.objects.filter(doctor=doctorid)
    
        
    return render(request,'doctor/patientlist.html',{'appointments':appointments})



def DoctorLogin(request):
    if request.method=='POST':
        name=request.POST['name']
        password=request.POST['password']
        try:
            doctor = Doctor.objects.get(name=name, password=password)
            request.session['docid'] =doctor.id # Store doctor's id in session
            return redirect('doctor:patientlist')
        except Doctor.DoesNotExist:
            return render(request, 'doctor/doctorlogin.html', {'msg': 'Invalid credentials'})
    return render(request,'doctor/doctorlogin.html')
def update_status_of_patient(request,patient_id):
    appointment=Appointment.objects.get(id=patient_id)
    email=appointment.email
    appointment.status='confirmed'
    appointment.save()
    send_mail(
                'Appointment Confirmed',
                'Dear Sir/Madam  your booking is confirmed',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
                )
    return redirect('doctor:patientlist')
def remove_apponitment(request,appointment_id):
    Appointment.objects.get(id=appointment_id).delete()
    return redirect('doctor:patientlist')