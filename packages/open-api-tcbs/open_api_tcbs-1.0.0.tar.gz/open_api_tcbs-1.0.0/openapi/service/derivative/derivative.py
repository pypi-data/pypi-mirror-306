import json
from dataclasses import asdict

from dacite import Config, from_dict

from openapi.dto.derivative_dto import derivative_dto
from openapi.utils import constant
from openapi.utils import request_api
import requests
from typing import Optional

# https://developers.tcbs.com.vn/#tag/total_cash_derivative/operation/total_cash_derivative
# 6.1.1. Money derivative
def get_total_cash_derivative(account_id, sub_account_id, get_type, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/account/status"
    headers = request_api.get_headers(token)
    params = {
        "accountId": account_id,
        "subAccountId": sub_account_id,
        "getType": get_type
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.TotalCashDerivativeResponse].from_json(json.dumps(response_data))
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/asset_derivative/operation/asset_position_close_derivative
# 6.2.1. Asset, position close
def get_asset_position_close(account_id: str, sub_account_id: str, symbol: Optional[str], page_no: int, page_size: int, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/account/portfolio/position/close"
    headers = request_api.get_headers(token)
    params = {
        "accountId": account_id,
        "subAccountId": sub_account_id,
        "symbol": symbol,
        "pageNo": page_no,
        "pageSize": page_size
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.AssetPositionCloseDerivativeResponse].from_json(json.dumps(response_data))
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/asset_derivative/operation/asset_position_open_derivative
# 6.2.2. Asset, position open
def get_asset_position_open(account_id: str, sub_account_id: str, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/account/portfolio/status"
    headers = request_api.get_headers(token)
    params = {
        "accountId": account_id,
        "subAccountId": sub_account_id
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.AssetPositionOpenDerivativeResponse].from_json(json.dumps(response_data))
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/get_order_derivative/operation/list_order_normal_derivative
# 6.3.1. Get list of orders
def get_list_order_normal(page_no: int, page_size: int, account_id: str, symbol: str, order_type: str, status: str, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/order/in-day"
    headers = request_api.get_headers(token)
    params = {
        "pageNo": page_no,
        "pageSize": page_size,
        "accountId": account_id,
        "symbol": symbol,
        "orderType": order_type,
        "status": status
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.ListOrderNormalDerivativeResponse].from_json(json.dumps(response_data))
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/get_order_derivative/operation/list_order_condition_derivative
# 6.3.2. Get list of conditional orders
def get_list_order_condition(page_no: int, page_size: int, account_id: str, sub_account_id: str, order_status: str, order_type: str, symbol: str, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/order/condition/detail"
    headers = request_api.get_headers(token)
    params = {
        "pageNo": page_no,
        "PageSize": page_size,
        "accountId": account_id,
        "subAccountID": sub_account_id,
        "orderStatus": order_status,
        "orderType": order_type,
        "Symbol": symbol
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.ListOrderConditionDerivativeResponse].from_json(json.dumps(response_data))
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/order_derivative/operation/order_normal_derivative
# 6.4.1. Place order
def place_order(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/order/place"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.OrderNormalDerivativeResponse].from_json(json.dumps(response_data))
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/order_derivative/operation/order_condition_derivative
# 6.4.2. Conditional order
def place_order_condition(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/order/condition/place"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.OrderConditionDerivativeResponseDTO].from_json(json.dumps(response_data))
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/edit_order_derivative/operation/edit_order_normal_derivative
# 6.5.1. Edit normal order
def edit_place_order(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/order/change"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.EditOrderNormalDerivativeResponseDTO].from_json(json.dumps(response_data))
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/edit_order_derivative/operation/edit_order_condition_derivative
# 6.5.2. Edit condition order
def edit_place_order_condition(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v2/order/condition/change"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.EditOrderConditionDerivativeResponseDTO].from_json(json.dumps(response_data))
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/cancel_order_derivative/operation/cancel_order_normal_derivative
# 6.6.1. Cancel normal order
def cancel_place_order(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/order/cancel"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.CancelOrderNormalDerivativeResponseDTO].from_json(json.dumps(response_data))
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/cancel_order_derivative/operation/cancel_order_condition_derivative
# 6.6.2. Cancel condition order
def cancel_place_order_condition(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/order/condition/cancel"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        return derivative_dto.DerivativeResponse[derivative_dto.CancelOrderConditionDerivativeResponseDTO].from_json(json.dumps(response_data))
    else:
        print(response.json())
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/market_information_derivative/operation/get_order
# 6.7.1. Symbol stock, price
def market_information_bid_ask(token):
    url = f"{constant.BASE_URL_PRODUCTION}/tartarus/v1/derivatives"
    headers = request_api.get_headers(token)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=derivative_dto.MarketInformationResponseDTO, data=response_data, config=config)
    else:
        print(response.json())
        response.raise_for_status()
