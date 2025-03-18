from fastapi import APIRouter
from pydantic import BaseModel
import api_database.process_data as dpg


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


router = APIRouter(tags=["pg"], prefix="/api")


@router.get("/tab01/get_unique_holding_date")
async def get_unique_holding_date():
    ds = dpg.get_unique_holding_date()
    return ds


@router.get("/tab01/get_unique_etf_code")
async def get_unique_etf_code():
    ds = dpg.get_unique_etf_code()
    return ds


@router.post("/tab02/get_stock")
async def get_stock(holdingdate: HoldingDate):
    ds = dpg.get_stock(holdingdate.holding_date)
    return ds


@router.post("/tab02/get_stock_counts")
async def get_stock_counts(holdingdate: HoldingDate):
    ds = dpg.get_stock_counts(holdingdate.holding_date)
    return ds


@router.post("/tab02/get_bond")
async def get_bond(holdingdate: HoldingDate):
    ds = dpg.get_bond(holdingdate.holding_date)
    return ds


@router.post("/tab02/get_cash")
async def get_cash(holdingdate: HoldingDate):
    ds = dpg.get_cash(holdingdate.holding_date)
    return ds


@router.post("/tab02/get_stock_by_industry")
async def get_stock_by_industry(holdingdate: HoldingDate):
    ds = dpg.get_stock_by_industry(holdingdate.holding_date)
    return ds


@router.post("/tab02/get_stock_by_etfs")
async def get_stock_by_etfs(holdingdate: HoldingDate):
    ds = dpg.get_stock_by_etfs(holdingdate.holding_date)
    return ds


@router.post("/tab02/get_top_stocks_in_etfs")
async def get_top_stocks_in_etfs(holdingdate: HoldingDate):
    ds = dpg.get_top_stocks_in_etfs(holdingdate.holding_date)
    return ds


@router.get("/tab03/get_unique_etf_code_string")
async def get_unique_etf_code_string():
    ds = dpg.get_unique_etf_code_string()
    return ds


@router.post("/tab03/get_compare_top_stocks_in_etf")
async def get_compare_top_stocks_in_etf(dropdownparams: DropdownParams):
    ds = dpg.get_compare_top_stocks_in_etf(
        dropdownparams.holding_date, dropdownparams.etf_code
    )
    return ds


@router.post("/tab04/get_etf_historical_close")
async def get_etf_historical_close(etfcode: EtfCode):
    ds = dpg.get_etf_historical_close(etfcode.etf_code)
    return ds


@router.post("/tab04/get_etf_code_by_scode")
async def get_etf_code_by_scode(scode: Scode):
    ds = dpg.get_etf_code_by_scode(scode.s_code)
    return ds


@router.post("/tab04/get_holding_percentage_and_amount")
async def get_holding_percentage_and_amount(scodeetf: ScodeEtf):
    ds = dpg.get_holding_percentage_and_amount(scodeetf.s_code, scodeetf.etf_code)
    return ds


@router.post("/tab05/chk_stock_in_db_latest")
async def chk_stock_in_db_latest(scode: Scode):
    ds = dpg.chk_stock_in_db_latest(scode.s_code)
    return ds


@router.post("/tab05/get_eft_holding_with_selected_stock")
async def get_eft_holding_with_selected_stock(scode: Scode):
    ds = dpg.get_eft_holding_with_selected_stock(scode.s_code)
    return ds
