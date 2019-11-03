from rest_framework import serializers
from .models import *

class RealDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = RealData
		fields = ['data_key', 'data_value', 'vector_clock']

class WriteRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = WriteRequest
		fields = ['data_key', 'data_value']

class GetRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = GetRequest
		fields = ['data_key']
