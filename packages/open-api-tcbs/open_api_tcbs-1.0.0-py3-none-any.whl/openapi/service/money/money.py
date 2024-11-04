from dataclasses import asdict

import requests
from dacite import Config, from_dict

from openapi.dto.money import money
from openapi.utils import constant
from openapi.utils import request_api


# https://developers.tcbs.com.vn/#tag/money/operation/transfer_between_subaccount
# 4.1.1. Transfer money internally
def transfer_between_subaccounts(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/physis/v1/stock/transfer"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=money.TransferBetweenSubaccountResponseDTO, data=response_data, config=config)
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/money/operation/withdrawal_derivative
# 4.2.1. Withdrawal of margin
def withdrawal_margin(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/cash/withdraw/update"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=money.WithdrawalDerivativeResponseDTO, data=response_data, config=config)
    else:
        response.raise_for_status()

# https://developers.tcbs.com.vn/#tag/money/operation/deposit_derivative
# 4.2.2. Deposit of margin
def deposit_margin(request_dto, token):
    url = f"{constant.BASE_URL_PRODUCTION}/khronos/v1/cash/deposit/update"
    headers = request_api.get_headers(token)
    response = requests.post(url, json=asdict(request_dto), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        return from_dict(data_class=money.DepositDerivativeMarginResponseDTO, data=response_data, config=config)
    else:
        response.raise_for_status()