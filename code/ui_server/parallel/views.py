from django.shortcuts import render
import json
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.response import Response
import requests

from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.query_utils import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt


READ_URL = 'https://bits-oasis.org/ems/events'
WRITE_URL = 'https://bits-oasis.org/ems/events'

servers_port = ['8010','8020','8030','8040', '8050']

servers_port_hash = []

for port in servers_port:
	servers_port_hash.append((hash(port)%100,port))

servers_port_hash.sort()


@api_view(['GET'])
def read_handler(request):
	try:
		key = request.GET['key']
	except:
		return Response({'message':'Invalid data/url'}, status=400)

	# key = data['key']
	hash_key = hash(key)

	ptr = 4
	for port_tuple in servers_port_hash:
		if port_tuple[0] > hash_key:
			break
		ptr = (ptr + 1)%5

	x = ptr

	count = 0
	data = {}

	r = requests.get("http://localhost:" + servers_port_hash[x][1] + "/storage_node/store/", json={'data_key':key})
	if r.status_code==200:
		try:
			data = r.json()
			count = count+1
		except:
			pass

	r = requests.get("http://localhost:" + servers_port_hash[(x+1)%5][1] + "/storage_node/store/", json={'data_key':key})
	if r.status_code==200:
		try:
			data = r.json()
			count = count+1
		except:
			pass


	r = requests.get("http://localhost:" + servers_port_hash[(x+2)%5][1] + "/storage_node/store/", json={'data_key':key})

	if r.status_code==200:
		try:
			data = r.json()
			count = count+1
		except:
			pass

	if(count < 2):
		return Response(data,status = 400)

	return Response(data, status=200)


# @api_view(['POST'])
@csrf_exempt
def write_handler(request):
	# print(request.data)

	try:
		key = request.POST['key']
		value = request.POST['value']
	except:
		try:
			key = request.data['key']
			value = request.data['value']
		except:
			return JsonResponse({'message':'Invalid data/url'}, status=400)

	hash_key = hash(key)%100

	ptr = 4
	for port_tuple in servers_port_hash:
		if port_tuple[0] > hash_key:
			break
		ptr = (ptr + 1)%5

	x = ptr

	count = 0
	data={}
	r = requests.put("http://localhost:" + servers_port_hash[x][1] + "/storage_node/store/", json={'data_key':key, 'data_value':value})
	print(r.status_code)
	if r.status_code==200:
		try:
			data = r.json()
			count = count+1

		except:
			pass

	r = requests.put("http://localhost:" + servers_port_hash[(x+1)%5][1] + "/storage_node/store/", json={'data_key':key, 'data_value':value})
	print(r.status_code)
	if r.status_code==200:
		try:
			data = r.json()
			count = count+1
		except:
			pass


	r = requests.put("http://localhost:" + servers_port_hash[(x+2)%5][1] + "/storage_node/store/", json={'data_key':key, 'data_value':value})
	print(r.status_code)
	if r.status_code==200:
		try:
			data = r.json()
			count = count+1
		except:
			pass


	if(count < 2) :
		ptr = (x+3)%5

		while ptr != x and count < 2:
			r = requests.put("http://localhost:" + servers_port_hash[ptr%5][1] + "/storage_node/store/", json={'data_key':key, 'data_value':value})
			ptr = (ptr+1)%5

			if r.status_code==200:
				try:
					data = r.json()
					count = count+1
				except:
					pass


		if count < 2 :
			return JsonResponse(data,status = 400)
		else:
			return JsonResponse(data,status = 200)
	else:
		return JsonResponse(data, status= 200)


def home_html(request):
	return render(request, 'index.html')


def read_html(request):
	return render(request, 'read.html')


def write_html(request):
	return render(request, 'write.html')
