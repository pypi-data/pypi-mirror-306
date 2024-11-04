from dataclasses import asdict

import requests
from dacite import Config, from_dict

from openapi.dto.stock_normal import stock_normal_dto
from openapi.utils import constant
from openapi.utils import request_api


# https://developers.tcbs.com.vn/#tag/order_stock_normal/operation/order
# 5.1.1. Place order
def place_order(request_dto, account_no, token):
    url = f"{constant.BASE_URL_PRODUCTION}/akhlys/v1/accounts/{account_no}/orders"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.PlaceOrderResponse, data=response_data, config=config)
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/update_order_stock_normal/operation/update_order_stock_normal
# 5.2.1. Update order
def update_order(request_dto, account_no, order_id, token):
    url = f"{constant.BASE_URL_PRODUCTION}/akhlys/v1/accounts/{account_no}/orders/{order_id}"
    headers = request_api.get_headers(token)
    response = requests.put(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.UpdateOrderResponse, data=response_data, config=config)
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/cancel_order_stock_normal/operation/cancel_order
# 5.3.1. Cancel order
def cancel_order(account_no, request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/akhlys/v1/accounts/{account_no}/cancel-orders"
    headers = request_api.get_headers(token)
    response = requests.put(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.CancelOrderResponse, data=response_data, config=config)
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/get_order_stock_normal/operation/get_order
# 5.4.1. Get order
def get_orders(account_no, token):
    url = f"{constant.BASE_URL_PRODUCTION}/aion/v1/accounts/{account_no}/orders"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.OrderSearchResponse, data=response_data, config=config)
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/get_order_stock_normal/operation/get_order_by_order_id
# 5.4.2. Get order by Order ID
def get_order(account_no, order_id, token):
    url = f"{constant.BASE_URL_PRODUCTION}/aion/v1/accounts/{account_no}/orders/{order_id}"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.OrderSearchResponse, data=response_data, config=config)
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/get_order_stock_normal/operation/get_command_match_information
# 5.4.3. Get order matching information
def get_command_match_information(account_no, token):
    url = f"{constant.BASE_URL_PRODUCTION}/aion/v1/accounts/{account_no}/orders"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.CommandMatchInformationResponse, data=response_data, config=config)
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/purchasing_power_stock_normal/operation/get_purchasing_power
# 5.5.1. Get purchasing power
def get_purchasing_power(account_no, token):
    url = f"{constant.BASE_URL_PRODUCTION}/aion/v1/accounts/{account_no}/ppse"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.Response, data=response_data, config=config)
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/purchasing_power_stock_normal/operation/get_purchasing_power_symbol
# 5.5.2. Get purchasing power by symbol
def get_purchasing_power_by_symbol(account_no, symbol, token):
    url = f"{constant.BASE_URL_PRODUCTION}/aion/v1/accounts/{account_no}/ppse/{symbol}"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.Response, data=response_data, config=config)
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/purchasing_power_stock_normal/operation/get_purchasing_power_symbol_price
# 5.5.3. Get purchasing power by symbol and price
def get_purchasing_power_by_symbol_and_price(account_no, symbol, price, token):
    url = f"{constant.BASE_URL_PRODUCTION}/aion/v1/accounts/{account_no}/ppse/{symbol}/{price}"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.Response, data=response_data, config=config)
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/get_asset_stock_normal/operation/get_asset
# 5.6.1. Get asset stock by sub account
def get_asset_stock_by_sub_account(account_no, token):
    url = f"{constant.BASE_URL_PRODUCTION}/aion/v1/accounts/{account_no}/se"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.SeInfoDTO, data=response_data, config=config)
    else:
        response.raise_for_status()
# https://developers.tcbs.com.vn/#tag/get_asset_stock_normal/operation/get_cash_investment
# 5.6.2. Get remain cash information
def get_cash_investment(account_no, token):
    url = f"{constant.BASE_URL_PRODUCTION}/aion/v1/accounts/{account_no}/cashInvestments"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=stock_normal_dto.CashInvestmentResponse, data=response_data, config=config)
    else:
        response.raise_for_status()
