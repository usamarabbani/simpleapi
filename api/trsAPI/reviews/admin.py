from django.contrib import admin

from trsAPI.reviews.models import Company, Review


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'rating', 'ipaddress', 'user', 'company',
        'submitted_date', 'deleted_date',
    )
    list_filter = ('rating', 'submitted_date', 'deleted_date', 'user', 'company')
