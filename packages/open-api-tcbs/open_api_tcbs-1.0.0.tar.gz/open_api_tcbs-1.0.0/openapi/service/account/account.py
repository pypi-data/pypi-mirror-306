import requests
from dacite import from_dict, Config

from openapi.dto.account.account_information_response import AccountInformationResponse
from openapi.utils import constant
from openapi.utils import request_api

# https://developers.tcbs.com.vn/#tag/account/operation/get_sub_account_information
def get_subaccount_info(custody_code, fields, token):
    url = f"{constant.BASE_URL_PRODUCTION}/eros/v2/get-profile/by-username/{custody_code}"
    headers = request_api.get_headers(token)
    params = {
        "fields": fields
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        account_info_response = from_dict(data_class=AccountInformationResponse, data=response_data, config=config)
        return account_info_response
    else:
        response.raise_for_status()
