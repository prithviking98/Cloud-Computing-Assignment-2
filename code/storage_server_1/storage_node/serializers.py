from rest_framework import serializers
from .models import *

class RealDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = RealData
		fields = ['data_key', 'data_value', 'vector_clock']

class HandedDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = HandedData
		fields = ['data_key', 'data_value', 'vector_clock', 'original_node_id']

class HandoffRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = HandoffRequest
		fields = ['data_key', 'data_value', 'original_node_id']

class WriteRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = WriteRequest
		fields = ['data_key', 'data_value']

class GetRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = GetRequest
		fields = ['data_key']
