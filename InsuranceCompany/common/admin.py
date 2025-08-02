from django.contrib import admin
from InsuranceCompany.common.models import Car, Offer


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'get_policy_info')
    list_filter = ('make', 'year')
    search_fields = ('make', 'model')
    ordering = ('make', 'model', 'year')
    
    def get_policy_info(self, obj):
        if hasattr(obj, 'insurancepolicy'):
            return f"Policy: {obj.insurancepolicy.policy_number}"
        return "No Policy"
    get_policy_info.short_description = 'Policy Information'


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'insurance_amount', 'premium', 'status', 'created_at', 'get_discounts_count')
    list_filter = ('status', 'created_at', 'car__make', 'car__year')
    search_fields = ('user__email', 'car__make', 'car__model', 'id')
    ordering = ('-created_at',)
    readonly_fields = ('premium', 'created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'car', 'status')
        }),
        ('Financial Details', {
            'fields': ('insurance_amount', 'premium', 'discounts')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_discounts_count(self, obj):
        return obj.discounts.count()
    get_discounts_count.short_description = 'Discounts Applied'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'car').prefetch_related('discounts')
