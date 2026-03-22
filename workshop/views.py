from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Booking


# =====================================
# PUBLIC HOME
# =====================================
def home(request):
    return render(request, "home.html")


# =====================================
# BOOK SERVICE (CUSTOMER)
# =====================================
def booking(request):

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        registration_number = request.POST.get("registration_number")
        vehicle_type = request.POST.get("vehicle_type")
        problem_description = request.POST.get("problem_description")

        if not name or not phone or not vehicle_type or not problem_description:
            messages.error(request, "Please fill all required fields.")
            return redirect("booking")

        booking = Booking.objects.create(
            name=name,
            phone=phone,
            registration_number=registration_number,
            vehicle_type=vehicle_type,
            problem_description=problem_description,
        )

        return render(request, "confirmation.html", {
            "booking": booking
        })

    return render(request, "booking.html")


# =====================================
# CUSTOMER TRACKING
# =====================================
def customer_login(request):

    if request.method == "POST":
        query = request.POST.get("query")

        bookings = Booking.objects.filter(
            Q(phone=query) |
            Q(registration_number__iexact=query)
        )

        if bookings.exists():
            return render(request, "customer_dashboard.html", {
                "bookings": bookings,
                "query": query
            })
        else:
            messages.error(request, "No bookings found.")
            return redirect("customer_login")

    return render(request, "customer_login.html")


# =====================================
# WORKSHOP LOGIN
# =====================================
def workshop_login(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = AuthenticationForm(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "workshop_login.html", {"form": form})


# =====================================
# WORKSHOP LOGOUT
# =====================================
def workshop_logout(request):
    logout(request)
    return redirect("workshop_login")


# =====================================
# STAFF CHECK
# =====================================
def staff_check(user):
    return user.is_staff


# =====================================
# ADMIN DASHBOARD
# =====================================
@login_required
@user_passes_test(staff_check)
def dashboard(request):

    today = timezone.now().date()

    total_revenue = Booking.objects.filter(
        status="Completed"
    ).aggregate(Sum("final_amount"))["final_amount__sum"] or 0

    today_revenue = Booking.objects.filter(
        status="Completed",
        created_at__date=today
    ).aggregate(Sum("final_amount"))["final_amount__sum"] or 0

    context = {
        "total": Booking.objects.count(),
        "pending": Booking.objects.filter(status="Pending").count(),
        "in_progress": Booking.objects.filter(status="In Progress").count(),
        "completed": Booking.objects.filter(status="Completed").count(),
        "recent_bookings": Booking.objects.order_by("-created_at")[:5],
        "total_revenue": total_revenue,
        "today_revenue": today_revenue,
        "today_total": Booking.objects.filter(created_at__date=today).count(),
        "today_completed": Booking.objects.filter(
            status="Completed",
            created_at__date=today
        ).count(),
    }

    return render(request, "dashboard.html", context)


# =====================================
# MANAGE BOOKINGS
# =====================================
@login_required
@user_passes_test(staff_check)
def manage_bookings(request):

    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")

    bookings = Booking.objects.all()

    if search_query:
        bookings = bookings.filter(
            Q(name__icontains=search_query) |
            Q(registration_number__icontains=search_query)
        )

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    bookings = bookings.order_by("-created_at")

    paginator = Paginator(bookings, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Handle Update/Delete
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        action = request.POST.get("action")

        booking = get_object_or_404(Booking, id=booking_id)

        if action == "update":
            booking.status = request.POST.get("status")
            booking.expected_completion_date = request.POST.get("expected_completion_date") or None
            booking.final_amount = request.POST.get("final_amount") or None
            booking.save()
            messages.success(request, "Booking updated successfully.")

        elif action == "delete":
            booking.delete()
            messages.success(request, "Booking deleted successfully.")

        return redirect("manage_bookings")

    return render(request, "manage_booking.html", {
        "page_obj": page_obj,
        "search_query": search_query,
        "status_filter": status_filter,
    })