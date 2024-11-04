from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class BasicInfo:
    tcbsId: Optional[str] = None
    code105C: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    depository: Optional[bool] = None

@dataclass
class PersonalInfo:
    fullName: Optional[str] = None
    fullNameNoAccent: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    contactAddress: Optional[str] = None
    permanentAddress: Optional[str] = None
    nationality: Optional[str] = None
    nationalityName: Optional[str] = None
    taxIdNumber: Optional[str] = None
    acronym: Optional[str] = None
    createdDate: Optional[str] = None
    updatedDate: Optional[str] = None
    flowOpenAccount: Optional[str] = None
    avatarUrl: Optional[str] = None
    businessType: Optional[str] = None
    ppBusinessType: Optional[str] = None
    ppBusinessField: Optional[str] = None
    ppBusinessTypeName: Optional[str] = None
    ppBusinessFieldName: Optional[str] = None
    identityCard: Optional[dict] = None

@dataclass
class BankAccount:
    accountNo: Optional[str] = None
    accountName: Optional[str] = None
    accountNameNoAccent: Optional[str] = None
    bankCode: Optional[str] = None
    bankName: Optional[str] = None
    branchCode: Optional[str] = None
    bankType: Optional[str] = None
    bankSys: Optional[str] = None
    authorized: Optional[bool] = None
    bankAccountType: Optional[str] = None

@dataclass
class BankSubAccount:
    accountNo: Optional[str] = None
    accountName: Optional[str] = None
    accountType: Optional[str] = None
    accountTypeName: Optional[str] = None
    status: Optional[str] = None
    isDefault: Optional[str] = None

@dataclass
class AccountInformationResponse:
    basicInfo: Optional[BasicInfo] = None
    personalInfo: Optional[PersonalInfo] = None
    bankAccounts: Optional[List[BankAccount]] = field(default_factory=list)
    bankSubAccounts: Optional[List[BankSubAccount]] = field(default_factory=list)