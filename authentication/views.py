from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import UserRegistrationForm, DiseasePredictionForm
from .models import CustomUser
import pandas as pd
import pickle
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Message

User = get_user_model()
def homepage(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('adminn')
        elif request.user.is_healthcareworker:
            return redirect('healthworker')
        # Add more conditions for other user types if needed
        else:
            # Redirect to a generic homepage for authenticated users
            return redirect('predict_disease')
    else:
        return redirect('login')

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            role = form.cleaned_data.get('role')  # Using .get() to avoid KeyError
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return redirect('register')

            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken.')
                return redirect('register')

            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'authentication/email_activation/activation_successful.html')
    else:
        return render(request, 'authentication/email_activation/activation_unsuccessful.html')


def healthcare_worker_view(request):
    return render(request, 'healthwoker.html')
def admin_view(request):
    return redirect('predict_disease')
def as_view (request):
     return redirect('login')

def predict_disease(request):
    if request.method == 'POST':
        form = DiseasePredictionForm(request.POST)
        if form.is_valid():
            # Extracting input values from the form
            population_density = form.cleaned_data['population_density']
            reported_cases = form.cleaned_data['reported_cases']

            # Preparing input data for prediction
            new_data = pd.DataFrame({
                'Population Density': [population_density],
                'Reported Cases': [reported_cases]
            })

            # Load the trained model
            with open('random_forest_model.pkl', 'rb') as f:
                best_model = pickle.load(f)

            # Making prediction using the best model
            prediction = best_model.predict(new_data)

            # Determining prediction message
            prediction_message = "The disease is likely to occur in this location." if prediction[0] == 1 else "The disease is not likely to occur in this location."

            return render(request, 'streamlit.html', {'prediction_message': prediction_message})
    else:
        form = DiseasePredictionForm()
    return render(request, 'hompage.html', {'form': form})

def chat(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user
        Message.objects.create(sender=sender, receiver=receiver, content=content)
        return redirect('chat', receiver_id=receiver_id)
    messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('timestamp')
    return render(request, 'streamlit.html', {'receiver': receiver, 'messages': messages})
def chat_view(request):
    # Assuming you have logic to determine the receiver user
    receiver = User.objects.get(username='heathcare')

    # Assuming you have logic to fetch messages
    messages = Message.objects.filter(receiver=receiver, sender=request.user)

    context = {
        'receiver': receiver,
        'messages': messages,
    }
    return render(request, 'streamlit.html', context)

