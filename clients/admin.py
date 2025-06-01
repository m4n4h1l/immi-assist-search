# in clients/admin.py

from django.contrib import admin
# 1. Import the original admin classes and models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from .models import Client, ImmigrationCase, Notice, Appointment

# --- Custom Admin Classes that EXTEND the defaults ---

# 2. Create our custom class by inheriting from Django's BaseUserAdmin
class CustomUserAdmin(BaseUserAdmin):
    # We only need to override the one method we want to change.
    # All other functionality (display, search, etc.) is inherited automatically.
    def has_module_permission(self, request):
        return request.user.is_superuser

class CustomGroupAdmin(BaseGroupAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

# --- The Safe Unregister/Re-register Pattern ---

# 3. Unregister the default admin classes
admin.site.unregister(User)
admin.site.unregister(Group)

# 4. Register the User and Group models with our new, extended admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)


# ===================================================================
# All of our app's models remain registered as before
# ===================================================================

class DerivativeInline(admin.TabularInline):
    model = Client
    fk_name = 'principal_applicant'
    fields = ('first_name', 'last_name', 'relationship_type', 'date_of_birth', 'alien_number')
    extra = 1
    verbose_name = "Family Member"
    verbose_name_plural = "Family Members (Derivatives)"

class ImmigrationCaseInline(admin.TabularInline):
    model = ImmigrationCase
    extra = 0

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'relationship_type', 'alien_number', 'date_of_birth')
    search_fields = ('last_name', 'first_name', 'alien_number')
    fields = ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'alien_number', 'relationship_type', 'principal_applicant')
    inlines = [DerivativeInline, ImmigrationCaseInline]

class NoticeInline(admin.TabularInline):
    model = Notice
    extra = 1
    fields = ('entry_date', 'form_type', 'i765_category', 'receipt_number', 'received_date', 'processing_center')

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 1

@admin.register(ImmigrationCase)
class ImmigrationCaseAdmin(admin.ModelAdmin):
    list_display = ('case_name', 'client', 'date_opened')
    list_filter = ('date_opened',)
    search_fields = ('case_name', 'client__first_name', 'client__last_name')
    inlines = [NoticeInline, AppointmentInline]

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('case', 'form_type', 'receipt_number', 'received_date')
    list_filter = ('form_type', 'processing_center')
    search_fields = ('case__client__first_name', 'receipt_number')