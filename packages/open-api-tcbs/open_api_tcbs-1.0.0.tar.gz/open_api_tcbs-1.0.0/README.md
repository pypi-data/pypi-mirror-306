1. Official document: https://developers.tcbs.com.vn/
2. Example call api:
```
import openapi.dto.derivative_dto.derivative_dto as derivative_dto
import openapi.dto.money.money as money_dto
import openapi.dto.stock_normal.stock_normal_dto as stock_normal_dto
import openapi.service.account.account as account_service
import openapi.service.authen.token as token_service
import openapi.service.derivative.derivative as derivative_service
import openapi.service.money.money as money_service
import openapi.service.stock_normal.normal as stock_service_service


def main():
    token = "xxx"
    api_key = "xxx"
    custody_code = "xxx"

    """
    # Rate limit 10 request/day. Please save token after call success
    # 2.1.1. Exchange API Key for JWT Token
    response_dto = token_service.get_token(api_key, "xxx")
    print(response_dto)
    """

    """
    # 3.1.1. Get account information
    response_dto = account_service.get_subaccount_info(custody_code, "basicInfo,personalInfo,bankSubAccounts,bankAccounts", token)
    print(response_dto)
    """

    """
    # 4.1.1. Transfer money internally
    # Create a request DTO
    request_dto = money_dto.TransferBetweenSubaccountRequestDTO(
        sourceAccountNumber="105C336655A",
        destinationAccountNumber="0001201435",
        amount=10000,
        description="CHUYEN TIEN PHAI SINH"
    )

    # Call the API
    response_dto = money_service.transfer_between_subaccounts(request_dto, token)
    print(response_dto)
    """

    """
    # 4.2.1. Withdrawal of margin
    # Create a request DTO
    request_dto = money_dto.WithdrawalDerivativeRequestDTO(
        accountId="105C336655",
        subAccountId="0001201435",
        amount=10000,
        paymentContent="RUT TIEN PHAI SINH"
    )

    # Call the API
    response_dto = money_service.withdrawal_margin(request_dto, token)
    print(response_dto)
    """

    """
    # 4.2.2. Deposit of margin
    # Create a request DTO
    request_dto = money_dto.DepositDerivativeRequestDTO(
        accountId="105C336655",
        subAccountId="0001201435",
        amount=10000,
        paymentContent="NAP TIEN KY QUY"
    )

    # Call the API
    response_dto = money_service.deposit_margin(request_dto, token)
    print(response_dto)
    """

    """
    # 5.1.1. Place order
    # Create a request DTO
    request_dto = stock_normal_dto.PlaceOrderExternalDto(
        execType="NS",
        price=1000,
        priceType="LO",
        quantity=100,
        symbol="FPT"
    )
    account_no: str = "0001201435"

    # Call the API
    response_dto = stock_service_service.place_order(request_dto, account_no, token)
    print(response_dto)
    """

    """
    # 5.2.1. Update order
    # Create a request DTO
    request_dto = stock_normal_dto.UpdateOrderRequestDto(
        price=1000,
        quantity=100
    )

    account_no: str = "0001201435"
    order_id: str = "9202205230000324355"

    # Call the API
    response_dto = stock_service_service.update_order(request_dto, account_no, order_id, token)
    print(response_dto)
    """

    """
    # 5.3.1. Cancel order
    # Create a request DTO
    request_dto = stock_normal_dto.CancelOrderRequestDto(
        ordersList=[
            stock_normal_dto.OrderIDResponse(orderID="9202205230000324355")
        ]
    )

    account_no: str = "0001201435"
    response_dto = stock_service_service.cancel_order(account_no, request_dto, token)
    print(response_dto)
    """

    """
    # 5.4.1. Get order
    account_no: str = "0001201435"
    response_dto = stock_service_service.get_orders(account_no, token)
    print(response_dto)
    """

    """
    # 5.4.2. Get order by Order ID
    account_no: str = "0001201435"
    order_id: str = "9202205230000324355"
    response_dto = stock_service_service.get_order(account_no, order_id, token)
    print(response_dto)
    """

    """
    # 5.4.3. Get order matching information
    account_no: str = "0001201435"
    response_dto = stock_service_service.get_command_match_information(account_no, token)
    print(response_dto)
    """

    """
    # 5.5.1. Get purchasing power
    account_no = "0001201435"
    response_dto = stock_service_service.get_purchasing_power(account_no, token)
    print(response_dto)
    """

    """
    # 5.5.2. Get purchasing power by symbol
    account_no = "0001201435"
    symbol = "FPT"
    response_dto = stock_service_service.get_purchasing_power_by_symbol(account_no, symbol, token)
    print(response_dto)
    """

    """
    # 5.5.3. Get purchasing power by symbol and price
    account_no = "0001201435"
    symbol = "FPT"
    price = 1000
    response_dto = stock_service_service.get_purchasing_power_by_symbol_and_price(account_no, symbol, price, token)
    print(response_dto)
    """

    """
    # 5.6.1. Get asset stock by sub account
    account_no = "0001201435"
    response_dto = stock_service_service.get_asset_stock_by_sub_account(account_no, token)
    print(response_dto)
    """

    """
    # 5.6.2. Get remain cash information
    account_no = "0001201435"
    response_dto = stock_service_service.get_cash_investment(account_no, token)
    print(response_dto)
    """

    """
    # 6.1.1. Money derivative
    account_id = "105C336655"
    sub_account_id = "105C336655A"
    get_type = "0"
    response_dto = derivative_service.get_total_cash_derivative(account_id, sub_account_id, get_type, token)
    print(response_dto)
    """

    """
    # 6.2.1. Asset, position close
    account_id = "105C336655"
    sub_account_id = "105C336655A"
    symbol = "FPT"
    page_no = 1
    page_size = 10
    response_dto = derivative_service.get_asset_position_close(account_id, sub_account_id, symbol, page_no, page_size, token)
    print(response_dto)
    """

    """
    # 6.2.2. Asset, position open
    account_id = "105C336655"
    sub_account_id = "105C336655A"
    response_dto = derivative_service.get_asset_position_open(account_id, sub_account_id, token)
    print(response_dto)
    """

    """
    # 6.3.1. Get list of orders
    account_id = "105C336655"
    page_no = 1
    page_size = 10
    symbol = "FPT"
    order_type = "ALL,ALL"
    status = "1"
    response_dto = derivative_service.get_list_order_normal(page_no, page_size, account_id, symbol, order_type, status, token)
    print(response_dto)
    """

    """
    # 6.3.2. Get list of conditional orders
    page_no = 1
    page_size = 10
    account_id = "105C336655"
    sub_account_id = "105C336655A"
    order_status = "0"
    order_type = ""
    symbol = "ALL,ALL"
    response_dto = derivative_service.get_list_order_condition(page_no, page_size, account_id, sub_account_id, order_status, order_type, symbol, token)
    print(response_dto)
    """

    """
    # 6.4.1. Place order
    # Create a request DTO
    accountId = "105C336655"
    subAccountId = "105C336655A"
    side = "B"
    symbol = "VN30F2103"
    price = 1
    volume = 1
    refId = "H.OWsC4418qYN59HXcvGtD3z"
    orderType = "0"
    request_dto = derivative_dto.PlaceOrderDto(accountId, subAccountId, side, symbol, price, volume, refId, orderType)
    response_dto = derivative_service.place_order(request_dto, token)
    print(response_dto)
    """

    """
    # 6.4.2. Conditional order
    # Create a request DTO
    accountId = "105C336655"
    subAccountId = "105C336655A"
    side = "B"
    symbol = "VN30F2110"
    price = 1
    volume = 1
    refId = "H.OWsC4418qYN59HXcvGtD3z"
    orderType = "SOL"
    callbackPoint = 0.1
    activationPrice = 1
    soPrice = 1
    request_dto = derivative_dto.OrderConditionDerivativeRequestDTO(subAccountId, accountId, side, symbol, price,
                                                                    volume, orderType, callbackPoint, activationPrice, soPrice, None, refId, None, None, None)

    response_dto = derivative_service.place_order_condition(request_dto, token)
    print(response_dto)
    """

    """
    # 6.5.1. Edit normal order
    # Create a request DTO
    accountId = "105C336655"
    subAccountId = "105C336655A"
    orderNo = "17"
    refId = "000123.H.HH2104062"
    nvol = 1
    nprice = 1

    request_dto = derivative_dto.EditOrderNormalDerivativeRequestDTO(accountId, subAccountId, orderNo, refId, nvol, nprice)
    response_dto = derivative_service.edit_place_order(request_dto, token)
    print(response_dto)
    """

    """
    # 6.5.2. Edit condition order
    # Create a request DTO
    accountId = "105C336655"
    pkOrderNo = "901938"
    type = ""
    refId = "000123.H.HH2104062"
    soPrice = 1

    request_dto = derivative_dto.EditOrderConditionDerivativeRequestDTO(accountId, pkOrderNo, type, refId, soPrice, None)
    response_dto = derivative_service.edit_place_order_condition(request_dto, token)
    print(response_dto)
    """

    """
    # 6.6.1. Cancel normal order
    # Create a request DTO
    accountId = "105C336655"
    orderNo = "901938"
    cmd = None
    refId = None
    pin = None

    request_dto = derivative_dto.CancelOrderNormalDerivativeRequestDTO(accountId, orderNo, cmd, pin, refId)
    response_dto = derivative_service.cancel_place_order(request_dto, token)
    print(response_dto)
    """

    """
    # 6.6.2. Cancel condition order
    # Create a request DTO
    accountId = "105C336655"
    orderNo = "901938"
    subAccountId = "105C336655A"

    request_dto = derivative_dto.CancelOrderConditionDerivativeRequestDTO(accountId, orderNo, subAccountId)
    response_dto = derivative_service.cancel_place_order_condition(request_dto, token)
    print(response_dto)
    """

    # """
    # 6.7.1. Symbol stock, price
    response_dto = derivative_service.market_information_bid_ask(token)
    print(response_dto)
    # """


if __name__ == "__main__":
    main()
```