from django.contrib import admin

from spreads.models import SpreadProposition, SpreadOperation

# Register your models here.

admin.site.register(SpreadOperation)
admin.site.register(SpreadProposition)