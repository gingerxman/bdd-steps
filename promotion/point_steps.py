# -*- coding: utf-8 -*-
import json

from behave import *
from features.steps.core import client as bdd_client
from features.steps.core import bdd_util, step_util, RestClient
from features.steps.product import product_steps

def get_point_product_id_by_name(name):
	product_id = product_steps.get_product_id_by_name(name)

	objs = bdd_util.exec_sql("ginger_promotion", "select * from point_product where product_id = %s", [product_id])
	return objs[0]['id']

@When(u"{corp_user}添加积分商品'{product_name}'")
def step_impl(context, corp_user, product_name):
	product_id = product_steps.get_product_id_by_name(product_name)

	input_data = json.loads(context.text)
	resp = context.client.put('ginger-promotion:point.product', {
		'product_id': product_id,
		'point_price': input_data['point_price'] * 100,
		'money_price': input_data.get('money_price', 0) * 100,
		'buy_limit': input_data.get('buy_limit', 1),
		'start_time': bdd_util.get_date(input_data.get('start_time', u'今天')),
		'end_time': bdd_util.get_date(input_data.get('end_time', u'7天后')),
	})
	bdd_util.assert_api_call_success(resp)

@When(u"{corp_user}更新积分商品'{product_name}'")
def step_impl(context, corp_user, product_name):
	point_product_id = get_point_product_id_by_name(product_name)

	update_data = {
		'id': point_product_id
	}
	input_data = json.loads(context.text)
	if 'point_price' in input_data:
		update_data['point_price'] = input_data['point_price'] * 100
	if 'money_price' in input_data:
		update_data['money_price'] = input_data['money_price'] * 100
	if 'buy_limit' in input_data:
		update_data['buy_limit'] = input_data['buy_limit']
	if 'start_time' in input_data:
		update_data['start_time'] = bdd_util.get_date(input_data['start_time'])
	if 'end_time' in input_data:
		update_data['end_time'] = bdd_util.get_date(input_data['end_time'])

	resp = context.client.post('ginger-promotion:point.product', update_data)
	bdd_util.assert_api_call(resp, context)

@When(u"{corp_user}禁用积分商品'{product_name}'")
def step_impl(context, corp_user, product_name):
	point_product_id = get_point_product_id_by_name(product_name)

	resp = context.client.put('ginger-promotion:point.disabled_products', {
		'ids': json.dumps([point_product_id])
	})
	bdd_util.assert_api_call(resp, context)

@When(u"{corp_user}启用积分商品'{product_name}'")
def step_impl(context, corp_user, product_name):
	point_product_id = get_point_product_id_by_name(product_name)

	resp = context.client.delete('ginger-promotion:point.disabled_products', {
		'ids': json.dumps([point_product_id])
	})
	bdd_util.assert_api_call(resp, context)

@When(u"{corp_user}删除积分商品'{product_name}'")
def step_impl(context, corp_user, product_name):
	point_product_id = get_point_product_id_by_name(product_name)

	resp = context.client.delete('ginger-promotion:point.product', {
		'id': point_product_id
	})
	bdd_util.assert_api_call(resp, context)

@Then(u"{corp_user}能获得积分商品列表")
def step_impl(context, corp_user):
	resp = context.client.get('ginger-promotion:point.products', {})
	bdd_util.assert_api_call_success(resp)
	actual = resp.data['products']

	for item in actual:
		item['name'] = item['product']['name']
		item['point_price'] = round(item['point_price']/100.0, 2)
		item['money_price'] = round(item['money_price']/100.0, 2)
		item['start_time'] = item['start_time'].split(' ')[0]
		item['end_time'] = item['end_time'].split(' ')[0]

	expected = json.loads(context.text)
	for item in expected:
		if 'start_time' in item:
			item['start_time'] = bdd_util.get_date(item['start_time']).strftime("%Y-%m-%d")
		if 'end_time' in item:
			item['end_time'] = bdd_util.get_date(item['end_time']).strftime("%Y-%m-%d")

	bdd_util.assert_list(expected, actual)

@Then(u"{user}能在商城中看到积分商品列表")
def step_impl(context, user):
	resp = context.client.get('ginger-promotion:point.enabled_products', {})
	bdd_util.assert_api_call_success(resp)
	actual = resp.data['products']

	for item in actual:
		item['name'] = item['product']['name']
		item['point_price'] = round(item['point_price']/100.0, 2)
		item['money_price'] = round(item['money_price']/100.0, 2)
		item['start_time'] = item['start_time'].split(' ')[0]
		item['end_time'] = item['end_time'].split(' ')[0]

	expected = json.loads(context.text)
	for item in expected:
		if 'start_time' in item:
			item['start_time'] = bdd_util.get_date(item['start_time']).strftime("%Y-%m-%d")
		if 'end_time' in item:
			item['end_time'] = bdd_util.get_date(item['end_time']).strftime("%Y-%m-%d")

	bdd_util.assert_list(expected, actual)
