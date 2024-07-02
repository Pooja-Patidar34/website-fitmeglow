

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,  AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from products.models import Order

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the user before logging in
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})

@login_required
def dashboard_view(request):
    # Retrieve recent orders for the logged-in user
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]  # Limit to the 5 most recent orders
    
    context = {
        'recent_orders': recent_orders,
    }
    return render(request, 'account/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to the next URL if available, or to a default URL
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})

