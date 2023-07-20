from django.shortcuts import render, redirect
from django.contrib.auth import logout
from accounts.forms import CustomUserCreationForm
from customer.views import base_context


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    context.update(base_context(request))
    return render(request, 'signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('homepage')



