from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
#from .models import Cow, Staff


class CustomUser(AbstractUser):
    username = None  # disable username field
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('NormalUser', 'NormalUser'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='NormalUser')

    USERNAME_FIELD = 'email'       # use email to log in
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Cow(models.Model):
    # 1. Cow Profile
    tag_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    breed = models.CharField(max_length=100)
    age = models.IntegerField()
    weight = models.FloatField()
    history = models.TextField(blank=True, null=True)

    # 2. Reproduction Tracking
    reproduction_status = models.CharField(max_length=50, blank=True, null=True)
    last_heat = models.DateField(blank=True, null=True)
    last_ai = models.DateField(blank=True, null=True)
    expected_calving = models.DateField(blank=True, null=True)

    # 3. Lineage
    mother_tag = models.CharField(max_length=50, blank=True, null=True)
    father_tag = models.CharField(max_length=50, blank=True, null=True)
    lineage_notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag_id


class Staff(models.Model):
    ROLE_CHOICES = [
        ("Herdsman", "Herdsman"),
        ("Milking Operator", "Milking Operator"),
        ("Cleaner", "Cleaner"),
        ("Veterinary", "Veterinary"),
        ("Manager", "Manager"),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Late", "Late"),
    ]

    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.staff.name} - {self.date}"


class PerformanceLog(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)  # 1-10 rating
    feedback = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.staff.name} Score: {self.score}"


SHIFT_CHOICES = (
    ('morning', 'Morning'),
    ('evening', 'Evening'),
)

class MilkProduction(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    shift = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    quantity_ltr = models.DecimalField(max_digits=5, decimal_places=2)
    recorded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.cow.tag_id} - {self.date} - {self.shift}"

class MilkBuyer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MilkSale(models.Model):
    buyer = models.ForeignKey(MilkBuyer, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    quantity_ltr = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_ltr = models.DecimalField(max_digits=8, decimal_places=2)
    recorded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.buyer.name} - {self.date} - {self.quantity_ltr} L"


class Vaccination(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="vaccinations")
    vaccine_name = models.CharField(max_length=100)
    dose_number = models.PositiveIntegerField(default=1)
    scheduled_date = models.DateField()
    administered_date = models.DateField(blank=True, null=True)
    veterinarian = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'Veterinary'})
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cow.tag_id} - {self.vaccine_name} Dose {self.dose_number}"


class Deworming(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="dewormings")
    dewormer_name = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    administered_date = models.DateField(blank=True, null=True)
    veterinarian = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'Veterinary'})
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cow.tag_id} - {self.dewormer_name}"


class Disease(models.Model):
    STATUS_CHOICES = [
        ("Ongoing", "Ongoing"),
        ("Recovered", "Recovered")
    ]

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="diseases")
    disease_name = models.CharField(max_length=100)
    symptoms = models.TextField()
    diagnosis_date = models.DateField(default=timezone.now)
    veterinarian = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'Veterinary'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Ongoing")
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cow.tag_id} - {self.disease_name}"

class Treatment(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="treatments")
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, blank=True, related_name="treatments")
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    administered_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'Veterinary'})
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cow.tag_id} - {self.medicine_name}"



# ------------------------
# Feed Inventory
# ------------------------
class Feed(models.Model):
    FEED_TYPES = [
        ('hay', 'Hay'),
        ('silage', 'Silage'),
        ('concentrate', 'Concentrate'),
    ]

    name = models.CharField(max_length=100)
    feed_type = models.CharField(max_length=20, choices=FEED_TYPES)
    quantity_kg = models.FloatField(default=0.0)  # current stock in kg
    unit_price = models.FloatField(help_text="Price per kg")
    supplier = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.feed_type})"

# ------------------------
# Daily Feeding Plan
# ------------------------
class FeedingPlan(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="feeding_plans")
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    date = models.DateField()
    quantity_kg = models.FloatField()
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('cow', 'feed', 'date')

    def __str__(self):
        return f"{self.cow.tag_id} - {self.feed.name} ({self.quantity_kg}kg on {self.date})"

# ------------------------
# Feed Cost Tracking / Purchases
# ------------------------
class FeedPurchase(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    unit_price = models.FloatField()
    total_cost = models.FloatField(editable=False)
    purchase_date = models.DateField(default=timezone.now)
    purchased_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Automatically calculate total cost
        self.total_cost = self.quantity_kg * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.feed.name} - {self.quantity_kg}kg purchased on {self.purchase_date}"
