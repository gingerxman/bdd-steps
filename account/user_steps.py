# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding('gb2312')

from behave import *
from features.steps.core import client as bdd_client
from features.steps.core import bdd_util, step_util, RestClient


@Given(u"{user}登录系统")
def step_impl(context, user):
	context.client = bdd_client.login('backend', user, password=None, context=context)

@When(u"{user}登录系统")
def step_impl(context, user):
	context.client = bdd_client.login('backend', user, password=None, context=context)

@Given(u"{user}注册为App用户")
def step_impl(context, user):
	context.client = bdd_client.login('app', user, password=None, context=context)
	resp = context.client.post('ginger-account:user.user', {
		'id': context.client.cur_user_id,
		'avatar': 'http://resource.vxiaocheng.com/ginger/girls/%s.jpg' % user
	})
	bdd_util.assert_api_call_success(resp)


@Given(u"{user}访问'{corpuser_name}'的商城")
def step_impl(context, user, corpuser_name):
	client = RestClient()

	corp_id = step_util.get_corp_id_for_corpuser(client, corpuser_name)

	resp = client.put('ginger-account:login.logined_mall_user', {
		'unionid': user,
		'name': user,
		'avatar': 'http://resource.vxiaocheng.com/veeno/demo/girls/%s/avatar.jpg' % user,
		'corp_id': corp_id
	})
	bdd_util.assert_api_call_success(resp)
	client.jwt_token = resp.data['jwt']
	client.cur_user_id = resp.data['id']

	context.corp = {
		"username": corpuser_name,
		"id": corp_id
	}
	context.client = client
