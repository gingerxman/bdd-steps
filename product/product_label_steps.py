# -*- coding: utf-8 -*-
import json

from behave import *

from features.steps.core import bdd_util

def get_product_label_id_by_name(name):
	objs = bdd_util.exec_sql(bdd_util.DB_PRODUCT, "select * from product_label where name = %s", [name])
	return objs[0]['id']


@Then(u"{user}能看到标签列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	resp = context.client.get("ginger-product:product.corp_labels")
	actual = resp.data["labels"]

	bdd_util.assert_api_call_success(resp)
	bdd_util.assert_list(expected, actual)

@Then(u"{user}能看到可用的标签列表")
def step_impl(context, user):
	expected = json.loads(context.text)
	resp = context.client.get("ginger-product:product.labels")
	actual = resp.data["labels"]

	bdd_util.assert_api_call_success(resp)
	bdd_util.assert_list(expected, actual)

@When(u"{user}创建标签")
def step_impl(context, user):
	datas = json.loads(context.text)
	for data in datas:

		resp = context.client.put("ginger-product:product.label", data)
		bdd_util.assert_api_call_success(resp)

@When(u"{user}删除商品标签'{name}'")
def step_impl(context, user, name):
	id = get_product_label_id_by_name(name)
	resp = context.client.delete("ginger-product:product.label", {"id": id})
	bdd_util.assert_api_call_success(resp)

@When(u"{user}修改标签'{name}'的信息")
def step_impl(context, user, name):
	params = json.loads(context.text)
	id = get_product_label_id_by_name(name)
	params['id'] = id

	resp = context.client.post("ginger-product:product.label", params)
	bdd_util.assert_api_call_success(resp)

@When(u"{user}启用标签'{name}'")
def step_impl(context, user, name):
	id = get_product_label_id_by_name(name)
	resp = context.client.delete("ginger-product:product.disabled_label", {"id": id})
	bdd_util.assert_api_call_success(resp)

@When(u"{user}禁用标签'{name}'")
def step_impl(context, user, name):
	id = get_product_label_id_by_name(name)
	resp = context.client.put("ginger-product:product.disabled_label", {"id": id})
	bdd_util.assert_api_call_success(resp)
