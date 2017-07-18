# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
# Create your views here.

class JsonItem(object):
	def __init__(self):
		with open('items.json') as data_file:
			data = json.load(data_file)

		self.items_dict = data
		self.sent_data = []

	def get_list_items(self):
		list_items = []
		for object in self.items_dict:
			list_items.append(object['name'])
		return list_items

	def get_item_number(self, name):
		for object in self.items_dict:
			if object["name"] == name:
				return object["id"]

order_class = JsonItem();

def index(request):
	food_list = order_class.get_list_items()
	json_food_list = json.dumps(food_list)
	context = {'list': json_food_list}
	
	return render(request, 'main/templates/index.html', context)

@csrf_exempt
def order(request):
	# order_class = JsonItem()
	email_dict_list = []

	if request.is_ajax():
		if request.method == 'POST':
			order = json.loads(request.body)
			for key, value in order.iteritems():
				if key != "csrfmiddlewaretoken":
					dict_key = order_class.get_item_number(key)
					email_dict = {}
					email_dict["item_id"] = dict_key
					email_dict["item_name"] = key
					email_dict["item_quantity"] = value
					email_dict_list.append(email_dict)
			order_class.sent_data = email_dict_list
			send_email(email_dict_list)

			return HttpResponse(json.dumps({"url":"/success"}), content_type='application/json')

def parsejson():
	data = order_class.get_list_items()
	print data

def send_email(payload):
	subject = "Lee's Oriental Order"
	to = ['sale@chicagofood.com']
	from_email = 'leesoriental3240@gmail.com'
	message = get_template('main/templates/email_template.html').render({"items":payload})
	EmailMessage(subject, message, to=to, from_email=from_email).send()

def success(request):
	ordered = order_class.sent_data
	return render(request, 'main/templates/success.html', {'order_list':ordered})



