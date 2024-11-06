# ------------------------------------------------------------------------
# Copyright (c) 2023 Hangzhou Creator Network Co., Ltd.
# License: Sans, mailto:sans@kreator-inc.com
# @Desc    : Kreatornow Open Serivce Python SDK
# ------------------------------------------------------------------------


from kreatornow import utils
import copy
import requests

SERV_ADS = "cps-mesh.open.stores.plans.get"
SERV_LINKS = "cps-mesh.cpslink.links.post"
SERV_ORDER = "cps-mesh.open.orders.query.get"
SERV_ORDER_DETAIL = "cps-mesh.open.orders.detail.get"
SERV_ORDER_SETTLEMENT = "cps-mesh.open.orders.settlement.get"

VALID_SERV = [SERV_ADS, SERV_LINKS, SERV_ORDER, SERV_ORDER_DETAIL, SERV_ORDER_SETTLEMENT]

class Obj(dict):
	def __init__(self, d=None):
		if d is not None:
			for k, v in d.items():
				self[k] = v
		return super().__init__()

	def __key(self, key):
		return "" if key is None else key.lower()

	def __str__(self):
		import json
		return json.dumps(self)

	def __setattr__(self, key, value):
		self[self.__key(key)] = value

	def __getattr__(self, key):
		return self.get(self.__key(key))

	def __getitem__(self, key):
		return super().get(self.__key(key))

	def __setitem__(self, key, value):
		return super().__setitem__(self.__key(key), value)

	def __deepcopy__(self, memo):
		# Create a new instance of Obj
		copied_obj = Obj()
		# Copy each key and value deeply
		for k, v in self.items():
			copied_obj[k] = copy.deepcopy(v, memo)
		return copied_obj


DEFAULT_RESPONSE_ERR_DICT = Obj(
	{
		'url': '',
		'http_code': -1,
		'body': '',
		'text': '',
		'time_consuming': 0,
		'headers': {},
		'cookies': {}
	}
)


class Network:
	@staticmethod
	def post_request(url, data=None, headers=None, cookies=None, ssl=True):
		try:
			res = requests.session().post(url=url, data=data, headers=headers, cookies=cookies, timeout=60, verify=ssl)
			return Network.format_data(res, True)
		except requests.RequestException as e:
			req_err_dicts = copy.deepcopy(DEFAULT_RESPONSE_ERR_DICT)
			req_err_dicts.url = url
			req_err_dicts.body = "RequestError:" + str(e)
			req_err_dicts.text = "RequestError:" + str(e)
			return req_err_dicts
		except Exception as e:
			err_dicts = copy.deepcopy(DEFAULT_RESPONSE_ERR_DICT)
			err_dicts.url = url
			err_dicts.body = "Error:" + str(e)
			err_dicts.text = "Error:" + str(e)
			return err_dicts

	@staticmethod
	def format_data(source_data, parse_json_body=False):
		try:
			time_consuming = int(source_data.elapsed.total_seconds() * 1000)
			response_dicts = Obj({})
			response_dicts.url = source_data.url
			response_dicts.http_code = source_data.status_code
			response_dicts.body = source_data.content.decode(encoding='utf8')
			if parse_json_body:
				response_dicts.body = utils.parse_json(response_dicts.body)
			response_dicts.text = source_data.text
			response_dicts.time_consuming = time_consuming
			response_dicts.headers = source_data.headers
			response_dicts.cookies = source_data.cookies.get_dict()
			return response_dicts
		except Exception as e:
			err_dicts = copy.deepcopy(DEFAULT_RESPONSE_ERR_DICT)
			err_dicts.url = source_data.url
			err_dicts.body = "Error:" + str(e)
			err_dicts.text = "Error:" + str(e)
			return err_dicts


class Serv:
	ads = ""
	link = ""
	orders = ""
	orderdetail = ""
	settlement = ""


SERV_HOST = "https://open.kreatornow.com/apis"
SERV_HEADER = {"Content-Type": "application/json"}


class Creator:
	def __init__(self, app_key, app_secret):
		if app_key == "" or app_secret == "":
			raise Exception("Creator init need valid app_key and app_secret")
		self._set_app_key(app_key)
		self._set_app_secret(app_secret)
		self._response = None

	def _set_app_key(self, app_key):
		self._app_key = str(app_key)

	def get_app_key(self):
		"""
		get your app_key
		:return: string
		"""
		return self._app_key

	def _set_app_secret(self, app_secret):
		self._app_secret = str(app_secret)

	def get_app_secret(self):
		"""
		get your app_secret
		:return: string
		"""
		return self._app_secret

	def _set_response(self, response):
		self._response = response

	def _clear_response(self):
		self._set_response(None)

	def _get_sign(self, api_service, req_params):
		base_sign_data = {
			'app_key': self.get_app_key(),
			'timestamp': utils.now_stamp(),
			'service': api_service
		}
		base_sign_data = dict(sorted(base_sign_data.items()))
		b2s = ''.join([f'{k}{v}' for k, v in base_sign_data.items()])
		sign_str = self.get_app_secret() + b2s + utils.json_stringify(req_params) + self.get_app_secret()
		return base_sign_data, utils.md5(sign_str, upper=True)

	def send_client(self, api_service: str, params: dict):
		"""
		send once service request
		:param api_service: typeof str or variable, variable in get_ads,get_link,get_orders,get_order_detail,
		get_settlement any
		:param params : typeof dict, your request params
		:return: None
		"""
		self._clear_response()
		if api_service not in VALID_SERV:
			raise Exception("Not Supported Service")
		basic_params, sign = self._get_sign(api_service, params)
		basic_params.update({'sign': sign})
		request_url = SERV_HOST + '?' + utils.make_query_string(basic_params)
		self._set_response(Network.post_request(request_url, utils.json_stringify(params), SERV_HEADER))

	def get_result(self):
		"""
		get current request response if you send client,other will return None
		:return: DictObject or None
		"""
		result = copy.deepcopy(self._response)
		self._clear_response()
		return result






