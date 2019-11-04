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

def get_ptr(key):
	hash_key = hash(key)

	ptr = 4
	for port_tuple in servers_port_hash:
		if port_tuple[0] > hash_key:
			break
		ptr = (ptr + 1)%5

	return ptr


@api_view(['GET'])
def read_handler(request):
	try:
		key = request.GET['key']
	except:
		return Response({'message':'Invalid data/url'}, status=400)

	
	x = get_ptr(key)

	count = 0
	data = {}

	try:
		r = requests.get("http://localhost:" + servers_port_hash[x][1] + "/storage_node/store/", json={'data_key':key})
		if r.status_code==200:
			try:
				data[x] = r.json()
				count = count+1
			except:
				pass
		elif r.status_code==404:
			data[x] = 'Key not found at this server'
	except:
		data[x] = 'Server Down'



	try:
		r = requests.get("http://localhost:" + servers_port_hash[(x+1)%5][1] + "/storage_node/store/", json={'data_key':key})
		if r.status_code==200:
			try:
				data[(x+1)%5] = r.json()
				count = count+1
			except:
				pass
		elif r.status_code==404:
			data[(x+1)%5] = 'Key not found at this server'
	except:
		data[(x+1)%5] = 'Server Down'



	try:
		r = requests.get("http://localhost:" + servers_port_hash[(x+2)%5][1] + "/storage_node/store/", json={'data_key':key})
		if r.status_code==200:
			try:
				data[(x+2)%5] = r.json()
				count = count+1
			except:
				pass
		elif r.status_code==404:
			data[(x+2)%5] = 'Key not found at this server'
	except:
		data[(x+2)%5] = 'Server Down'



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

	x = get_ptr(key)

	count = 0
	data={}
	failed = []
	try:
		r = requests.put("http://localhost:" + servers_port_hash[(x+0)%5][1] + "/storage_node/store/", json={'data_key':key, 'data_value':value})

		if r.status_code==200:
			try:
				data[(x+0)%5]= r.json()
				count = count+1

			except:
				pass
	except:
		failed.append((x+0)%5)
		data[(x+0)%5] = 'Server Down'




	try:
		r = requests.put("http://localhost:" + servers_port_hash[(x+1)%5][1] + "/storage_node/store/", json={'data_key':key, 'data_value':value})

		if r.status_code==200:
			try:
				data[(x+1)%5]= r.json()
				count = count+1

			except:
				pass
	except:
		failed.append((x+1)%5)
		data[(x+1)%5] = 'Server Down'


	try:
		r = requests.put("http://localhost:" + servers_port_hash[(x+2)%5][1] + "/storage_node/store/", json={'data_key':key, 'data_value':value})

		if r.status_code==200:
			try:
				data[(x+2)%5]= r.json()
				count = count+1

			except:
				pass
	except:
		failed.append((x+2)%5)
		data[(x+2)%5] = 'Server Down'


	if(count < 2) :
		ptr1 = (x+3)%5
		ptr2 = (x+4)%5
		for failed_node in failed:

			try:
				r = requests.put("http://localhost:" + servers_port_hash[ptr1][1] + "/storage_node/handoff/", json={'original_node_id':failed_node, 'data_key':key, 'data_value':value})

				if r.status_code==200:
					try:
						data['handoff_' + str(ptr1)+'__failed_'+str(failed_node)]= r.json()
						count = count+1

					except:
						pass
			except:
				data['handoff_' + str(ptr1)] = 'Server Down'



			try:
				r = requests.put("http://localhost:" + servers_port_hash[ptr2][1] + "/storage_node/handoff/", json={'original_node_id':failed_node, 'data_key':key, 'data_value':value})

				if r.status_code==200:
					try:
						data['handoff_' + str(ptr2)+'__failed_'+str(failed_node)]= r.json()
						count = count+1

					except:
						pass
			except:
				data['handoff_' + str(ptr2)] = 'Server Down'




		if count < 2 :
			return JsonResponse(data,status = 400)
		else:
			return JsonResponse(data,status = 200)
	else:
		return JsonResponse(data, status= 200)

@api_view(['GET'])
def del_handler(request):
	
	try:
		key = request.GET['key']
	except:
		return Response({'message':'Invalid data/url'}, status=400)

	x = get_ptr(key)
	
	try:
		r = requests.delete("http://localhost:" + servers_port_hash[x][1] + "/storage_node/store/", json={'data_key':key})
	except:
		pass

	try:
		r = requests.delete("http://localhost:" + servers_port_hash[(x+1)%5][1] + "/storage_node/store/", json={'data_key':key})
	except:
		pass

	try:
		r = requests.delete("http://localhost:" + servers_port_hash[(x+2)%5][1] + "/storage_node/store/", json={'data_key':key})
	except:
		pass
	
def home_html(request):
	return render(request, 'index.html')


def read_html(request):
	return render(request, 'read.html')


def write_html(request):
	return render(request, 'write.html')

def del_html(request):
	return render(request, 'del.html')

