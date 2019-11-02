from django.contrib import admin

# Register your models here.
from .models import StorageServer, SelfID, ClockStamp, RealData, HandedData

admin.site.register(StorageServer)
admin.site.register(SelfID)
admin.site.register(ClockStamp)
admin.site.register(RealData)
admin.site.register(HandedData)
