from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PlaceOrderExternalDto:
    execType: str
    price: int
    priceType: str
    quantity: int
    symbol: str

@dataclass
class PlaceOrderResponse:
    orderId: str
    error: str
    message: str

@dataclass
class UpdateOrderRequestDto:
    price: int
    quantity: int

@dataclass
class UpdateOrderResponse:
    orderId: str
    error: str
    message: str

@dataclass
class OrderIDResponse:
    orderID: str

@dataclass
class CancelOrderRequestDto:
    ordersList: List[OrderIDResponse]

@dataclass
class Detail:
    deleted: str
    errorCode: str
    errorMesage: str
    orderID: str

@dataclass
class DataX:
    details: List[Detail]
    object: str

@dataclass
class CancelOrderResponse:
    data: List[DataX]
    object: str
    pageIndex: int
    pageSize: int
    totalCount: int

@dataclass
class OrderInfo:
    object: str
    accountNo: str
    orderID: str
    execType: str
    orderQtty: float
    execQtty: float
    codeID: str
    symbol: str
    priceType: str
    txtime: str
    txdate: str
    expDate: str
    timeType: str
    orStatus: str
    feeAcr: float
    limitPrice: float
    cancelQtty: float
    remainQtty: float
    via: str
    quotePrice: float
    matchPrice: float
    tradePlace: str
    matchType: str
    isDisposal: str
    isCancel: str
    isAmend: str
    userName: str
    orsOrderID: str
    sectype: str
    isFOOrder: str
    odTimeStamp: str
    matchAmount: float
    mmType: str
    bRatio: float
    taxSellAmout: float

@dataclass
class OrderSearchResponse:
    object: str
    pageSize: int
    pageIndex: int
    totalCount: int
    data: Optional[List[OrderInfo]] = None

@dataclass
class CommandMatchInformationDetailResponse:
    orderId: str
    side: str
    symbol: str
    quoteQtty: int
    quotePrice: float
    tradeId: str
    qtty: int
    price: float
    timeExec: str

@dataclass
class CommandMatchInformationResponse:
    object: str
    totalCount: int
    pageSize: int
    pageIndex: int
    data: Optional[List[CommandMatchInformationDetailResponse]] = None

@dataclass
class Response:
    accountNo: str
    symbol: str
    price: float
    pp0: float
    ppse: float
    ppseref: float
    maxBuyQuantity: float
    realMaxBuyQuantity: float
    minBuyQuantity: float
    marginRatioLoan: str
    marginPriceLoan: str
    rateBrkS: float
    rateBrkB: float
    custodyID: Optional[str] = None

@dataclass
class StockHoldingInfo:
    symbol: str
    secType: str
    secTypeName: Optional[str]
    availableTrading: float
    mortgaged: float
    t0: float
    t1: float
    t2: float
    blocked: float
    securedQuantity: float
    sellRemain: float
    exercisedCA: float
    unexercisedCA: float
    stockDividend: float
    cashDividend: float
    waitForTrade: float
    waitForTransfer: float
    waitForWithdraw: float
    currentPrice: float
    costPrice: float
    sellExec: float
    totalQtty: float
    settlement: float

@dataclass
class SeInfoDTO:
    object: str
    accountNo: str
    custodyID: str
    fullName: str
    stock: List[StockHoldingInfo]

@dataclass
class IAInfo:
    partner: str
    available: float
    hold: float


@dataclass
class CashInvestmentInfo:
    object: str
    iaInfos: List[IAInfo]
    pp0forBF: float
    bankAvlBalanceBF: float
    bodBalance: float
    cashBalance: float
    accountNo: str
    custodyID: str
    fullName: str
    balance: float
    avlAdvanceAmount: float
    buyingAmount: float
    blockAmount: float
    cashDevident: float
    bankAvlBalance: float
    bankBlockAmount: float
    avlWithdraw: float
    pp0: float
    secureAmtPO: float
    bondBlockAmount: float
    mBlockAmount: float
    fundBlockAmount: float
    avalBondBlockAmount: float
    depoFee: float
    bCashDividend: float
    sCashDividend: float
    dsecured: float
    adused: float
    mrused: float

@dataclass
class CashInvestmentResponse:
    object: str
    totalCount: int
    pageSize: int
    pageIndex: int
    data: List[CashInvestmentInfo]