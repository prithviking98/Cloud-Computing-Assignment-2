from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(StorageServer)
admin.site.register(ClockStamp)
admin.site.register(RealData)
admin.site.register(HandedData)
