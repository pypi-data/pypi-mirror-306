# ------------------------------------------------------------------------
# Copyright (c) 2023 Hangzhou Creator Network Co., Ltd.
# License: Sans, mailto:sans@kreator-inc.com
# @Desc    : Kreatornow Open Serivce Python SDK
# ------------------------------------------------------------------------

import hashlib
import json
import time

# Json Start #
def parse_json(json_str):
	"""
	json_str_parse
	:param json_str:
	:return: list/dict
	"""
	try:
		result = json.loads(json_str)
		return result
	except:
		return {}

def json_stringify(source):
	"""
	trans_to_json_str
	:param source: list/dict
	:return: string
	"""
	try:
		result = json.dumps(source, separators=(',', ':'), ensure_ascii=False)
		return result
	except:
		return ''

# Json End #

# encrypt start #
def md5(content, upper=False, lower=False):
	if upper:
		return hashlib.md5(content.encode("utf-8")).hexdigest().upper()
	if lower:
		return hashlib.md5(content.encode("utf-8")).hexdigest().lower()
	return hashlib.md5(content.encode("utf-8")).hexdigest()
# encrypt end #

def make_query_string(params):
	if isinstance(params, str):
		return params
	if not isinstance(params, dict):
		return ""
	query_string = []
	for key, value in params.items():
		query_string.append(str(key) + '=' + str(value))
	return '&'.join(query_string)

def now_stamp():
	return int(time.time())
