from django.db import models

# Create your models here.

class StorageServer(models.Model):
	server_id = models.IntegerField() #integers, 0,1,2...
	server_port = models.IntegerField()
	server_down = models.BooleanField(default = True) #true if server is down
