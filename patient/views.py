from django.shortcuts import render,redirect
from random import randint
from django.core.mail import send_mail
from . models import *
from doctor.models import *
from django.conf import settings
from django.http import Http404
from django.contrib.auth import logout as auth_logout

# Create your views here.

def Home(request):
    return render(request,'patient/home.html')

def aboutus(request):
    return render(request,'patient/aboutus.html')

def contactus(request):
    return render(request,'patient/contactus.html')

def doctors(request):
    return render(request,'patient/doctors.html')

def Booking(request):
    doctors = Doctor.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        date = request.POST['date']
        time = request.POST['time']
        message = request.POST['message']
        doctor_id = request.POST['doctor']
        doctor = Doctor.objects.get(id=doctor_id)
        appointment = Appointment(name=name, date=date, time=time, email=email, doctor=doctor, message=message, status='waiting')
        appointment.save()
        # Assuming a function to confirm appointments
        # confirm_appointment(appointment)
        return render(request, 'patient/booking.html', {'msg': 'Your appointment has been added to the list'})
    return render(request, 'patient/booking.html', {'doctors': doctors})



def List(request):
     if 'patientid' in request.session: 
        patient_id = request.session['patientid'] 
        patient = Patient.objects.get(id=patient_id) 
        patients = Appointment.objects.filter(email=patient.email)
        return render(request, 'patient/list.html', {'patients': patients}) 
     else: 
         return redirect('patient:login')
#     patients = Appointment.objects.filter(status='confirmed')
#     return render(request, 'patient/list.html', {'patients': patients})

# def confirm_appointment(appointment):
#     appointment.status = 'confirmed'
#     appointment.save()

# 

def confirm_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        raise Http404("Appointment does not exist")

    if request.method == 'POST':
        appointment.status = 'confirmed'
        appointment.save()
        message = "Appointment confirmed successfully."
        return render(request, 'patient/booking.html', {'appointment': appointment, 'message': message})

    return render(request, 'patient/booking.html', {'appointment': appointment})


def Login(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        patient_exist = Patient.objects.filter(email=email,password=password).exists()
        if patient_exist :
            patient = Patient.objects.get(email=email,password=password)
            request.session['patientid']=patient.id
            if patient.status == 'toverify':
                otp = randint(1000,9999)
                send_mail(
            'please verify your otp',
                str(otp),
                settings.EMAIL_HOST_USER,
                [patient.email]
                )
                patient.otp=otp
                patient.save()
                return redirect('patient:otp')
            else :
                return redirect('patient:booking')
        else :
                return render(request, 'patient/login.html', {'msg':'invalid email or password'})
    
    return render(request,'patient/login.html')

def Signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        patient_exist = Patient.objects.filter(email=email).exists()

        if not patient_exist:
            otp = randint(1000, 9999)
            send_mail(
                'Please verify your OTP',
                str(otp),
                settings.EMAIL_HOST_USER,
                [email]
            )
            patient = Patient(name=name, email=email, password=password, otp=otp, status='toverify')
            patient.save()
            request.session['patientid'] = patient.id
            request.session['email'] = email
            return redirect('patient:otp')
        else:
            return render(request, 'patient/signup.html', {'error': 'Email already registered.'})

    return render(request, 'patient/signup.html')

# def otp(request):
#     if request.method == 'POST':
#         otp_input = request.POST['otp']
#         c_id = request.session.get('patientid')
#         if not c_id:
#             return redirect('signup')

#         try:
#             patient = Patient.objects.get(id=c_id)
#             if otp_input == patient.otp:
#                 Patient.objects.filter(id=c_id).update(status='verified')
#                 return redirect('patient:booking')
#             else:
#                 return render(request, 'otp.html', {'msg': 'Invalid OTP'})
#         except Patient.DoesNotExist:
#             return redirect('signup')
#     return render(request, 'otp.html')

def otp(request):
    if request.method == 'POST' :
        otp = request.POST['otp']
        c_id = request.session['patientid']
        patient =Patient.objects.get(id=c_id)
        if otp==patient.otp :
            Patient.objects.filter(id=c_id).update(status='verified')
            return redirect('patient:booking')
        else :
            return render (request,'patient/otp.html' ,{'msg':'invalid otp'})
    return render(request, 'patient/otp.html')

def resend(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            patient = Patient.objects.get(email=email)
            otp = randint(1000, 9999)
            patient.otp = otp
            patient.save()
            send_mail(
                'Resend OTP',
                str(otp),
                settings.EMAIL_HOST_USER,
                [email]
            )
            return render(request, 'patient/otp.html', {'msg': 'A new OTP has been sent to your email.'})
        except Patient.DoesNotExist:
            return redirect('patient:signup')
    else:
        return redirect('signup')
    

def search_doctors(request):
    query = request.GET.get('q')
    if query:
        results = Doctor.objects.filter(name__icontains=query) | Doctor.objects.filter(specialization__icontains=query)
    else:
        results = Doctor.objects.all()
    return render(request, 'patient/doctors.html', {'doctors': results})

def logout(request):
    auth_logout(request)
    return redirect('patient:login')