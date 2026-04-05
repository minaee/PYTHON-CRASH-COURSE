from django.contrib import admin

from .models import Transaction

# Register your models here.
admin.site.register(Transaction)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
