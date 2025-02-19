from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BloodInventory, DonorProfile, PatientRequest

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_type', 'units_available')
    list_filter = ('blood_type',)
    search_fields = ('blood_type',)

class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'blood_units', 'status', 'created_at')
    list_filter = ('blood_type', 'status', 'created_at')
    search_fields = ('user__username', 'blood_type')
    ordering = ('-created_at',)

class PatientRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_type', 'units_required', 'status', 'created_at')
    list_filter = ('blood_type', 'status', 'created_at')
    search_fields = ('user__username', 'blood_type')
    ordering = ('-created_at',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(BloodInventory, BloodInventoryAdmin)
admin.site.register(DonorProfile, DonorProfileAdmin)
admin.site.register(PatientRequest, PatientRequestAdmin)