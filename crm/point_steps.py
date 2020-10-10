# -*- coding: utf-8 -*-
import json

from behave import *
from features.steps.core import client as bdd_client
from features.steps.core import bdd_util, step_util, RestClient

def get_point_rule_id_by_name(name):
	if name == '':
		return 0

	objs = bdd_util.exec_sql("ginger_crm", "select * from point_rule where name = %s", [name])
	return objs[0]['id']

@When(u"{corp_user}添加积分规则")
def step_impl(context, corp_user):
	input_data = json.loads(context.text)
	resp = context.client.put('ginger-crm:point.point_rule', {
		"name": input_data['name'],
		'type': input_data['type'],
		'point': input_data['point'],
		'data': json.dumps(input_data['data'])
	})
	bdd_util.assert_api_call_success(resp)

@When(u"{corp_user}更新积分规则'{rule_name}'")
def step_impl(context, corp_user, rule_name):
	rule_id = get_point_rule_id_by_name(rule_name)
	resp = context.client.get('ginger-crm:point.point_rule', {
		'id': rule_id
	})
	rule_type = resp.data['type']

	input_data = json.loads(context.text)
	resp = context.client.post('ginger-crm:point.point_rule', {
		'id': rule_id,
		'type': rule_type,
		'point': input_data['point'],
		'data': json.dumps(input_data['data'])
	})
	bdd_util.assert_api_call_success(resp)

@When(u"{corp_user}删除积分规则'{rule_name}'")
def step_impl(context, corp_user, rule_name):
	rule_id = get_point_rule_id_by_name(rule_name)

	resp = context.client.delete('ginger-crm:point.point_rule', {
		'id': rule_id
	})
	bdd_util.assert_api_call(resp, context)

@Then(u"{corp_user}能获得积分规则列表")
def step_impl(context, corp_user):
	resp = context.client.get('ginger-crm:point.point_rules', {})
	bdd_util.assert_api_call_success(resp)
	actual = resp.data['rules']

	expected = json.loads(context.text)
	bdd_util.assert_list(expected, actual)
