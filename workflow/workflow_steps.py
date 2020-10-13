# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding('gb2312')

from behave import *
from features.steps.core import bdd_util, RestClient

@given(u"重置服务")
def step_impl(context):
	rest_client = RestClient()
	response = rest_client.put('ginger-finance:dev.bdd_reset')
	bdd_util.assert_api_call_success(response)

	response = rest_client.put('ginger-account:dev.bdd_reset')
	bdd_util.assert_api_call_success(response)

	response = rest_client.put('ginger-crm:dev.bdd_reset')
	bdd_util.assert_api_call_success(response)

	response = rest_client.put('ginger-promotion:dev.bdd_reset')
	bdd_util.assert_api_call_success(response)

	response = rest_client.put('ginger-product:dev.bdd_reset')
	bdd_util.assert_api_call_success(response)

	response = rest_client.put('ginger-order:dev.bdd_reset')
	bdd_util.assert_api_call_success(response)

@then(u"结束测试")
def step_impl(context):
	import sys
	sys.exit(1)