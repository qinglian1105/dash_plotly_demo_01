from fastapi import APIRouter
import api_database.process_data as dpg
from api_gate.schema import HoldingDate, DropdownParams, EtfCode, Scode, ScodeEtf


router = APIRouter(tags=["pg"], prefix="/api")


@router.get("/overview/get_unique_holding_date")
async def get_unique_holding_date():
    ds = dpg.get_unique_holding_date()
    return ds


@router.get("/overview/get_unique_etf_code")
async def get_unique_etf_code():
    ds = dpg.get_unique_etf_code()
    return ds


@router.post("/overview/get_stock")
async def get_stock(holdingdate: HoldingDate):
    ds = dpg.get_stock(holdingdate.holding_date)
    return ds


@router.post("/overview/get_stock_counts")
async def get_stock_counts(holdingdate: HoldingDate):
    ds = dpg.get_stock_counts(holdingdate.holding_date)
    return ds


@router.post("/overview/get_bond")
async def get_bond(holdingdate: HoldingDate):
    ds = dpg.get_bond(holdingdate.holding_date)
    return ds


@router.post("/overview/get_cash")
async def get_cash(holdingdate: HoldingDate):
    ds = dpg.get_cash(holdingdate.holding_date)
    return ds


@router.post("/overview/get_stock_by_industry")
async def get_stock_by_industry(holdingdate: HoldingDate):
    ds = dpg.get_stock_by_industry(holdingdate.holding_date)
    return ds


@router.post("/overview/get_stock_by_etfs")
async def get_stock_by_etfs(holdingdate: HoldingDate):
    ds = dpg.get_stock_by_etfs(holdingdate.holding_date)
    return ds


@router.post("/overview/get_top_stocks_in_etfs")
async def get_top_stocks_in_etfs(holdingdate: HoldingDate):
    ds = dpg.get_top_stocks_in_etfs(holdingdate.holding_date)
    return ds


@router.get("/top_30_stocks/get_unique_etf_code_string")
async def get_unique_etf_code_string():
    ds = dpg.get_unique_etf_code_string()
    return ds


@router.post("/top_30_stocks/get_compare_top_stocks_in_etf")
async def get_compare_top_stocks_in_etf(dropdownparams: DropdownParams):
    ds = dpg.get_compare_top_stocks_in_etf(
        dropdownparams.holding_date, dropdownparams.etf_code
    )
    return ds


@router.post("/trend/get_etf_historical_close")
async def get_etf_historical_close(etfcode: EtfCode):
    ds = dpg.get_etf_historical_close(etfcode.etf_code)
    return ds


@router.post("/trend/get_etf_code_by_scode")
async def get_etf_code_by_scode(scode: Scode):
    ds = dpg.get_etf_code_by_scode(scode.s_code)
    return ds


@router.post("/trend/get_holding_percentage_and_amount")
async def get_holding_percentage_and_amount(scodeetf: ScodeEtf):
    ds = dpg.get_holding_percentage_and_amount(scodeetf.s_code, scodeetf.etf_code)
    return ds


@router.post("/individual_stocks/chk_stock_in_db_latest")
async def chk_stock_in_db_latest(scode: Scode):
    ds = dpg.chk_stock_in_db_latest(scode.s_code)
    return ds


@router.post("/individual_stocks/get_eft_holding_with_selected_stock")
async def get_eft_holding_with_selected_stock(scode: Scode):
    ds = dpg.get_eft_holding_with_selected_stock(scode.s_code)
    return ds


@router.post("/industry_leading/get_top_stock_of_top_industry_of_etf")
async def get_industry_leading(holdingdate: HoldingDate):
    ds = dpg.get_top_stock_of_top_industry_of_etf(holdingdate.holding_date)
    return ds


@router.post("/holding_of_etf/get_top_percentage_of_etf")
async def get_holding_of_etf(holdingdate: HoldingDate):
    ds = dpg.get_top_percentage_of_etf(holdingdate.holding_date)
    return ds
