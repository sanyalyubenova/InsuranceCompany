from django.contrib import admin
from InsuranceCompany.policies.models import InsurancePolicy, Discount, Claim


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ('policy_number', 'user', 'car', 'start_date', 'end_date', 'price', 'is_active', 'offer')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('policy_number', 'user__email', 'car__make', 'car__model')
    ordering = ('-start_date',)
    readonly_fields = ('policy_number',)
    
    fieldsets = (
        ('Policy Information', {
            'fields': ('policy_number', 'user', 'car', 'is_active')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Financial', {
            'fields': ('price', 'insurance_amount')
        }),
        ('Offer', {
            'fields': ('offer',)
        })
    )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('discount_type', 'percentage', 'get_applicable_policies_count')
    list_filter = ('discount_type',)
    search_fields = ('discount_type',)
    
    def get_applicable_policies_count(self, obj):
        return obj.applicable_to.count()
    get_applicable_policies_count.short_description = 'Applicable Policies'


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('id', 'policy', 'claim_date', 'amount', 'status')
    list_filter = ('status', 'claim_date')
    search_fields = ('policy__policy_number', 'description')
    ordering = ('-claim_date',)
    
    fieldsets = (
        ('Claim Information', {
            'fields': ('policy', 'claim_date', 'status')
        }),
        ('Details', {
            'fields': ('description', 'amount', 'photos')
        }),
    )
