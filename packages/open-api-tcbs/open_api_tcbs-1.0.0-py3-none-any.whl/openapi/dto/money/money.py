from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class TransferBetweenSubaccountRequestDTO:
    sourceAccountNumber: str
    destinationAccountNumber: str
    amount: float
    description: str

@dataclass
class TransferBetweenSubaccountResponseDTO:
    code: str
    message: str


@dataclass
class WithdrawalDerivativeRequestDTO:
    accountId: str
    subAccountId: str
    amount: float
    paymentContent: str

@dataclass
class WithdrawalDerivativeResponseDTO:
    cmd: str
    rc: str
    rs: str
    oID: str
    data: list

@dataclass
class DepositDerivativeRequestDTO:
    accountId: str
    subAccountId: str
    amount: float
    paymentContent: str

@dataclass
class DepositDerivativeResponseDTO:
    transactionId: str

@dataclass
class DepositDerivativeMarginResponseDTO:
    cmd: str
    rc: str
    rs: str
    oID: str
    data: List[DepositDerivativeResponseDTO]
