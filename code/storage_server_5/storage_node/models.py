from django.db import models

# Create your models here.

class StorageServer(models.Model):
	server_id = models.IntegerField() #integers, 0,1,2...
	server_port = models.IntegerField()
	#no server_down field, servers only notify ui_server
	#otherwise ordering has to be present for bringing up storage_servers

class ClockStamp(models.Model):
	server_id = models.IntegerField()
	time_stamp = models.IntegerField(default = 0)

class RealData(models.Model):
	data_key = models.CharField(max_length = 100)
	data_value = models.CharField(max_length = 100)
	vector_clock = models.CharField(max_length = 200)

class HandedData(models.Model):
	data_key = models.CharField(max_length = 100)
	data_value = models.CharField(max_length = 100)
	vector_clock = models.CharField(max_length = 200)
	original_node_id = models.IntegerField()

class WriteRequest(models.Model):
	data_key = models.CharField(max_length = 100)
	data_value = models.CharField(max_length = 100)

class GetRequest(models.Model):
	data_key = models.CharField(max_length = 100)

class HandoffRequest(models.Model):
	data_key = models.CharField(max_length = 100)
	data_value = models.CharField(max_length = 100)
	original_node_id = models.IntegerField()
