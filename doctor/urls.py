from django .urls import path
from . import views
app_name='doctor'
urlpatterns=[
    path('doctorlogin/',views.DoctorLogin,name='doctorlogin'),
    path('patientlist/',views.PatientList,name='patientlist'),
    path('update_status_of_patient/<int:patient_id>',views.update_status_of_patient,name='update_status_of_patient'),
    path('remove_apponitment/<int:appointment_id>',views.remove_apponitment,name='remove_apponitment'),
]
