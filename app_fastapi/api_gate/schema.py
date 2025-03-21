from pydantic import BaseModel


class HoldingDate(BaseModel):
    holding_date: str


class DropdownParams(BaseModel):
    holding_date: str
    etf_code: str


class EtfCode(BaseModel):
    etf_code: str


class Scode(BaseModel):
    s_code: str


class ScodeEtf(BaseModel):
    s_code: str
    etf_code: str
