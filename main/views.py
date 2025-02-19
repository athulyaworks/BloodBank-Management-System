# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import User, DonorProfile, PatientRequest, BloodInventory
from .forms import DonorSignUpForm, PatientSignUpForm, AuthoritySignUpForm, BloodRequestForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def review(request):
    return render(request,'review.html')

def contact(request):
    return render(request,'contact.html')

def login_view(request):
    return render(request, 'login.html')

def donor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_type == 'DONOR':
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('donor_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'donor_login.html')

def patient_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.user_type == 'PATIENT':
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'patient_login.html')

def authority_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.user_type == 'AUTHORITY':
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('authority_dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'authority_login.html')


# Blood inventory management
@login_required
def blood_inventory(request):
    inventory = BloodInventory.objects.all()
    return render(request, 'blood_inventory.html', {'inventory': inventory})

@login_required
def update_inventory(request):
    if request.user.user_type != 'AUTHORITY':
        return redirect('login')
    if request.method == 'POST':
        blood_type = request.POST.get('blood_type')
        units = int(request.POST.get('units'))
        inventory, created = BloodInventory.objects.get_or_create(blood_type=blood_type)
        inventory.units_available += units
        inventory.save()
    return redirect('blood_inventory')

# Profile management
@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Add profile update logic here
        return redirect('donor_dashboard' if request.user.user_type == 'DONOR' else 'patient_dashboard')
    return render(request, 'edit_profile.html')

# Blood request management
@login_required
def request_blood(request):
    if request.user.user_type != 'PATIENT':
        return redirect('login')
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.user = request.user
            blood_request.save()
            return redirect('patient_dashboard')
    else:
        form = BloodRequestForm()
    return render(request, 'request_blood.html', {'form': form})

# History views
@login_required
def donation_history(request):
    if request.user.user_type != 'DONOR':
        return redirect('login')
    donations = DonorProfile.objects.filter(user=request.user)
    return render(request, 'donation_history.html', {'donations': donations})

@login_required
def request_history(request):
    if request.user.user_type != 'PATIENT':
        return redirect('login')
    requests = PatientRequest.objects.filter(user=request.user)
    return render(request, 'request_history.html', {'requests': requests})

# Search functionality
def search_blood(request):
    query = request.GET.get('query')
    results = BloodInventory.objects.all()
    if query:
        results = results.filter(blood_type__icontains=query)
    return render(request, 'search_blood.html', {'results': results})

class DonorSignUpView(CreateView):
    model = User
    form_class = DonorSignUpForm
    template_name = 'donor_signup.html'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful! Please login to continue.')
        # login(self.request, user)
        return redirect('donor_login')

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'patient_signup.html'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful! Please login to continue.')
        # login(self.request, user)
        return redirect('patient_login')

class AuthoritySignUpView(CreateView):
    model = User
    form_class = AuthoritySignUpForm
    template_name = 'authority_signup.html'

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Registration successful! Please login to continue.')
        # login(self.request, user)
        return redirect('authority_dashboard')

@login_required
def donor_dashboard(request):
    try:
        donor_profile = DonorProfile.objects.get(user=request.user)
        if request.user.user_type != 'DONOR':
            messages.error(request, 'You are not authorized to access this page')
            return redirect('login')
            
        context = {
            'donor_profile': donor_profile,
            'user': request.user
        }
        return render(request, 'donor_dashboard.html', context)
    except DonorProfile.DoesNotExist:
        messages.error(request, 'Donor profile not found')
        return redirect('login')

@login_required
def patient_dashboard(request):
    # Check if user is authenticated and is a patient
    if not request.user.is_authenticated or request.user.user_type != 'PATIENT':
        messages.error(request, 'You must be logged in as a patient to access this page.')
        return redirect('patient_login')
    
    # Get patient's blood requests
    requests = PatientRequest.objects.filter(user=request.user)
    
    context = {
        'requests': requests,
        'form': BloodRequestForm(),
        'user': request.user  # Explicitly pass user to template
    }
    
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.user = request.user
            blood_request.save()
            messages.success(request, 'Blood request submitted successfully!')
            return redirect('patient_dashboard')
        else:
            messages.error(request, 'Please correct the errors in your form.')
            context['form'] = form
    
    return render(request, 'patient_dashboard.html', context)

@login_required
def authority_dashboard(request):
    if request.user.user_type != 'AUTHORITY':
        return redirect('authority_login')
    context = {
        'donor_requests': DonorProfile.objects.filter(status='PENDING'),
        'patient_requests': PatientRequest.objects.filter(status='PENDING'),
        'blood_inventory': BloodInventory.objects.all(),
        'all_donors': DonorProfile.objects.all(),
        'all_patients': User.objects.filter(user_type='PATIENT')
    }
    return render(request, 'authority_dashboard.html', context)

@login_required
def approve_donor(request, donor_id):
    if request.user.user_type != 'AUTHORITY':
        return redirect('login')
    
    donor_profile = DonorProfile.objects.get(id=donor_id)
    if donor_profile.status == 'PENDING':
        donor_profile.status = 'APPROVED'
        donor_profile.save()
        
        # Update blood inventory
        inventory, created = BloodInventory.objects.get_or_create(
            blood_type=donor_profile.blood_type
        )
        inventory.units_available += donor_profile.blood_units
        inventory.save()
    
    return redirect('authority_dashboard')

@login_required
def approve_patient_request(request, request_id):
    if request.user.user_type != 'AUTHORITY':
        return redirect('login')
    
    patient_request = PatientRequest.objects.get(id=request_id)

    # Fetch or create the BloodInventory entry
    inventory, created = BloodInventory.objects.get_or_create(
        blood_type=patient_request.blood_type,
        defaults={'units_available': 0}  # Default to 0 if new entry
    )

    if patient_request.status == 'PENDING' and inventory.units_available >= patient_request.units_required:
        patient_request.status = 'APPROVED'
        patient_request.save()

        # Deduct blood units
        inventory.units_available -= patient_request.units_required
        inventory.save()
    else:
        messages.error(request, "Not enough blood units available.")
    
    return redirect('authority_dashboard')



@csrf_exempt  # Temporarily disable CSRF protection for testing (not recommended for production)
def logout_view(request):
    if request.method == "POST":  # Ensure only POST requests are allowed
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('home')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('home')  # Redirect to home instead of showing an error