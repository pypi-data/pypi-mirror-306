import requests
from dacite import Config, from_dict

from openapi.dto.authen.TokenResponseDto import TokenResponseDto
from openapi.utils import constant


# https://developers.tcbs.com.vn/#tag/authen/operation/get_token
# 2.1.1. Exchange API Key for JWT Token
def get_token(api_key, otp):
    url = f"{constant.BASE_URL_PRODUCTION}/gaia/v1/oauth2/openapi/token"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "apiKey": api_key,
        "otp": otp
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        config = Config(strict=False)
        account_info_response = from_dict(data_class=TokenResponseDto, data=response_data, config=config)
        return account_info_response
    else:
        print(response.json())
        response.raise_for_status()
