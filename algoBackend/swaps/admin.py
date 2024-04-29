from django.contrib import admin

from swaps.models import SwapOperation, SwapProposition

# Register your models here.

admin.site.register(SwapOperation)
admin.site.register(SwapProposition)