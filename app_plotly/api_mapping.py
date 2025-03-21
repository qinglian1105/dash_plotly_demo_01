import requests


HOST = "http://host.docker.internal:5008"

MAPS = {
    "get_unique_holding_date": {
        "part_path": "overview/get_unique_holding_date",
        "method": "get",
        "variables": [],
    },
    "get_unique_etf_code": {
        "part_path": "overview/get_unique_etf_code",
        "method": "get",
        "variables": [],
    },
    "get_stock": {
        "part_path": "overview/get_stock",
        "method": "post",
        "variables": ["holding_date"],
    },
    "get_stock_counts": {
        "part_path": "overview/get_stock_counts",
        "method": "post",
        "variables": ["holding_date"],
    },
    "get_bond": {
        "part_path": "overview/get_bond",
        "method": "post",
        "variables": ["holding_date"],
    },
    "get_cash": {
        "part_path": "overview/get_cash",
        "method": "post",
        "variables": ["holding_date"],
    },
    "get_stock_by_industry": {
        "part_path": "overview/get_stock_by_industry",
        "method": "post",
        "variables": ["holding_date"],
    },
    "get_stock_by_etfs": {
        "part_path": "overview/get_stock_by_etfs",
        "method": "post",
        "variables": ["holding_date"],
    },
    "get_top_stocks_in_etfs": {
        "part_path": "overview/get_top_stocks_in_etfs",
        "method": "post",
        "variables": ["holding_date"],
    },
    "get_unique_etf_code_string": {
        "part_path": "top_30_stocks/get_unique_etf_code_string",
        "method": "get",
        "variables": [],
    },
    "get_compare_top_stocks_in_etf": {
        "part_path": "top_30_stocks/get_compare_top_stocks_in_etf",
        "method": "post",
        "variables": ["holding_date", "etf_code"],
    },
    "get_etf_historical_close": {
        "part_path": "trend/get_etf_historical_close",
        "method": "post",
        "variables": ["etf_code"],
    },
    "get_etf_code_by_scode": {
        "part_path": "trend/get_etf_code_by_scode",
        "method": "post",
        "variables": ["s_code"],
    },
    "get_holding_percentage_and_amount": {
        "part_path": "trend/get_holding_percentage_and_amount",
        "method": "post",
        "variables": ["s_code", "etf_code"],
    },
    "chk_stock_in_db_latest": {
        "part_path": "individual_stocks/chk_stock_in_db_latest",
        "method": "post",
        "variables": ["s_code"],
    },
    "get_eft_holding_with_selected_stock": {
        "part_path": "individual_stocks/get_eft_holding_with_selected_stock",
        "method": "post",
        "variables": ["s_code"],
    },
    "get_top_stock_of_top_industry_of_etf": {
        "part_path": "industry_leading/get_top_stock_of_top_industry_of_etf",
        "method": "post",
        "variables": ["holding_date"],
    },
    "get_top_percentage_of_etf": {
        "part_path": "holding_of_etf/get_top_percentage_of_etf",
        "method": "post",
        "variables": ["holding_date"],
    },
}

INTRODUCTION_ETF_INFO = [
    {
        "Num": 1,
        "Security Code": "0050",
        "Security Name (CHT)": "元大台灣50",
        "Asset Value (B, TWD)": 472.79,
    },
    {
        "Num": 2,
        "Security Code": "00878",
        "Security Name (CHT)": "國泰永續高股息",
        "Asset Value (B, TWD)": 405.69,
    },
    {
        "Num": 3,
        "Security Code": "0056",
        "Security Name (CHT)": "元大高股息",
        "Asset Value (B, TWD)": 403.28,
    },
    {
        "Num": 4,
        "Security Code": "00919",
        "Security Name (CHT)": "群益台灣精選高息",
        "Asset Value (B, TWD)": 331.75,
    },
    {
        "Num": 5,
        "Security Code": "006208",
        "Security Name (CHT)": "富邦台50",
        "Asset Value (B, TWD)": 207.48,
    },
    {
        "Num": 6,
        "Security Code": "00929",
        "Security Name (CHT)": "復華台灣科技優息",
        "Asset Value (B, TWD)": 198.86,
    },
    {
        "Num": 7,
        "Security Code": "00940",
        "Security Name (CHT)": "元大台灣價值高息",
        "Asset Value (B, TWD)": 143.06,
    },
    {
        "Num": 8,
        "Security Code": "00713",
        "Security Name (CHT)": "元大台灣高息低波",
        "Asset Value (B, TWD)": 130.24,
    },
]

SUMMARY_TEXT = [
    "The main subject of this study is Equity ETFs in Taiwan's capital market, and some of them are Multi-Asset ETF.",
    "Besides, the second selection criteria is that asset size of the ETF exceeds NT$100 billion.",
    "Therefore, there are 8 ETFs that meet the conditions, and their information is shown in the table below.",
]


def call_api(gate, *args):
    params = MAPS[gate]
    url_api = f"{HOST}/api/{params['part_path']}"
    if params["method"] == "get":
        r = requests.get(url_api).json()
        return r
    else:
        dic = dict()
        for var, arg in zip(params["variables"], args):
            dic[var] = arg
        r = requests.post(url_api, json=dic).json()
        return r


def get_introduction_summary_text():
    return SUMMARY_TEXT


def get_introduction_etf_info():
    return INTRODUCTION_ETF_INFO
