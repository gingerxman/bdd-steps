# -*- coding: utf-8 -*-
import json

from behave import *
from features.steps.core import client as bdd_client
from features.steps.core import bdd_util, step_util, RestClient

def get_customer_id_by_name(name):
	if name == '':
		return 0

	objs = bdd_util.exec_sql("ginger_crm", "select * from customer_customer where name = %s", [name])
	return objs[0]['id']

@Then(u"{user}能获得自己的客户信息")
def step_impl(context, user):
	resp = context.client.get('ginger-crm:customer.customer', {
	})
	bdd_util.assert_api_call_success(resp)
	actual = resp.data

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)

@Then(u"{corp_user}能获得'{customer_name}'的客户信息")
def step_impl(context, corp_user, customer_name):
	resp = context.client.get('ginger-crm:customer.customer', {
		'id': get_customer_id_by_name(customer_name)
	})
	bdd_util.assert_api_call_success(resp)
	actual = resp.data

	expected = json.loads(context.text)
	bdd_util.assert_dict(expected, actual)

@Then(u"{corp_user}能获得客户列表")
def step_impl(context, corp_user):
	resp = context.client.get('ginger-crm:customer.customers', {})
	bdd_util.assert_api_call_success(resp)
	actual = resp.data['customers']

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)
