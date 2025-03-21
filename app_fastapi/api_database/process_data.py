from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import api_database.sql_strings as sq
import os
import psycopg2


ENV_PATH = os.path.join(os.getcwd())
ENV_FILE = ".env.dev"
ENV_FILE_PATH = os.path.join(ENV_PATH, ENV_FILE)
load_dotenv(ENV_FILE_PATH)
HOST = os.environ.get("PG_HOST")
DBNAME = os.environ.get("PG_DBNAME")
USER = os.environ.get("PG_USER")
PASSWORD = os.environ.get("PG_PASSWORD")
PORT = os.environ.get("PG_PORT")
CONN_STR = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"


def get_connection(host, dbname, user, password, port):
    conn = psycopg2.connect(
        database=dbname, user=user, password=password, host=host, port=port
    )
    return conn


def get_change(figure_t02, figure_t01):
    if figure_t01 == figure_t02:
        return "0%"
    elif figure_t02 < figure_t01:
        change = f"▼ {round(abs(((figure_t02 - figure_t01) / figure_t01) * 100), 2)}%"
        return change
    else:
        change = f"▲ {round(((figure_t02 - figure_t01) / figure_t01) * 100, 2)}%"
        return change


def get_unique_etf_code_string():
    dss = get_unique_etf_code()
    etf_code_str = ""
    for ds in dss:
        etf_code_str = etf_code_str + f"""'{ds["value"]}',"""
    return {"code_str": etf_code_str[:-1]}


def get_last_two_hodling_date():
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_LAST_TWO_HODLING_DATE
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["holding_date"] = row[0]
            dss.append(ds)

        res = {"date_02": dss[0]["holding_date"], "date_01": dss[1]["holding_date"]}
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_date_before_date(search_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = """SELECT DISTINCT holding_date 
                     FROM top_etf_holding  
                     ORDER BY holding_date DESC;"""
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            dss.append(row[0])

        for idx, ds in enumerate(dss):
            if ds == search_date:
                break

        res = {"date_02": dss[idx], "date_01": dss[idx + 1]}

        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_stock(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_STOCK.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["holding_date"] = row[0]
            ds["amount"] = row[1]
            dss.append(ds)

        t02 = dss[0]["amount"]
        t01 = dss[1]["amount"]
        change = get_change(t02, t01)
        unit = 1000000
        res = {"stock": f"{round(t02 / unit, 0):,.0f} (M)", "change": change}
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_stock_counts(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_STOCK_COUNTS.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["holding_date"] = row[0]
            ds["amount"] = row[1]
            dss.append(ds)

        t02 = dss[0]["amount"]
        t01 = dss[1]["amount"]
        change = get_change(t02, t01)
        res = {"stock_counts": t02, "change": change}
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_bond(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_BOND.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["holding_date"] = row[0]
            ds["amount"] = row[1]
            dss.append(ds)

        t02 = dss[0]["amount"]
        t01 = dss[1]["amount"]
        change = get_change(t02, t01)
        unit = 1000000
        res = {"bond": f"{round(t02 / unit, 0):,.0f} (M)", "change": change}
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_cash(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_CASH.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["holding_date"] = row[0]
            ds["amount"] = row[1]
            dss.append(ds)

        t02 = dss[0]["amount"]
        t01 = dss[1]["amount"]
        change = get_change(t02, t01)
        unit = 1000000
        res = {"cash": f"{round(t02 / unit, 0):,.0f} (M)", "change": change}
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_stock_by_industry(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_STOCK_BY_INDUSTRY.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        unit = 1000000
        names = []
        values = []
        for row in rows:
            names.append(row[0])
            values.append(round(row[1] / unit, 0))

        other = sum(values[15:])
        names = names[0:15]
        values = values[0:15]
        names.append("其他")
        values.append(other)
        title = "Stock Investment Industry Distribution"
        res = {"names": names, "values": values, "title": title}
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_stock_by_etfs(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_STOCK_BY_ETFS.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        unit = 1
        names = []
        values = []
        for row in rows:
            names.append(row[0])
            values.append(round(row[1] / unit, 0))

        title = "Market Value (stock) of ETF"
        label = {"x": "ETF Code", "y": "Market Value"}
        df = pd.DataFrame({label["x"]: names, label["y"]: values})
        res = {"df": df, "title": title, "label": label}
        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_top_stocks_in_etfs(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_TOP_STOCKS_IN_ETFS.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        unit = 1000000
        dss = []
        for idx, row in enumerate(rows):
            ds = dict()
            ds["Num"] = idx + 1
            ds["Security Code"] = row[0]
            ds["Security Name"] = row[1]
            ds["Industry Name"] = row[2]
            ds["Market Value (M)"] = f"{round(row[3] / unit, 0):,.0f}"
            dss.append(ds)

        return dss
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_unique_holding_date():
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_UNIQUE_HOLDING_DATE
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["label"] = row[0]
            ds["value"] = row[0]
            dss.append(ds)

        return dss
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_unique_etf_code():
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_UNIQUE_ETF_CODE
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["label"] = f"{row[0]} - {row[1]}"
            ds["value"] = row[0]
            dss.append(ds)

        dss.insert(0, {"label": "All", "value": "all"})

        return dss
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_compare_top_stocks_in_etf(holding_date, etf_code):
    try:
        dates = get_date_before_date(holding_date)
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_COMPARE_TOP_STOCKS_IN_ETF.format(
            find_date=dates["date_02"],
            etf_code=etf_code,
            previous_date=dates["date_01"],
        )
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["Num"] = row[0]
            ds["Code"] = row[1]
            ds["Name"] = row[2]
            ds["Industry"] = row[3]
            ds["Price(p)"] = f"{row[4]:,.0f}" if row[4] > 499 else f"{row[4]:,.2f}"
            ds["MV"] = f"{row[5]:,.0f}"
            ds["Amount(t1)"] = f"{row[6]:,.0f}"
            ds["Amount(t0)"] = f"{row[7]:,.0f}"
            ds["▲(t1-t0)"] = f"{row[8]:,.0f}"
            ds["Ranking_1"] = row[9]
            ds["▲(p*(t1-t0))"] = f"{row[10]:,.0f}"
            ds["Ranking_2"] = row[11]
            dss.append(ds)

        return dss
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_etf_historical_close(etf_code):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_ETF_HISTORICAL_CLOSE.format(etf_code)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        trading_dates = []
        etf_closes = []
        for row in rows:
            trading_dates.append(row[0])
            etf_closes.append(row[1])

        name = "Price"
        dss = {"x": trading_dates, "y": etf_closes, "name": name}
        return dss
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_etf_code_by_scode(s_code):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_ETF_CODE_BY_SCODE.format(s_code)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        dss = []
        for row in rows:
            ds = dict()
            ds["label"] = f"{row[0]} - {row[1]}"
            ds["value"] = row[0]
            dss.append(ds)

        return dss
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_holding_percentage_and_amount(s_code, etf_code):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_HOLDING_PERCENTAGE_AND_AMOUNT.format(
            s_code=s_code, etf_code=etf_code
        )
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        categories = []
        bar_values = []
        line_values = []
        for row in rows:
            categories.append(row[0])
            bar_values.append(row[1])
            line_values.append(row[2])

        results = {
            "category": categories,
            "bar_value": bar_values,
            "line_value": line_values,
        }

        return results
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_change_results(figure_t02, figure_t01):
    diff = figure_t02 - figure_t01
    if figure_t02 > 499:
        diff = round(diff, 0)
        closing = f"{figure_t02:,.0f}"
    elif figure_t02 > 49:
        diff = round(diff, 1)
        closing = f"{figure_t02:,.1f}"
    else:
        diff = round(diff, 2)
        closing = f"{figure_t02:,.2f}"

    if diff == 0:
        return f" {figure_t02}  (0, 0%)"
    elif diff < 0:
        change = f" {closing}  ({diff}, ▼{round(abs(((figure_t02 - figure_t01) / figure_t01) * 100), 2)}%)"
        return change
    else:
        change = f" {closing}  (+{diff}, ▲{round(((figure_t02 - figure_t01) / figure_t01) * 100, 2)}%)"
        return change


def chk_stock_in_db_latest(s_code):
    try:
        engine = create_engine(CONN_STR, echo=False)
        sql_str = sq.CHK_STOCK_IN_DB_LATEST.format(s_code)
        ds = pd.read_sql(sql_str, engine)
        if ds is None:
            return None
        else:
            sql_str = sq.GET_LATEST_TWO_CLOSE_BY_SCODE.format(s_code)
            ds = pd.read_sql(sql_str, engine)
            if len(ds) < 2:
                changes = f"{ds['s_close'][0]}, (New)"
                result = {
                    "holding_date": ds["holding_date"][0],
                    "s_code": s_code,
                    "s_name": ds["s_name"][0],
                    "s_close": changes,
                }
                return result
            else:
                changes = get_change_results(ds["s_close"][0], ds["s_close"][1])
                result = {
                    "holding_date": ds["holding_date"][0],
                    "s_code": s_code,
                    "s_name": ds["s_name"][0],
                    "s_close": changes,
                }
                return result
    except Exception as e:
        print(e)
    finally:
        engine.dispose()


def get_eft_holding_with_selected_stock(s_code):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_EFT_HOLDING_WITH_SELECTED_STOCK.format(s_code)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        total_amount = 0
        dss = []
        for row in rows:
            ds = dict()
            ds["Num"] = row[0]
            ds["ETF Code"] = row[1]
            ds["ETF Name"] = row[2]
            ds["Holding Amount (Board lot/張數)"] = f"{row[3]:,.0f}"
            ds["Holding Percentage (%)"] = f"{row[4]:,.2f}"
            dss.append(ds)
            total_amount = total_amount + row[3]

        dss.append(
            {
                "Nnu": "",
                "ETF Code": "",
                "ETF Name": "Total",
                "Holding Amount (Board lot/張數)": f"{total_amount:,.0f}",
                "Holding Percentage (%)": "-",
            }
        )
        return dss
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_top_percentage_of_etf(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_TOP_PERCENTAGE_OF_ETF.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        etf_codes = []
        s_codes = []
        percentages = []
        for row in rows:
            etf_codes.append(row[0])
            s_codes.append(row[1])
            percentages.append(row[2])

        res = {
            "ETF": etf_codes,
            "Stock": s_codes,
            "Percentage(%)": percentages,
        }

        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def get_top_stock_of_top_industry_of_etf(holding_date):
    try:
        conn = get_connection(HOST, DBNAME, USER, PASSWORD, PORT)
        cursor = conn.cursor()
        sql_str = sq.GET_TOP_STOCK_OF_TOP_INDUSTRY_OF_ETF.format(holding_date)
        cursor.execute(sql_str)
        rows = cursor.fetchall()

        industry_names = []
        s_codes = []
        s_names = []
        holdings = []
        mvs = []
        ranks = []
        for row in rows:
            industry_names.append(row[0])
            s_codes.append(row[1])
            s_names.append(row[2])
            holdings.append(row[3])
            mvs.append(round(row[4] / 1000000, 0))
            ranks.append(row[5])

        res = {
            "industry_name": industry_names,
            "s_code": s_codes,
            "s_name": s_names,
            "holding": holdings,
            "mv": mvs,
            "rank": ranks,
        }

        return res
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
