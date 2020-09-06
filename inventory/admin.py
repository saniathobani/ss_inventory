from django.contrib import admin

# Register your models here.
from .models import Lot, Expenses

class LotAdmin(admin.ModelAdmin):
    list_display = ('scrap_category','purchased_date', 'status', 'description')
    list_display_links = ('scrap_category',)
    list_filter = ('purchased_date','status',)
    search_fields = ('scrap_category','purchased_date', 'status', 'description')
    list_per_page = 20



class ExpensesAdmin(admin.ModelAdmin):
    list_display = ('handler','date', 'category', 'amount')
    list_display_links = ('handler',)
    list_filter = ('date','category',)
    search_fields = ('scrap_category','date', 'category', 'amount')
    list_per_page = 20

admin.site.register(Lot, LotAdmin)

admin.site.register(Expenses, ExpensesAdmin)