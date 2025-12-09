from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from .models import Cow, Staff, Task, Attendance, PerformanceLog, MilkProduction, MilkSale, MilkBuyer
from .models import Vaccination, Deworming, Disease, Treatment, Feed, FeedingPlan, FeedPurchase
from django.contrib import messages
from django.core import serializers
import json
from django.utils import timezone
from django.utils.dateparse import parse_date

User = get_user_model()

#def home(request):
#    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')
    #form = SignupForm()
    #return render(request, 'signup.html', {'form': form})

@csrf_exempt
def ajax_signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        location = request.POST.get("location")
        role = request.POST.get("role")  # <-- new field

        # 1. Password match check
        if password != confirm_password:
            return JsonResponse({"status": "error", "message": "Passwords do not match"}, status=400)

        # 2. Email exists check
        if User.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already registered"}, status=400)

        # 3. Create user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            location=location,
            role=role,  # <-- save role
            password=make_password(password),
        )

        return JsonResponse({"status": "success", "message": "Account created successfully"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def ajax_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.role == "Admin":
                return JsonResponse({"status": "success", "redirect_url": "/adminpanel/"})
            else:
                return JsonResponse({"status": "success", "redirect_url": "/userpanel/"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid email or password"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


    
#def login(request):
 #   return render(request, 'login.html')

def adminpanel_view(request):
    return render(request, 'cowdashboard.html')

def userpanel_view(request):
    return render(request, 'userpanel.html')

def view_cow(request):
    return render(request, "cowregister.html")

#def add_cow(request):
#    return render(request, "cowregister.html")

@csrf_exempt
def add_cow(request):
    if request.method == "POST":
        # Extract form data
        tag_id = request.POST.get("tag_id")
        name = request.POST.get("name")
        breed = request.POST.get("breed")
        age = request.POST.get("age")
        weight = request.POST.get("weight")
        history = request.POST.get("history")

        # Reproduction
        reproduction_status = request.POST.get("reproduction_status")
        last_heat = request.POST.get("last_heat")
        last_ai = request.POST.get("last_ai")
        expected_calving = request.POST.get("expected_calving")

        # Lineage
        mother_tag = request.POST.get("mother_tag")
        father_tag = request.POST.get("father_tag")
        lineage_notes = request.POST.get("lineage_notes")

        # Create cow (even if tag exists, just create new)
        cow = Cow.objects.create(
            tag_id=tag_id,
            name=name,
            breed=breed,
            age=age,
            weight=weight,
            history=history,
            reproduction_status=reproduction_status,
            last_heat=last_heat or None,
            last_ai=last_ai or None,
            expected_calving=expected_calving or None,
            mother_tag=mother_tag,
            father_tag=father_tag,
            lineage_notes=lineage_notes,
        )

        # Always return a success message
        return JsonResponse({
            "status": "success",
            "message": "Cow registered successfully"
        })

    # For non-POST requests
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

def fetch_cows(request):
    cows = Cow.objects.all().values(
        'tag_id', 'name', 'breed', 'age', 'weight', 'reproduction_status'
    )
    return JsonResponse(list(cows), safe=False)


@csrf_exempt
def get_cow(request, tag_id):
    """Fetch a single cow's details for editing"""
    cow = get_object_or_404(Cow, tag_id=tag_id)
    data = {
        "tag_id": cow.tag_id,
        "name": cow.name,
        "breed": cow.breed,
        "age": cow.age,
        "weight": cow.weight,
        "history": cow.history,
        "reproduction_status": cow.reproduction_status,
        "last_heat": cow.last_heat.isoformat() if cow.last_heat else "",
        "last_ai": cow.last_ai.isoformat() if cow.last_ai else "",
        "expected_calving": cow.expected_calving.isoformat() if cow.expected_calving else "",
        "mother_tag": cow.mother_tag,
        "father_tag": cow.father_tag,
        "lineage_notes": cow.lineage_notes,
    }
    return JsonResponse(data)

@csrf_exempt
def update_cow(request, tag_id):
    """Update a cow record"""
    if request.method == "POST":
        cow = get_object_or_404(Cow, tag_id=tag_id)
        cow.name = request.POST.get("name")
        cow.breed = request.POST.get("breed")
        cow.age = request.POST.get("age")
        cow.weight = request.POST.get("weight")
        cow.history = request.POST.get("history")
        cow.reproduction_status = request.POST.get("reproduction_status")
        cow.last_heat = request.POST.get("last_heat") or None
        cow.last_ai = request.POST.get("last_ai") or None
        cow.expected_calving = request.POST.get("expected_calving") or None
        cow.mother_tag = request.POST.get("mother_tag")
        cow.father_tag = request.POST.get("father_tag")
        cow.lineage_notes = request.POST.get("lineage_notes")
        cow.save()
        return JsonResponse({"status": "success", "message": "Cow updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_cow(request, tag_id):
    """Delete a cow record"""
    if request.method == "POST":
        cow = get_object_or_404(Cow, tag_id=tag_id)
        cow.delete()
        return JsonResponse({"status": "success", "message": "Cow deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


###STAFF PANEL STARTS  #########################
#def staff_page(request):
 #   return render(request, "staff.html")
def staff_register_page(request):
    return render(request, "staffregister.html")


@csrf_exempt
def add_staff_ajax(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        address = request.POST.get("address")
        is_active = request.POST.get("is_active") == "True"

        Staff.objects.create(
            name=name,
            phone=phone,
            role=role,
            address=address,
            is_active=is_active
        )

        return JsonResponse({"status": "success", "message": "Staff added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


def fetch_staff(request):
    staff = Staff.objects.all().values(
        "id", "name", "phone", "role", "is_active", "address"
    )
    return JsonResponse(list(staff), safe=False)


def get_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    data = {
        "id": staff.id,
        "name": staff.name,
        "phone": staff.phone,
        "role": staff.role,
        "address": staff.address,
        "is_active": staff.is_active,
    }
    return JsonResponse(data)


@csrf_exempt
def update_staff(request, id):
    if request.method == "POST":
        staff = get_object_or_404(Staff, id=id)

        staff.name = request.POST.get("name")
        staff.phone = request.POST.get("phone")
        staff.role = request.POST.get("role")
        staff.address = request.POST.get("address")
        staff.is_active = request.POST.get("is_active") == "True"

        staff.save()

        return JsonResponse({"status": "success", "message": "Staff updated successfully"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt
def delete_staff(request, id):
    if request.method == "POST":
        staff = get_object_or_404(Staff, id=id)
        staff.delete()
        return JsonResponse({"status": "success", "message": "Staff deleted successfully"})
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# PAGE
def task_page(request):
    staff = Staff.objects.all()
    return render(request, "task_page.html", {"staff": staff})

# FETCH
def fetch_tasks(request):
    tasks = Task.objects.select_related("staff").all()

    data = []
    for t in tasks:
        data.append({
            "id": t.id,
            "staff": t.staff.name,     # <-- DataTable needs this
            "title": t.title,
            "due_date": str(t.due_date) if t.due_date else "",
            "status": t.status,
        })

    return JsonResponse(data, safe=False)

# ADD
def add_task(request):
    if request.method == "POST":
        Task.objects.create(
            staff_id=request.POST["staff"],
            title=request.POST["title"],
            description=request.POST.get("description", ""),
            due_date=request.POST.get("due_date"),
            status=request.POST.get("status", "Pending")
        )
        return JsonResponse({"message": "Task added successfully!"})
    return JsonResponse({"error": "Invalid request"}, status=400)

# GET SINGLE
def get_task(request, id):
    task = get_object_or_404(Task, id=id)
    return JsonResponse({
        "id": task.id,
        "staff": task.staff_id,
        "title": task.title,
        "description": task.description,
        "due_date": str(task.due_date) if task.due_date else "",
        "status": task.status,
    })

# UPDATE
def update_task(request, id):
    task = get_object_or_404(Task, id=id)

    task.staff_id = request.POST["staff"]
    task.title = request.POST["title"]
    task.description = request.POST.get("description", "")
    task.due_date = request.POST.get("due_date") or None
    task.status = request.POST.get("status")

    task.save()
    return JsonResponse({"message": "Task updated successfully!"})

# DELETE
def delete_task(request, id):
    get_object_or_404(Task, id=id).delete()
    return JsonResponse({"message": "Task deleted successfully!"})

#ATTENDANCE
def attendance_page(request):
    staff = Staff.objects.all()
    return render(request, "attendance_page.html", {"staff": staff})

def fetch_attendance(request):
    attendance = Attendance.objects.select_related("staff").all()

    data = []
    for a in attendance:
        data.append({
            "id": a.id,
            "staff": a.staff.name,      # <-- FIXED: DataTables needs this
            "date": str(a.date),
            "status": a.status,
            "time_in": str(a.time_in) if a.time_in else "",
            "time_out": str(a.time_out) if a.time_out else "",
        })

    return JsonResponse(data, safe=False)

def add_attendance(request):
    Attendance.objects.create(
        staff_id=request.POST["staff"],
        date=request.POST["date"],
        time_in=request.POST.get("time_in"),
        time_out=request.POST.get("time_out"),
        status=request.POST.get("status", "Present")
    )
    return JsonResponse({"message": "Attendance recorded!"})

def get_attendance(request, id):
    att = get_object_or_404(Attendance, id=id)
    return JsonResponse({
        "id": att.id,
        "staff": att.staff_id,
        "date": str(att.date),
        "time_in": str(att.time_in),
        "time_out": str(att.time_out),
        "status": att.status,
    })

def update_attendance(request, id):
    att = get_object_or_404(Attendance, id=id)
    att.staff_id = request.POST["staff"]
    att.date = request.POST["date"]
    att.time_in = request.POST.get("time_in")
    att.time_out = request.POST.get("time_out")
    att.status = request.POST.get("status")
    att.save()
    return JsonResponse({"message": "Attendance updated!"})

def delete_attendance(request, id):
    get_object_or_404(Attendance, id=id).delete()
    return JsonResponse({"message": "Attendance deleted!"})


#PERFOMANCE
def performance_page(request):
    staff = Staff.objects.all()
    tasks = Task.objects.all()
    return render(request, "performance_page.html", {
        "staff": staff,
        "tasks": tasks
    })

def fetch_performance(request):
    data = list(Performance.objects.values())
    return JsonResponse(data, safe=False)

def add_performance(request):
    Performance.objects.create(
        staff_id=request.POST["staff"],
        task_id=request.POST["task"],
        score=request.POST["score"],
        notes=request.POST.get("notes", ""),
        date=request.POST["date"]
    )
    return JsonResponse({"message": "Performance logged!"})

def get_performance(request, id):
    p = get_object_or_404(Performance, id=id)
    return JsonResponse({
        "id": p.id,
        "staff": p.staff_id,
        "task": p.task_id,
        "score": p.score,
        "notes": p.notes,
        "date": str(p.date)
    })

def update_performance(request, id):
    p = get_object_or_404(Performance, id=id)
    p.staff_id = request.POST["staff"]
    p.task_id = request.POST["task"]
    p.score = request.POST["score"]
    p.notes = request.POST.get("notes", "")
    p.date = request.POST["date"]
    p.save()
    return JsonResponse({"message": "Performance updated!"})

def delete_performance(request, id):
    get_object_or_404(Performance, id=id).delete()
    return JsonResponse({"message": "Performance deleted!"})


###STAFF PANEL STARTS  #########################

###MILK PRODUCTION PANEL #######################

# ====== MILK PRODUCTION ======
def milk_production_page(request):
    cows = Cow.objects.all()
    staff = Staff.objects.filter(role="Milking Operator")
    return render(request, "milk_production.html", {"cows": cows, "staff": staff})

@csrf_exempt
def add_milk_production_ajax(request):
    if request.method == "POST":
        cow_id = request.POST.get("cow")
        date = request.POST.get("date")
        shift = request.POST.get("shift")
        quantity_ltr = request.POST.get("quantity_ltr")
        staff_id = request.POST.get("recorded_by")

        MilkProduction.objects.create(
            cow_id=cow_id,
            date=date,
            shift=shift,
            quantity_ltr=quantity_ltr,
            recorded_by_id=staff_id
        )
        return JsonResponse({"status": "success", "message": "Milk production added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def fetch_milk_production(request):
    data = MilkProduction.objects.all().values(
        "id", "cow__tag_id", "date", "shift", "quantity_ltr", "recorded_by__name"
    )
    return JsonResponse(list(data), safe=False)

def get_milk_production(request, id):
    record = get_object_or_404(MilkProduction, id=id)
    data = {
        "id": record.id,
        "cow": record.cow.id,
        "date": record.date,
        "shift": record.shift,
        "quantity_ltr": record.quantity_ltr,
        "recorded_by": record.recorded_by.id if record.recorded_by else None
    }
    return JsonResponse(data)

@csrf_exempt
def update_milk_production(request, id):
    if request.method == "POST":
        record = get_object_or_404(MilkProduction, id=id)
        record.cow_id = request.POST.get("cow")
        record.date = request.POST.get("date")
        record.shift = request.POST.get("shift")
        record.quantity_ltr = request.POST.get("quantity_ltr")
        record.recorded_by_id = request.POST.get("recorded_by")
        record.save()
        return JsonResponse({"status": "success", "message": "Milk production updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_milk_production(request, id):
    if request.method == "POST":
        record = get_object_or_404(MilkProduction, id=id)
        record.delete()
        return JsonResponse({"status": "success", "message": "Milk production deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


### MILK SALES PANEL #######################

# PAGE
def milk_sales_page(request):
    buyers = MilkBuyer.objects.all()
    staff = Staff.objects.filter(role="Milking Operator")
    return render(request, "milk_sales.html", {"buyers": buyers, "staff": staff})

# ADD
@csrf_exempt
def add_milk_sale_ajax(request):
    if request.method == "POST":
        buyer_id = request.POST.get("buyer")
        date = request.POST.get("date")
        quantity_ltr = request.POST.get("quantity_ltr")
        price_per_ltr = request.POST.get("price_per_ltr")
        staff_id = request.POST.get("recorded_by")

        MilkSale.objects.create(
            buyer_id=buyer_id,
            date=date,
            quantity_ltr=quantity_ltr,
            price_per_ltr=price_per_ltr,
            recorded_by_id=staff_id
        )
        return JsonResponse({"status": "success", "message": "Milk sale added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# FETCH
def fetch_milk_sales(request):
    data = MilkSale.objects.all().values(
        "id",
        "buyer__name",
        "date",
        "quantity_ltr",
        "price_per_ltr",
        "recorded_by__name"
    )
    return JsonResponse(list(data), safe=False)

# GET SINGLE
def get_milk_sale(request, id):
    sale = get_object_or_404(MilkSale, id=id)
    data = {
        "id": sale.id,
        "buyer": sale.buyer.id,
        "date": sale.date,
        "quantity_ltr": sale.quantity_ltr,
        "price_per_ltr": sale.price_per_ltr,
        "recorded_by": sale.recorded_by.id if sale.recorded_by else None
    }
    return JsonResponse(data)

# UPDATE
@csrf_exempt
def update_milk_sale(request, id):
    if request.method == "POST":
        sale = get_object_or_404(MilkSale, id=id)
        sale.buyer_id = request.POST.get("buyer")
        sale.date = request.POST.get("date")
        sale.quantity_ltr = request.POST.get("quantity_ltr")
        sale.price_per_ltr = request.POST.get("price_per_ltr")
        sale.recorded_by_id = request.POST.get("recorded_by")
        sale.save()
        return JsonResponse({"status": "success", "message": "Milk sale updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# DELETE
@csrf_exempt
def delete_milk_sale(request, id):
    if request.method == "POST":
        sale = get_object_or_404(MilkSale, id=id)
        sale.delete()
        return JsonResponse({"status": "success", "message": "Milk sale deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

##### MILK BUYER############
# PAGE
def milk_buyer_page(request):
    return render(request, "milk_buyers.html")

# ADD
@csrf_exempt
def add_milk_buyer_ajax(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        location = request.POST.get("location")

        if not name or not contact:
            return JsonResponse({"status": "error", "message": "Name and Phone are required"}, status=400)

        MilkBuyer.objects.create(
            name=name,
            phone=contact,
            address=location
        )
        return JsonResponse({"status": "success", "message": "Milk buyer added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# FETCH
def fetch_milk_buyers(request):
    data = list(MilkBuyer.objects.all().values("id", "name", "phone", "address"))
    return JsonResponse(data, safe=False)

# GET SINGLE
def get_milk_buyer(request, id):
    buyer = get_object_or_404(MilkBuyer, id=id)
    return JsonResponse({
        "id": buyer.id,
        "name": buyer.name,
        "phone": buyer.phone,
        "address": buyer.address
    })

# UPDATE
@csrf_exempt
def update_milk_buyer(request, id):
    if request.method == "POST":
        buyer = get_object_or_404(MilkBuyer, id=id)
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        location = request.POST.get("location")

        if not name or not contact:
            return JsonResponse({"status": "error", "message": "Name and Phone are required"}, status=400)

        buyer.name = name
        buyer.phone = contact
        buyer.address = location
        buyer.save()
        return JsonResponse({"status": "success", "message": "Milk buyer updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# DELETE
@csrf_exempt
def delete_milk_buyer(request, id):
    if request.method == "POST":
        buyer = get_object_or_404(MilkBuyer, id=id)
        buyer.delete()
        return JsonResponse({"status": "success", "message": "Milk buyer deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
##### MILK BUYER############

###MILK PRODUCTION PANEL #######################


######### HEALTH & VETERINARY ##########################

###########################
# VACCINATION PANEL
###########################

# PAGE
def vaccination_scheduler_page(request):
    cows = Cow.objects.all()
    vets = Staff.objects.filter(role="Veterinary")
    return render(request, "vaccinations.html", {"cows": cows, "vets": vets})

# ADD
@csrf_exempt
def add_vaccination_ajax(request):
    if request.method == "POST":
        cow_id = request.POST.get("cow")
        vaccine_name = request.POST.get("vaccine_name")
        dose_number = request.POST.get("dose_number")
        scheduled_date = request.POST.get("scheduled_date")
        administered_date = request.POST.get("administered_date") or None
        vet_id = request.POST.get("veterinarian")
        notes = request.POST.get("notes", "")

        Vaccination.objects.create(
            cow_id=cow_id,
            vaccine_name=vaccine_name,
            dose_number=dose_number,
            scheduled_date=scheduled_date,
            administered_date=administered_date,
            veterinarian_id=vet_id,
            notes=notes
        )
        return JsonResponse({"status": "success", "message": "Vaccination added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# FETCH
def fetch_vaccinations(request):
    data = Vaccination.objects.all().values(
        "id",
        "cow__tag_id",
        "vaccine_name",
        "dose_number",
        "scheduled_date",
        "administered_date",
        "veterinarian__name",
        "notes"
    )
    return JsonResponse(list(data), safe=False)

# GET SINGLE
def get_vaccination(request, id):
    v = get_object_or_404(Vaccination, id=id)
    data = {
        "id": v.id,
        "cow": v.cow.id,
        "vaccine_name": v.vaccine_name,
        "dose_number": v.dose_number,
        "scheduled_date": v.scheduled_date,
        "administered_date": v.administered_date,
        "veterinarian": v.veterinarian.id if v.veterinarian else None,
        "notes": v.notes
    }
    return JsonResponse(data)

# UPDATE
@csrf_exempt
def update_vaccination(request, id):
    if request.method == "POST":
        v = get_object_or_404(Vaccination, id=id)
        v.cow_id = request.POST.get("cow")
        v.vaccine_name = request.POST.get("vaccine_name")
        v.dose_number = request.POST.get("dose_number")
        v.scheduled_date = request.POST.get("scheduled_date")
        v.administered_date = request.POST.get("administered_date") or None
        v.veterinarian_id = request.POST.get("veterinarian")
        v.notes = request.POST.get("notes", "")
        v.save()
        return JsonResponse({"status": "success", "message": "Vaccination updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

# DELETE
@csrf_exempt
def delete_vaccination(request, id):
    if request.method == "POST":
        v = get_object_or_404(Vaccination, id=id)
        v.delete()
        return JsonResponse({"status": "success", "message": "Vaccination deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

###########################
# DEWORMING PANEL
###########################

def deworming_reminders_page(request):
    cows = Cow.objects.all()
    vets = Staff.objects.filter(role="Veterinary")
    return render(request, "dewormings.html", {"cows": cows, "vets": vets})

@csrf_exempt
def add_deworming_ajax(request):
    if request.method == "POST":
        cow_id = request.POST.get("cow")
        dewormer_name = request.POST.get("dewormer_name")
        scheduled_date = request.POST.get("scheduled_date")
        administered_date = request.POST.get("administered_date") or None
        vet_id = request.POST.get("veterinarian")
        notes = request.POST.get("notes", "")

        Deworming.objects.create(
            cow_id=cow_id,
            dewormer_name=dewormer_name,
            scheduled_date=scheduled_date,
            administered_date=administered_date,
            veterinarian_id=vet_id,
            notes=notes
        )
        return JsonResponse({"status": "success", "message": "Deworming added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def fetch_deworming(request):
    data = Deworming.objects.all().values(
        "id",
        "cow__tag_id",
        "dewormer_name",
        "scheduled_date",
        "administered_date",
        "veterinarian__name",
        "notes"
    )
    return JsonResponse(list(data), safe=False)

def get_deworming(request, id):
    d = get_object_or_404(Deworming, id=id)
    data = {
        "id": d.id,
        "cow": d.cow.id,
        "dewormer_name": d.dewormer_name,
        "scheduled_date": d.scheduled_date,
        "administered_date": d.administered_date,
        "veterinarian": d.veterinarian.id if d.veterinarian else None,
        "notes": d.notes
    }
    return JsonResponse(data)

@csrf_exempt
def update_deworming(request, id):
    if request.method == "POST":
        d = get_object_or_404(Deworming, id=id)
        d.cow_id = request.POST.get("cow")
        d.dewormer_name = request.POST.get("dewormer_name")
        d.scheduled_date = request.POST.get("scheduled_date")
        d.administered_date = request.POST.get("administered_date") or None
        d.veterinarian_id = request.POST.get("veterinarian")
        d.notes = request.POST.get("notes", "")
        d.save()
        return JsonResponse({"status": "success", "message": "Deworming updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_deworming(request, id):
    if request.method == "POST":
        d = get_object_or_404(Deworming, id=id)
        d.delete()
        return JsonResponse({"status": "success", "message": "Deworming deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

###########################
# DISEASE PANEL
###########################

def disease_monitoring_page(request):
    cows = Cow.objects.all()
    vets = Staff.objects.filter(role="Veterinary")
    return render(request, "diseases.html", {"cows": cows, "vets": vets})

@csrf_exempt
def add_disease_ajax(request):
    if request.method == "POST":
        cow_id = request.POST.get("cow")
        disease_name = request.POST.get("disease_name")
        symptoms = request.POST.get("symptoms")
        diagnosis_date = request.POST.get("diagnosis_date") or timezone.now().date()
        vet_id = request.POST.get("veterinarian")
        status = request.POST.get("status", "Ongoing")
        notes = request.POST.get("notes", "")

        Disease.objects.create(
            cow_id=cow_id,
            disease_name=disease_name,
            symptoms=symptoms,
            diagnosis_date=diagnosis_date,
            veterinarian_id=vet_id,
            status=status,
            notes=notes
        )
        return JsonResponse({"status": "success", "message": "Disease record added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def fetch_diseases(request):
    data = Disease.objects.all().values(
        "id",
        "cow__tag_id",
        "disease_name",
        "symptoms",
        "diagnosis_date",
        "veterinarian__name",
        "status",
        "notes"
    )
    return JsonResponse(list(data), safe=False)

def get_disease(request, id):
    d = get_object_or_404(Disease, id=id)
    data = {
        "id": d.id,
        "cow": d.cow.id,
        "disease_name": d.disease_name,
        "symptoms": d.symptoms,
        "diagnosis_date": d.diagnosis_date,
        "veterinarian": d.veterinarian.id if d.veterinarian else None,
        "status": d.status,
        "notes": d.notes
    }
    return JsonResponse(data)

@csrf_exempt
def update_disease(request, id):
    if request.method == "POST":
        d = get_object_or_404(Disease, id=id)
        d.cow_id = request.POST.get("cow")
        d.disease_name = request.POST.get("disease_name")
        d.symptoms = request.POST.get("symptoms")
        d.diagnosis_date = request.POST.get("diagnosis_date")
        d.veterinarian_id = request.POST.get("veterinarian")
        d.status = request.POST.get("status")
        d.notes = request.POST.get("notes", "")
        d.save()
        return JsonResponse({"status": "success", "message": "Disease record updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_disease(request, id):
    if request.method == "POST":
        d = get_object_or_404(Disease, id=id)
        d.delete()
        return JsonResponse({"status": "success", "message": "Disease record deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

###########################
# TREATMENT PANEL
###########################

def treatment_history_page(request):
    cows = Cow.objects.all()
    vets = Staff.objects.filter(role="Veterinary")
    diseases = Disease.objects.all()
    return render(request, "treatments.html", {"cows": cows, "vets": vets, "diseases": diseases})

@csrf_exempt
def add_treatment_ajax(request):
    if request.method == "POST":
        cow_id = request.POST.get("cow")
        disease_id = request.POST.get("disease") or None
        medicine_name = request.POST.get("medicine_name")
        dosage = request.POST.get("dosage")
        start_date = request.POST.get("start_date") or timezone.now().date()
        end_date = request.POST.get("end_date") or None
        administered_by_id = request.POST.get("administered_by")
        notes = request.POST.get("notes", "")

        Treatment.objects.create(
            cow_id=cow_id,
            disease_id=disease_id,
            medicine_name=medicine_name,
            dosage=dosage,
            start_date=start_date,
            end_date=end_date,
            administered_by_id=administered_by_id,
            notes=notes
        )
        return JsonResponse({"status": "success", "message": "Treatment added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def fetch_treatments(request):
    data = Treatment.objects.all().values(
        "id",
        "cow__tag_id",
        "disease__disease_name",
        "medicine_name",
        "dosage",
        "start_date",
        "end_date",
        "administered_by__name",
        "notes"
    )
    return JsonResponse(list(data), safe=False)

def get_treatment(request, id):
    t = get_object_or_404(Treatment, id=id)
    data = {
        "id": t.id,
        "cow": t.cow.id,
        "disease": t.disease.id if t.disease else None,
        "medicine_name": t.medicine_name,
        "dosage": t.dosage,
        "start_date": t.start_date,
        "end_date": t.end_date,
        "administered_by": t.administered_by.id if t.administered_by else None,
        "notes": t.notes
    }
    return JsonResponse(data)

@csrf_exempt
def update_treatment(request, id):
    if request.method == "POST":
        t = get_object_or_404(Treatment, id=id)
        t.cow_id = request.POST.get("cow")
        t.disease_id = request.POST.get("disease") or None
        t.medicine_name = request.POST.get("medicine_name")
        t.dosage = request.POST.get("dosage")
        t.start_date = request.POST.get("start_date")
        t.end_date = request.POST.get("end_date") or None
        t.administered_by_id = request.POST.get("administered_by")
        t.notes = request.POST.get("notes", "")
        t.save()
        return JsonResponse({"status": "success", "message": "Treatment updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
def delete_treatment(request, id):
    if request.method == "POST":
        t = get_object_or_404(Treatment, id=id)
        t.delete()
        return JsonResponse({"status": "success", "message": "Treatment deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
######### HEALTH & VETERINARY ##########################


# ============================
# FEED INVENTORY
# ============================

# PAGE
def feed_inventory_page(request):
    return render(request, "feed_inventory.html")


# FETCH ALL FEEDS
def fetch_feeds(request):
    feeds = Feed.objects.all().values(
        "id", "name", "feed_type", "quantity_kg", "unit_price", "supplier", "expiry_date"
    )
    data = []
    for f in feeds:
        data.append({
            "id": f["id"],
            "name": f["name"],
            "feed_type": f["feed_type"],
            "quantity_kg": f["quantity_kg"],
            "unit_price": f["unit_price"],
            "supplier": f["supplier"] or "",
            "expiry_date": f["expiry_date"].strftime("%Y-%m-%d") if f["expiry_date"] else "",
        })
    return JsonResponse(data, safe=False)


# ADD FEED
@csrf_exempt
def add_feed_ajax(request):
    if request.method == "POST":
        name = request.POST.get("name")
        feed_type = request.POST.get("feed_type")
        quantity_kg = float(request.POST.get("quantity_kg", 0))
        unit_price = float(request.POST.get("unit_price", 0))
        supplier = request.POST.get("supplier", "")
        expiry_date = request.POST.get("expiry_date") or None

        Feed.objects.create(
            name=name,
            feed_type=feed_type,
            quantity_kg=quantity_kg,
            unit_price=unit_price,
            supplier=supplier,
            expiry_date=expiry_date
        )
        return JsonResponse({"status": "success", "message": "Feed added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


# GET SINGLE FEED
def get_feed(request, id):
    feed = get_object_or_404(Feed, id=id)
    data = {
        "id": feed.id,
        "name": feed.name,
        "feed_type": feed.feed_type,
        "quantity_kg": feed.quantity_kg,
        "unit_price": feed.unit_price,
        "supplier": feed.supplier or "",
        "expiry_date": feed.expiry_date.strftime("%Y-%m-%d") if feed.expiry_date else "",
    }
    return JsonResponse(data)


# UPDATE FEED
@csrf_exempt
def update_feed(request, id):
    if request.method == "POST":
        feed = get_object_or_404(Feed, id=id)
        feed.name = request.POST.get("name")
        feed.feed_type = request.POST.get("feed_type")
        feed.quantity_kg = float(request.POST.get("quantity_kg", feed.quantity_kg))
        feed.unit_price = float(request.POST.get("unit_price", feed.unit_price))
        feed.supplier = request.POST.get("supplier", feed.supplier)
        feed.expiry_date = request.POST.get("expiry_date") or None
        feed.save()
        return JsonResponse({"status": "success", "message": "Feed updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


# DELETE FEED
@csrf_exempt
def delete_feed(request, id):
    if request.method == "POST":
        feed = get_object_or_404(Feed, id=id)
        feed.delete()
        return JsonResponse({"status": "success", "message": "Feed deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


# ============================
# FEEDING PLAN PAGE
# ============================
def feeding_plan_page(request):
    # To populate dropdowns in the modal form
    cows = Cow.objects.all()
    feeds = Feed.objects.all()
    staff_members = Staff.objects.all()
    return render(request, "feeding_plan.html", {
        "cows": cows,
        "feeds": feeds,
        "staff_members": staff_members
    })

# ============================
# FETCH ALL FEEDING PLANS
# ============================
def fetch_feeding_plans(request):
    plans = FeedingPlan.objects.select_related("cow", "feed", "recorded_by").all()
    data = []
    for p in plans:
        data.append({
            "id": p.id,
            "cow": p.cow.tag_id,
            "feed": p.feed.name,
            "date": p.date.strftime("%Y-%m-%d"),
            "quantity_kg": p.quantity_kg,
            "notes": p.notes or "",
            "recorded_by": p.recorded_by.name if p.recorded_by else "",
        })
    return JsonResponse(data, safe=False)

# ============================
# ADD FEEDING PLAN
# ============================
@csrf_exempt
def add_feeding_plan_ajax(request):
    if request.method == "POST":
        cow_id = request.POST.get("cow")
        feed_id = request.POST.get("feed")
        date = parse_date(request.POST.get("date"))
        quantity_kg = float(request.POST.get("quantity_kg", 0))
        notes = request.POST.get("notes", "")
        recorded_by_id = request.POST.get("recorded_by") or None

        FeedingPlan.objects.create(
            cow_id=cow_id,
            feed_id=feed_id,
            date=date,
            quantity_kg=quantity_kg,
            notes=notes,
            recorded_by_id=recorded_by_id
        )
        return JsonResponse({"status": "success", "message": "Feeding plan added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

# ============================
# GET SINGLE FEEDING PLAN
# ============================
def get_feeding_plan(request, id):
    plan = get_object_or_404(FeedingPlan, id=id)
    data = {
        "id": plan.id,
        "cow": plan.cow.id,
        "feed": plan.feed.id,
        "date": plan.date.strftime("%Y-%m-%d"),
        "quantity_kg": plan.quantity_kg,
        "notes": plan.notes or "",
        "recorded_by": plan.recorded_by.id if plan.recorded_by else "",
    }
    return JsonResponse(data)

# ============================
# UPDATE FEEDING PLAN
# ============================
@csrf_exempt
def update_feeding_plan(request, id):
    if request.method == "POST":
        plan = get_object_or_404(FeedingPlan, id=id)
        plan.cow_id = request.POST.get("cow")
        plan.feed_id = request.POST.get("feed")
        plan.date = parse_date(request.POST.get("date"))
        plan.quantity_kg = float(request.POST.get("quantity_kg", plan.quantity_kg))
        plan.notes = request.POST.get("notes", plan.notes)
        recorded_by_id = request.POST.get("recorded_by") or None
        plan.recorded_by_id = recorded_by_id
        plan.save()
        return JsonResponse({"status": "success", "message": "Feeding plan updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

# ============================
# DELETE FEEDING PLAN
# ============================
@csrf_exempt
def delete_feeding_plan(request, id):
    if request.method == "POST":
        plan = get_object_or_404(FeedingPlan, id=id)
        plan.delete()
        return JsonResponse({"status": "success", "message": "Feeding plan deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


# ============================
# FEED PURCHASE PAGE
# ============================
def feed_purchase_page(request):
    # To populate dropdowns in the modal form
    feeds = Feed.objects.all()
    staff_members = Staff.objects.all()
    return render(request, "feed_purchase.html", {
        "feeds": feeds,
        "staff_members": staff_members
    })

# ============================
# FETCH ALL FEED PURCHASES
# ============================
def fetch_feed_purchases(request):
    purchases = FeedPurchase.objects.select_related("feed", "purchased_by").all()
    data = []
    for p in purchases:
        data.append({
            "id": p.id,
            "feed": p.feed.name,
            "quantity_kg": p.quantity_kg,
            "unit_price": p.unit_price,
            "total_cost": p.total_cost,
            "purchase_date": p.purchase_date.strftime("%Y-%m-%d"),
            "purchased_by": p.purchased_by.name if p.purchased_by else "",
        })
    return JsonResponse(data, safe=False)

# ============================
# ADD FEED PURCHASE
# ============================
@csrf_exempt
def add_feed_purchase_ajax(request):
    if request.method == "POST":
        feed_id = request.POST.get("feed")
        quantity_kg = float(request.POST.get("quantity_kg", 0))
        unit_price = float(request.POST.get("unit_price", 0))
        purchase_date = request.POST.get("purchase_date") or timezone.now().date()
        purchased_by_id = request.POST.get("purchased_by") or None

        FeedPurchase.objects.create(
            feed_id=feed_id,
            quantity_kg=quantity_kg,
            unit_price=unit_price,
            purchase_date=purchase_date,
            purchased_by_id=purchased_by_id
        )
        return JsonResponse({"status": "success", "message": "Feed purchase added successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

# ============================
# GET SINGLE FEED PURCHASE
# ============================
def get_feed_purchase(request, id):
    purchase = get_object_or_404(FeedPurchase, id=id)
    data = {
        "id": purchase.id,
        "feed": purchase.feed.id,
        "quantity_kg": purchase.quantity_kg,
        "unit_price": purchase.unit_price,
        "total_cost": purchase.total_cost,
        "purchase_date": purchase.purchase_date.strftime("%Y-%m-%d"),
        "purchased_by": purchase.purchased_by.id if purchase.purchased_by else "",
    }
    return JsonResponse(data)

# ============================
# UPDATE FEED PURCHASE
# ============================
@csrf_exempt
def update_feed_purchase(request, id):
    if request.method == "POST":
        purchase = get_object_or_404(FeedPurchase, id=id)
        purchase.feed_id = request.POST.get("feed")
        purchase.quantity_kg = float(request.POST.get("quantity_kg", purchase.quantity_kg))
        purchase.unit_price = float(request.POST.get("unit_price", purchase.unit_price))
        purchase.purchase_date = request.POST.get("purchase_date") or purchase.purchase_date
        purchased_by_id = request.POST.get("purchased_by") or None
        purchase.purchased_by_id = purchased_by_id
        purchase.save()  # total_cost is automatically calculated in save()
        return JsonResponse({"status": "success", "message": "Feed purchase updated successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

# ============================
# DELETE FEED PURCHASE
# ============================
@csrf_exempt
def delete_feed_purchase(request, id):
    if request.method == "POST":
        purchase = get_object_or_404(FeedPurchase, id=id)
        purchase.delete()
        return JsonResponse({"status": "success", "message": "Feed purchase deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
############### FEED & NUTRITION ############################################







###LOGOUT STARTS  #########################
def logout_view(request):
    logout(request)  # logs the user out
    return redirect('home')  # redirect to signup/home page
###LOGOUT STARTS  #########################

