from django.shortcuts import render,redirect,get_object_or_404
from accounts.models import CustomUser,Profile
from django.views import View
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .form import ProfileForm
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives


from .models import CustomUser
# Create your views here.

class log_in(View):

    def get(self, request):
        next_url = request.GET.get('next', request.POST.get('next', ''))
        context ={
            'next_url':next_url
        }

        return render(request, 'account/login.html',context)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('checkbox')
        next_url = request.POST.get('next', '')


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
            if remember_me:
                request.session.set_expiry(36000)
            else:
                request.session.set_expiry(0)
            return redirect(next_url if next_url else 'index')
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

login_required(login_url='log_in')
def profile_dashboard(request):
    return render(request,'profile/dashboard.html')

login_required(login_url='log_in')
def profile(request):
    profile,created = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile)
    form1 = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form1 = PasswordChangeForm(user=request.user,data=request.POST )
        if form1.is_valid():
            form1.save()
            return redirect('log_in')

        # profile update
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')      
        
    context ={
        'form':form,
        'form1':form1
    }
    return render(request,'profile/profile.html',context)

"""================================================================================================================================================================================================
                                                                        Account verfiy
================================================================================================================================================================================================"""

@login_required
def send_verification_email(request):

    user = request.user

    # Already verified
    if user.email_verified:
        return redirect('profile')

    # User doesn't have an email
    if not user.email:
        return redirect('profile')

    # Create verification URL
    verification_url = request.build_absolute_uri(
        reverse(
            'verify_email',
            kwargs={
                'token': user.email_verification_token
            }
        )
    )

    # Data for email templates
    context = {
        'user': user,
        'verification_url': verification_url,
    }

    # Plain-text email
    text_content = render_to_string(
        'account/verification_email.txt',
        context
    )

    # HTML email
    html_content = render_to_string(
        'account/verification_email.html',
        context
    )

    # Create email
    email = EmailMultiAlternatives(
        subject='Verify your email - SajiloCart',
        body=text_content,
        from_email='support@sajilocart.com',
        to=[user.email],
    )

    # Attach HTML version
    email.attach_alternative(
        html_content,
        'text/html'
    )

    # Send email
    email.send(fail_silently=False)

    return redirect('profile')


def verify_email(request, token):

    user = get_object_or_404(
        CustomUser,
        email_verification_token=token
    )

    user.email_verified = True

    user.save(
        update_fields=['email_verified']
    )

    return redirect('profile')