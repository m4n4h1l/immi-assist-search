# in clients/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import NoticeForm

# ===================================================================
# Public-Facing View
# ===================================================================

def public_homepage(request):
    """
    This view renders the simple, public welcome page.
    It does not require a login and contains no confidential information.
    """
    return render(request, 'clients/public_homepage.html')


# ===================================================================
# Internal, Secured Views (Require Login)
# ===================================================================

@login_required
def dashboard(request):
    """
    This is the main dashboard for logged-in users.
    It fetches all Principal Applicants from the database and displays them in a list.
    """
    clients = Client.objects.filter(relationship_type='PRINCIPAL').order_by('last_name')
    return render(request, 'clients/dashboard.html', {'clients': clients})


@login_required
def client_detail(request, client_id):
    """
    This view displays a single client's complete file.
    It uses the client's ID from the URL to fetch the correct record.
    If a client with the given ID isn't found, it will show a 404 error page.
    """
    client = get_object_or_404(Client, id=client_id)
    return render(request, 'clients/client_detail.html', {'client': client})


@login_required
def add_notice(request):
    """
    This view handles the form for adding a new notice or receipt.
    If the request is GET, it displays a blank form.
    If the request is POST (meaning the form was submitted), it validates the data,
    saves the new notice, and redirects the user back to the main dashboard.
    """
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NoticeForm()
            
    return render(request, 'clients/add_notice.html', {'form': form})