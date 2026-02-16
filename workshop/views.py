from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Booking


# HOME VIEW
def home(request):
    booking_id = request.session.pop('latest_booking_id', None)
    return render(request, 'home.html', {'booking_id': booking_id})


# BOOKING VIEW
def booking(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        vehicle_type = request.POST.get('vehicle_type')
        problem_description = request.POST.get('problem_description')

        booking = Booking.objects.create(
            name=name,
            phone=phone,
            vehicle_type=vehicle_type,
            problem_description=problem_description
        )

        request.session['latest_booking_id'] = str(booking.booking_id)

        return redirect('home')

    return render(request, 'booking.html')


# ADMIN MANAGE BOOKINGS
@login_required
def manage_bookings(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        status = request.POST.get("status")

        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = status
        booking.save()

        return redirect("manage_bookings")

    bookings = Booking.objects.all().order_by("-booking_date")
    return render(request, "manage_booking.html", {"bookings": bookings})



@login_required
def dashboard(request):
    total = Booking.objects.count()
    pending = Booking.objects.filter(status='Pending').count()
    in_progress = Booking.objects.filter(status='In Progress').count()
    completed = Booking.objects.filter(status='Completed').count()

    context = {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'completed': completed,
    }

    return render(request, 'dashboard.html', context)


@login_required
def manage_bookings(request):
    # SEARCH
    search_query = request.GET.get("search", "")
    
    # FILTER
    status_filter = request.GET.get("status", "")

    bookings = Booking.objects.all().order_by("-booking_date")

    if search_query:
        bookings = bookings.filter(name__icontains=search_query)

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    # UPDATE STATUS
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")

        booking = get_object_or_404(Booking, id=booking_id)

        if action == "update":
            booking.status = request.POST.get("status")
            booking.save()

        elif action == "delete":
            booking.delete()

        return redirect("manage_bookings")

    context = {
        "bookings": bookings,
        "search_query": search_query,
        "status_filter": status_filter,
    }

    return render(request, "manage_booking.html", context)

def customer_login(request):
    if request.method == "POST":
        phone = request.POST.get("phone")

        bookings = Booking.objects.filter(phone=phone)

        if bookings.exists():
            return render(request, "customer_dashboard.html", {
                "bookings": bookings,
                "phone": phone
            })
        else:
            return render(request, "customer_login.html", {
                "error": "No bookings found for this number."
            })

    return render(request, "customer_login.html")

