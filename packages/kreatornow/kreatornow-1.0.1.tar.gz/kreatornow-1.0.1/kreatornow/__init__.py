# ------------------------------------------------------------------------
# Copyright (c) 2023 Hangzhou Creator Network Co., Ltd.
# License: Sans, mailto:sans@kreator-inc.com
# @Desc    : Kreatornow Open Serivce Python SDK
# ------------------------------------------------------------------------

from kreatornow.kreatornow import *

# ------------------------------------------------------------------------------
# define the supported service
# ------------------------------------------------------------------------------
kreatornow.Serv.ads = SERV_ADS
kreatornow.Serv.link = SERV_LINKS
kreatornow.Serv.orders = SERV_ORDER
kreatornow.Serv.orderdetail = SERV_ORDER_DETAIL
kreatornow.Serv.settlement = SERV_ORDER_SETTLEMENT
get_ads = kreatornow.Serv.ads
get_link = kreatornow.Serv.link
get_orders = kreatornow.Serv.orders
get_order_detail = kreatornow.Serv.orderdetail
get_settlement = kreatornow.Serv.settlement

# ------------------------------------------------------------------------------
# include utils
# ------------------------------------------------------------------------------
kreatornow.parse_json = kreatornow.utils.parse_json
kreatornow.json_stringify = kreatornow.utils.json_stringify
kreatornow.md5 = kreatornow.utils.md5
kreatornow.make_query_string = kreatornow.utils.make_query_string
kreatornow.now_stamp = kreatornow.utils.now_stamp
