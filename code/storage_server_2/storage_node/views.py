from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from .serializers import *
from .models import *
from storage_server.settings import SELF_ID, NUM_NODES, NODE_IDS
# Create your views here.

@api_view(['GET','PUT','DELETE'])
def store(request):
	print("storage_node/store")

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
def handoff(request):

	clock = ClockStamp.objects.get(server_id = SELF_ID)
	clock.time_stamp = clock.time_stamp+1
	clock.save()

	request_data = JSONParser().parse(request)
	request_serializer = HandoffRequestSerializer(data=request_data)
	if request_serializer.is_valid():
		data_key = request_data['data_key']
		data_value = request_data['data_value']
		clocks = ClockStamp.objects.order_by('server_id')
		vector_clock = str(clocks[0].time_stamp)
		for i in range(1,clocks.count()):
			vector_clock= vector_clock + ',' + str(clocks[i].time_stamp)
		original_node_id = request_data['original_node_id']
		handed_data = HandedData(data_key = data_key, data_value = data_value, vector_clock = vector_clock, original_node_id = original_node_id)
		handed_data.save()
		serializer = HandedDataSerializer(handed_data)
		return JsonResponse(serializer.data)
	return JsonResponse(request_serializer.errors, status=400) #bad request

@api_view(['PUT'])
def handoff_return(request):
	clock = ClockStamp.objects.get(server_id = SELF_ID)
	clock.time_stamp = clock.time_stamp+1
	clock.save()

	request_datas = JSONParser().parse(request)
	print(request_datas)
	print("request_datas return list len", len(request_datas['return_list']))
	for request_data in request_datas['return_list']:
		request_serializer = HandedDataSerializer(data = request_data)
		if request_serializer.is_valid():
			print(request_serializer.data)
			print(len(request_serializer.data))
			clocks = ClockStamp.objects.order_by('server_id')
			vector_clock = request_serializer.data['vector_clock']
			vector_clock = vector_clock.split(',')

			for i in range(0,len(vector_clock)):
				clocks[i].time_stamp = max(clocks[i].time_stamp, int(vector_clock[i]))
				clocks[i].save()

			data_key = request_data['data_key']
			data_value = request_data['data_value']
			handed_data = RealData(data_key = data_key, data_value = data_value, vector_clock = request_serializer.data['vector_clock'])
			try:
				stored_data = RealData.objects.get(data_key = data_key)
				stored_data.delete()
			except RealData.DoesNotExist:
				print("key doesn't already exist")
			handed_data.save()
		else:
			return JsonResponse(request_serializer.errors, status=400) #bad request
	return Response(status = '200')

@api_view(['GET'])
def handoff_return_trigger(request):
	for id in NODE_IDS:
		data_set = HandedData.filter(original_node_id = id)
		json = JSONRenderer().render(data_set, many = True)

	return Response(status=200)
