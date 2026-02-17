from django.shortcuts import  render, redirect
from django.http import HttpResponse
from appointment.forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required , permission_required
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.views.generic import TemplateView , ListView
from appointment.models import Doctor , Appointment

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
			messages.success(request, f"Registration successful. Welcome {user.username}!" )
			return redirect("dashboard")
		else:
			# Display specific errors to help the user
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f"{field}: {error}")
			messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="appointment/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			messages.info(request, f"You are now logged in as {user.username}.")
			return redirect('dashboard')
		else:
			# If authentication fails, print errors to console for debugging and show generic message to user
			print(f"Login failed. Errors: {form.errors}")
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="appointment/login.html", context={"login_form":form})


def search(request):
	if request.method == 'POST':
		timeslot = request.POST['timeSlot']
		doctorName = request.POST['doctorName']
		doc = Doctor.objects.get(name = doctorName)
		docEmail = doc.email

		userName = request.user
		current_user = User.objects.get(username = userName)
		userMail = current_user.email

		meetId = doc.appointment_set.all()[0]

		subject = 'Request for Appointment'
		message = f'Patient Name: {userName} \nPatient Email Id: {userMail} \nDoctor Name: {doctorName} \nDoctor Mail Id: {docEmail} \nTime slot {timeslot} \nMeeting Id for video call: {meetId}' 
		from_email = settings.EMAIL_HOST_USER
		recipient_list = [docEmail , userMail]
		status = send_mail(subject, message, from_email, recipient_list)
		if status == 1:
			return HttpResponse("done")
		else:
			return HttpResponse("")

	doctors = Doctor.objects.all()[:5]
	context = {
        "doctors" : doctors
    }
	return render(request , 'videocall/videocallpage.html' , context)


class BookAppointment(ListView):
	model = Doctor
	template_name = 'videocall/output.html'
	context_object_name = 'appointment'
	
	def get_queryset(self):
		obj = self.model.objects.filter(state__contains=self.request.GET['state'], 
		specialization__contains=self.request.GET['specialization'])
		return obj


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")

