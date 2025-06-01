# in clients/models.py

from django.db import models
from django.utils import timezone

class Client(models.Model):
    # We are updating this list to include the new types
    RELATIONSHIP_CHOICES = [
        ('PRINCIPAL', 'Principal Applicant'),
        ('SPOUSE', 'Spouse'),
        ('CHILD', 'Child'),
        ('PARENT', 'Parent'),    # ADDED
        ('SIBLING', 'Sibling'),  # ADDED
    ]

    # This links a derivative client back to their principal applicant.
    # It's a "self-referencing" relationship. It can be blank because the Principal has no parent in this context.
    principal_applicant = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL, # Prevents deleting family if a principal is deleted
        null=True,
        blank=True,
        related_name='derivatives'
    )
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='PRINCIPAL')
    
    # --- Existing fields ---
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    alien_number = models.CharField(max_length=20, blank=True, unique=True, null=True, help_text="A-Number (if available)")
    date_of_birth = models.DateField(help_text="Format: YYYY-MM-DD")

    def __str__(self):
        return f"{self.first_name} {self.last_name} (A#: {self.alien_number or 'N/A'})"


# The ImmigrationCase and Notice models remain unchanged below this line...
class ImmigrationCase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cases')
    case_name = models.CharField(max_length=200, help_text="e.g., 'I-485 Application - 2025' or 'Asylum Case'")
    date_opened = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.case_name} for {self.client}"


class Notice(models.Model):
    case = models.ForeignKey(ImmigrationCase, on_delete=models.CASCADE, related_name='notices')
    entry_date = models.DateField(default=timezone.now, help_text="The date you are entering this information.")
    form_type = models.CharField(max_length=50, help_text="e.g., I-485, I-765, Account Access Notice")
    i765_category = models.CharField(max_length=10, blank=True, help_text="e.g., C11, C5. Only for I-765 forms.")
    receipt_number = models.CharField(max_length=50, blank=True)
    received_date = models.DateField(blank=True, null=True, help_text="The 'Received Date' on the notice from USCIS.")
    processing_center = models.CharField(max_length=100, blank=True, help_text="e.g., California Service Center")
    
    def __str__(self):
        return f"Notice for {self.case.client} - {self.form_type} ({self.receipt_number or 'No Receipt #'})"
    
# Add this class to the end of your clients/models.py file

class Appointment(models.Model):
    case = models.ForeignKey(ImmigrationCase, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField(help_text="Date and time of the appointment")
    purpose = models.CharField(max_length=255, help_text="e.g., USCIS Biometrics, Citizenship Interview")
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        # This provides a nice, readable name for each appointment in the admin panel
        return f"{self.purpose} on {self.appointment_date.strftime('%Y-%m-%d %I:%M %p')}"