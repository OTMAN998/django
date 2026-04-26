from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.core import signing

def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create a user object to get the hashed password, but DO NOT save it to the DB
            user = form.save(commit=False)
            
            # Securely bundle the user details into a timed cryptographically signed token
            token = signing.dumps({
                'username': user.username,
                'email': form.cleaned_data['email'],
                'password': user.password,
            })
            
            # Send Email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account at CV Generator.'
            message = render_to_string('registration/activation_email.txt', {
                'user': user,
                'domain': current_site.domain,
                'token': token,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            
            return render(request, 'registration/activation_sent.html')
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {'form': form})

def activate(request, token):
    User = get_user_model()
    try:
        # Decrypt token and verify it's under 1 day old (86400 seconds)
        data = signing.loads(token, max_age=86400)
        
        # Only create the database record if the username hasn't been taken in the meantime
        if not User.objects.filter(username=data['username']).exists():
            user = User(username=data['username'], email=data['email'], password=data['password'])
            user.is_active = True
            user.save()
            return render(request, 'registration/activation_success.html')
        else:
            return render(request, 'registration/activation_invalid.html')
            
    except (signing.SignatureExpired, signing.BadSignature, KeyError):
        return render(request, 'registration/activation_invalid.html')
