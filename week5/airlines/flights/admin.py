from django.contrib import admin
from .models import Flight,Airport,Passengers

# Register your models here.
class flightAdmin(admin.ModelAdmin):
    list_display = ('id','origin','destination','duration')

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ["flight"]

admin.site.register(Flight,flightAdmin)
admin.site.register(Airport)
admin.site.register(Passengers,PassengerAdmin)