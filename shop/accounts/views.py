from django.shortcuts import render,redirect
from accounts.models import CustomUser
from django.views import View
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm



# Create your views here.

class log_in(View):

    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is not registered yet.')
            return redirect('log_in')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('index')

        messages.error(request, 'Invalid Password')
        return redirect('log_in')


class register(View):
    def get(self,request):
        return render(request,'account/register.html')

    def post(self,request):
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')

        if password == cpassword:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request,'Username already exists')
                return redirect('register')
            if CustomUser.objects.filter(email=email).exists():
                return redirect('register')
            try:
                validate_password(password)
                CustomUser.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password,phone=phone,street_address=address)
                messages.success(request,'Your account successfully registered')
                return redirect('register')

            except ValidationError as e:
                for i in e:
                    messages.error(request, i)
        else:
            messages.error(request,'Password and confirm password do not match')

                    
def log_out(request):
    logout(request)
    return redirect('index')


def password_change(request):
        # Create password change form for the current user
    form = PasswordChangeForm(user=request.user)

    # Check whether password change form was submitted
    if request.method == 'POST':

        # Create form again with submitted data
        form = PasswordChangeForm(user=request.user,data=request.POST )

        # Check whether form data is valid
        if form.is_valid():
            # Save the new password
            form.save()
            # Redirect user to login page
            return redirect('log_in')
    return render(request,'account/password_change.html')

        

