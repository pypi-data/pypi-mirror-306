from dataclasses import dataclass
from typing import Optional, Generic, TypeVar, List

from dataclasses_json import dataclass_json

T = TypeVar('T')

@dataclass_json
@dataclass
class DerivativeResponse(Generic[T]):
    cmd: str
    rc: str
    rs: str
    oID: str
    data: T

@dataclass_json
@dataclass
class TotalCashDerivativeResponse:
    cash: Optional[float]
    stock: Optional[float]
    collateral: Optional[float]
    type: Optional[str]
    net: Optional[float]
    tyle: Optional[float]
    im: Optional[float]
    vm: Optional[float]
    dm: Optional[float]
    mr: Optional[float]
    avaiCash: Optional[float]
    avaiColla: Optional[float]
    vmunpay: Optional[float]
    info: Optional[str]
    color: Optional[str]
    vm_eod: Optional[float]
    others: Optional[float]
    tax: Optional[float]
    feeCTCK: Optional[float]
    feeHNX: Optional[float]
    cashWithdraw: Optional[float]
    tienbosung: Optional[float]
    cashavaiwithdraw: Optional[float]
    assets: Optional[float]
    nav: Optional[float]
    cashOut: Optional[float]
    unrelizeVM: Optional[float]
    feePos: Optional[float]
    feeMan: Optional[float]
    product: Optional[str]
    status: Optional[str]
    debt: Optional[float]
    w1: Optional[float]
    w2: Optional[float]
    limit: Optional[float]
    package: Optional[str]

@dataclass_json
@dataclass
class AssetPositionCloseDerivativeResponse:
    symbol: str
    side: str
    openPrice: float
    closePrice: float
    closePosition: str
    fee: float
    tax: float
    closeVM: float
    unrealize: float
    closePC: float
    time: str

@dataclass_json
@dataclass
class AssetPositionOpenDerivativeResponse:
    symbol: str
    im: str
    deliver: str
    receive: str
    net: int
    side: str
    account: str
    wasp: float
    wapb: float
    lastPrice: float
    imValue: float
    vmValue: float
    mrValue: float
    duedate: str
    netoffvol: int
    avg_remain: float
    vm_remain: float
    pc_remain: str
    stoploss: Optional[str]
    takeprofit: Optional[str]

@dataclass_json
@dataclass
class ListOrderNormalDerivativeResponse:
    orderNo: str
    pk_orderNo: str
    orderTime: str
    accountCode: str
    side: str
    symbol: str
    volume: int
    showPrice: float
    matchVolume: int
    matchPriceBQ: float
    status: str
    orderStatus: str
    channel: str
    group: str
    cancelTime: Optional[str]
    isCancel: bool
    isAmend: bool
    info: Optional[str]
    maxPrice: Optional[float]
    matchValue: Optional[float]
    quote: Optional[str]
    autoType: Optional[str]
    product: Optional[str]
    orderType: Optional[str]
    source: Optional[str]

@dataclass_json
@dataclass
class ListOrderConditionDerivativeResponse:
    orderNo: str
    groupOrder: str
    pk_orderNo: str
    accountCode: str
    side: str
    symbol: str
    showPrice: float
    volume: int
    condition: str
    result: str
    active_time: str
    send_time: str
    cancel_time: Optional[str]
    group: str
    channel: str
    maxPrice: Optional[float]
    soPrice: float
    orderType: str
    from_time: str
    exp_time: str
    status: str
    details: str
    notes: str

@dataclass_json
@dataclass
class OrderNormalDerivativeResponse:
    symbol: str
    status: str
    msg_type: str
    showPrice: float
    orderTime: str
    type: str
    accountCode: str
    orderNo: str
    matchVolume: float
    side: str
    volume: float
    pk_orderNo: str
    channel: str
    group: str
    quote: str
    accType: Optional[str] = None
    shareStatus: Optional[str] = None
    market: Optional[str] = None
    refID: Optional[str] = None
    autoType: Optional[str] = None
    product: Optional[str] = None

@dataclass
class PlaceOrderDto:
    accountId: str
    subAccountId: str
    side: str
    symbol: str
    price: float
    volume: int
    refId: str
    orderType: str
    advance: Optional[int] = None
    pin: Optional[str] = None

@dataclass
class OrderConditionDerivativeRequestDTO:
    subAccountId: str
    accountId: str
    side: str
    symbol: str
    price: str
    volume: str
    orderType: str
    callbackPoint: str
    activationPrice: str
    soPrice: str
    refId: str

@dataclass
class OrderConditionDerivativeRequestDTO:
    subAccountId: str
    accountId: str
    side: str
    symbol: str
    price: float
    volume: float
    orderType: str
    callbackPoint: float
    activationPrice: float
    soPrice: float
    advance: Optional[str] = None
    refId: Optional[str] = None
    pin: Optional[str] = None
    type: Optional[str] = None
    cmd: Optional[str] = None

@dataclass
@dataclass_json
class OrderConditionDerivativeResponseDTO:
    symbol: str
    status: str
    msg_type: str
    showPrice: float
    orderTime: str
    type: str
    accountCode: str
    orderNo: int
    matchVolume: float
    side: str
    volume: float
    pk_orderNo: str
    channel: str
    group: str
    quote: str
    shareStatus: Optional[str] = None
    market: Optional[str] = None
    refID: Optional[str] = None
    accType: Optional[str] = None
    autoType: Optional[str] = None
    product: Optional[str] = None

@dataclass
class EditOrderNormalDerivativeRequestDTO:
    accountId: str
    subAccountId: str
    orderNo: str
    refId: str
    nvol: float
    nprice: float

@dataclass
@dataclass_json
class EditOrderNormalDerivativeResponseDTO:
    orderNo: str
    msg_type: str
    status: str
    pk_orderNo: str
    volume: float
    showPrice: float

@dataclass
class EditOrderConditionDerivativeRequestDTO:
    accountId: str
    pkOrderNo: str
    type: str
    refId: str
    soPrice: float
    cmd: Optional[str] = None

@dataclass
@dataclass_json
class EditOrderConditionDerivativeResponseDTO:
    showPrice: str
    price: str
    volume: str
    pkOrderNo: str
    notes: str

@dataclass
class CancelOrderNormalDerivativeRequestDTO:
    accountId: str
    orderNo: str
    cmd: Optional[str] = None
    pin: Optional[str] = None
    refId: Optional[str] = None

@dataclass
@dataclass_json
class CancelOrderNormalDerivativeResponseDTO:
    orderNo: str
    msg_type: Optional[str] = None
    status: Optional[str] = None
    pk_orderNo: Optional[str] = None
    cancelTime: Optional[str] = None


@dataclass
class CancelOrderConditionDerivativeRequestDTO:
    accountId: str
    orderNo: str
    subAccountId: Optional[str] = None

@dataclass
@dataclass_json
class CancelOrderConditionDerivativeResponseDTO:
    pass

@dataclass
class MarketInformationDerivativeResponseDTO:
    symbol: Optional[str] = None
    ceilPrice: Optional[float] = None
    floorPrice: Optional[float] = None
    refPrice: Optional[float] = None
    bidPrice01: Optional[float] = None
    bidPrice02: Optional[float] = None
    bidPrice03: Optional[float] = None
    bidQtty01: Optional[float] = None
    bidQtty02: Optional[float] = None
    bidQtty03: Optional[float] = None
    offerPrice01: Optional[float] = None
    offerPrice02: Optional[float] = None
    offerPrice03: Optional[float] = None
    offerQtty01: Optional[float] = None
    offerQtty02: Optional[float] = None
    offerQtty03: Optional[float] = None
    matchPrice: Optional[float] = None
    matchQtty: Optional[float] = None
    change: Optional[float] = None
    changePercent: Optional[float] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    totalVol: Optional[float] = None
    openVol: Optional[float] = None
    buyForeignQtty: Optional[float] = None
    sellForeignQtty: Optional[float] = None
    expiryDate: Optional[str] = None
    avg: Optional[float] = None

@dataclass
class MarketInformationResponseDTO:
    data: List[MarketInformationDerivativeResponseDTO]