from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *
from storage_server.settings import SELF_ID
# Create your views here.

@api_view(['GET','PUT','DELETE'])
def store(request):
	print("storage_node/store")

	#TODO: update self clock
	clock = ClockStamp.objects.get(server_id = SELF_ID)
	clock.time_stamp = clock.time_stamp+1
	clock.save()

	if request.method == 'GET':
		request_data = JSONParser().parse(request)
		request_serializer = GetRequestSerializer(data=request_data)
		if request_serializer.is_valid():
			data_key = request_data['data_key']
			try:
				stored_data = RealData.objects.get(data_key = data_key)
			except RealData.DoesNotExist:
				return Response( status = 404) #not found
			serializer = RealDataSerializer(stored_data)
			return JsonResponse(serializer.data)
		return JsonResponse(request_serializer.errors, status=400) #bad request

	elif request.method == 'PUT':
		request_data = JSONParser().parse(request)
		request_serializer = WriteRequestSerializer(data=request_data)
		if request_serializer.is_valid():
			data_key = request_data['data_key']
			try:
				stored_data = RealData.objects.get(data_key = data_key)
				stored_data.delete()
			except RealData.DoesNotExist:
				print("key doesn't already exist")
			data_value = request_data['data_value']
			clocks = ClockStamp.objects.order_by('server_id')
			vector_clock = str(clocks[0].time_stamp)
			for i in range(1,clocks.count()):
				vector_clock= vector_clock + ',' + str(clocks[i].time_stamp)
			storage_data = RealData(data_key = data_key, data_value = data_value, vector_clock = vector_clock)
			storage_data.save()
			serializer = RealDataSerializer(storage_data)
			return JsonResponse(serializer.data)
		return JsonResponse(request_serializer.errors, status=400) #bad request

	elif request.method == 'DELETE':
		request_data = JSONParser().parse(request)
		request_serializer = GetRequestSerializer(data=request_data)
		if request_serializer.is_valid():
			data_key = request_data['data_key']
			try:
				stored_data = RealData.objects.get(data_key = data_key)
			except RealData.DoesNotExist:
				return Response( status = 404) #not found
			stored_data.delete()
			serializer = RealDataSerializer(stored_data)
			return JsonResponse(serializer.data)
		return JsonResponse(request_serializer.errors, status=400) #bad request

@api_view(['PUT'])
def store(request):
	return Response()
