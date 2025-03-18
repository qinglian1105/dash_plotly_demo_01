# SQL string


GET_COMPARE_TOP_STOCKS_IN_ETF = """
WITH tb_01 AS (
    SELECT
        s_code,
        s_name,
        industry_name
    FROM
        company_info
),
tb_02 AS (
    SELECT
        s_code,
        s_close,
        sum(holding_amount) AS holding_amount_t02,
        sum(s_close * holding_amount) AS mv
    FROM
        top_etf_holding
    WHERE
        unit = '股'
        AND holding_date IN ('{find_date}')
        AND etf_code IN ({etf_code})
    GROUP BY
        s_code,
        s_close
    ORDER BY
        mv DESC
    LIMIT
        30
), tb_03 AS (
    SELECT
        tb_02.s_code,
        tb_01.s_name,
        tb_01.industry_name,
        tb_02.s_close,
        tb_02.mv,
        tb_02.holding_amount_t02
    FROM
        tb_02
        LEFT JOIN tb_01 on tb_02.s_code = tb_01.s_code
    ORDER BY
        tb_02.mv DESC
),
tb_04 AS (
    SELECT
        s_code,
        sum(holding_amount) AS holding_amount_t01
    FROM
        top_etf_holding
    WHERE
        holding_date IN ('{previous_date}')
        AND etf_code IN ({etf_code})
        AND s_code IN (
            SELECT
                s_code
            FROM
                tb_03
        )
    GROUP BY
        s_code
),
tb_05 AS (
    SELECT
        tb_03.s_code,
        tb_03.s_name,
        tb_03.industry_name,
        tb_03.s_close,
        tb_03.mv,
        tb_03.holding_amount_t02,
        tb_04.holding_amount_t01,
        (
            tb_03.holding_amount_t02 - tb_04.holding_amount_t01
        ) AS change_amount,
        (
            tb_03.holding_amount_t02 - tb_04.holding_amount_t01
        ) * tb_03.s_close AS change_mv
    FROM
        tb_03
        LEFT JOIN tb_04 ON tb_03.s_code = tb_04.s_code
),
tb_06 AS (
    SELECT
        ROW_NUMBER() OVER (
            ORDER BY
                tb_05.change_amount DESC
        ) AS ranking_amount_buy,
        tb_05.s_code,
        tb_05.change_amount
    FROM
        tb_05
    ORDER BY
        tb_05.change_amount DESC
),
tb_07 AS (
    SELECT
        ROW_NUMBER() OVER (
            ORDER BY
                tb_05.change_mv DESC
        ) AS ranking_mv_buy,
        tb_05.s_code,
        tb_05.change_mv
    FROM
        tb_05
    ORDER BY
        tb_05.change_mv DESC
)
SELECT
    ROW_NUMBER() OVER (
        ORDER BY
            tb_05.mv DESC
    ) AS ranking_mv,
    tb_05.s_code,
    tb_05.s_name,
    tb_05.industry_name,
    tb_05.s_close,
    ROUND(tb_05.mv / 1000000) AS mv,
    ROUND(tb_05.holding_amount_t02 / 1000) AS holding_amount_t02,
    ROUND(tb_05.holding_amount_t01 / 1000) AS holding_amount_t01,
    ROUND(tb_05.change_amount / 1000) AS change_amount,
    tb_06.ranking_amount_buy,
    ROUND(tb_05.change_mv / 1000000) AS change_mv,
    tb_07.ranking_mv_buy
FROM
    tb_05
    LEFT JOIN tb_06 ON tb_05.s_code = tb_06.s_code
    LEFT JOIN tb_07 ON tb_05.s_code = tb_07.s_code
ORDER BY
    tb_05.mv DESC;
"""


GET_LAST_TWO_HODLING_DATE = """
SELECT DISTINCT
   holding_date
FROM
   top_etf_holding
ORDER BY
   holding_date DESC
LIMIT
   2;
"""


GET_STOCK = """
WITH MV AS (
    SELECT
        holding_date,
        s_code,
        (s_close * holding_amount) AS mv
    FROM
        public.top_etf_holding
    WHERE
        unit IN ('股')
)
SELECT
    MV.holding_date,
    sum(MV.mv) AS mv_s
FROM
    MV
WHERE
    holding_date <= '{}'
GROUP BY
    MV.holding_date
ORDER BY
    MV.holding_date DESC
LIMIT
    2;
"""

GET_STOCK_COUNTS = """
SELECT
   holding_date,
   count(DISTINCT s_code) AS counts
FROM
   top_etf_holding
WHERE
   unit IN ('股')
   AND holding_date <= '{}'
GROUP BY
   holding_date
ORDER BY
   holding_date DESC
LIMIT
   2;
"""

GET_BOND = """
SELECT
   holding_date,
   sum(holding_amount) AS amount
FROM
   top_etf_holding
WHERE
   s_code NOT IN (
      'M_NTD',
      'C_NTD',
      'RP_NTD',
      'DA_NTD',
      'PFUR_NTD',
      'RDI_NTD'
   )
   AND unit NOT IN ('口', '股')
   AND holding_date <= '{}'
GROUP BY
   holding_date
ORDER BY
   holding_date DESC
LIMIT
   2;
"""

GET_CASH = """
SELECT
   holding_date,
   sum(holding_amount) AS cash
from
   top_etf_holding
WHERE
   s_code IN ('C_NTD')
   AND holding_date <= '{}'
GROUP BY
   holding_date
ORDER BY
   holding_date DESC
LIMIT
   2;
"""


GET_STOCK_BY_INDUSTRY = """
WITH tb_01 AS (
    SELECT
        s_code,
        industry_code,
        industry_name
    FROM
        company_info
),
tb_02 AS (
    SELECT
        holding_date,
        top_etf_holding.s_code,
        (s_close * holding_amount) AS mv,
        tb_01.industry_name
    FROM
        top_etf_holding
        LEFT JOIN tb_01 on tb_01.s_code = top_etf_holding.s_code
    WHERE
        unit IN ('股')
)
SELECT
    tb_02.industry_name,
    sum(tb_02.mv) AS mv_industry
FROM
    tb_02
WHERE
    tb_02.holding_date = '{}'
GROUP BY
    tb_02.industry_name
ORDER BY
    mv_industry DESC;
"""

GET_STOCK_BY_ETFS = """
SELECT
   etf_code,
   sum((s_close * holding_amount)) AS mv_etf
FROM
   top_etf_holding
WHERE
   unit IN ('股')
   AND holding_date = '{}'
GROUP BY
   etf_code
ORDER BY
   mv_etf DESC;
"""

GET_TOP_STOCKS_IN_ETFS = """
WITH tb_01 AS (
    SELECT
        s_code,
        s_name,
        industry_code,
        industry_name
    FROM
        company_info
),
tb_02 AS (
    SELECT
        s_code,
        sum((s_close * holding_amount)) AS mv_s
    FROM
        top_etf_holding
    WHERE
        unit IN ('股')
        AND holding_date = '{}'
    GROUP BY
        s_code
)
SELECT
    tb_02.s_code,
    tb_01.s_name,
    tb_01.industry_name,
    tb_02.mv_s
FROM
    tb_02
    LEFT JOIN tb_01 on tb_01.s_code = tb_02.s_code
ORDER BY
    tb_02.mv_s desc
LIMIT
    10;
"""


GET_UNIQUE_HOLDING_DATE = """
SELECT DISTINCT
   holding_date
FROM
   top_etf_holding
ORDER BY
   holding_date DESC;
"""

GET_UNIQUE_ETF_CODE = """
SELECT DISTINCT
   etf_code,
   etf_name
FROM
   top_etf
ORDER BY
   etf_code ASC;
"""


GET_ETF_HISTORICAL_CLOSE = """
SELECT
   trading_date,
   etf_close
FROM
   top_etf
WHERE
   trading_date <= (
      SELECT
         trading_date
      FROM
         top_etf
      ORDER BY
         trading_date DESC
      LIMIT
         1
   )
   AND etf_code = '{}'
ORDER BY
   trading_date ASC;
"""


GET_HOLDING_PERCENTAGE_AND_AMOUNT = """
SELECT
   holding_date,   
   ROUND(holding_percentage * 100, 2),
   ROUND(SUM(holding_amount) / 1000) AS holding_amount
FROM
   top_etf_holding
WHERE
   unit = '股'
   AND holding_date <= (
      SELECT
         holding_date
      FROM
         top_etf_holding
      ORDER BY
         holding_date DESC
      LIMIT
         1
   )
   AND s_code = '{s_code}'
   AND etf_code = '{etf_code}'
GROUP BY
   holding_date,   
   holding_percentage
ORDER BY   
   holding_date ASC;
"""

GET_ETF_CODE_BY_SCODE = """
SELECT
   DISTINCT tb_01.etf_code,
   tb_02.etf_name
FROM
   top_etf_holding AS tb_01
   LEFT JOIN top_etf AS tb_02 ON tb_01.etf_code = tb_02.etf_code
WHERE
   unit = '股'
   AND holding_date <= (
      SELECT
         holding_date
      FROM
         top_etf_holding
      ORDER BY
         holding_date DESC
      LIMIT
         1
   )
   AND s_code = '{}';
"""


CHK_STOCK_IN_DB_LATEST = """
SELECT
   DISTINCT s_code
FROM
   top_etf_holding
WHERE
   unit = '股'
   AND s_code = '{}'
   AND holding_date = (
      SELECT
         holding_date
      FROM
         top_etf_holding
      ORDER BY
         holding_date DESC
      LIMIT
         1
   )
ORDER BY
   s_code ASC;
"""


GET_LATEST_TWO_CLOSE_BY_SCODE = """
SELECT
   DISTINCT tb_01.s_code,
   tb_02.s_name,
   tb_01.holding_date,
   tb_01.s_close
FROM
   top_etf_holding AS tb_01
   LEFT JOIN company_info AS tb_02 on tb_01.s_code = tb_02.s_code
WHERE
   tb_01.unit = '股'
   and tb_01.s_code = '{}'
   AND holding_date IN (
      SELECT
         DISTINCT holding_date
      FROM
         top_etf_holding
      ORDER BY
         holding_date DESC
      LIMIT
         2
   )
ORDER BY
   tb_01.holding_date DESC;
"""

GET_EFT_HOLDING_WITH_SELECTED_STOCK = """
WITH tb_01 AS (
   SELECT
      DISTINCT etf_code,
      etf_name
   FROM
      top_etf
),
tb_02 AS (
   SELECT
      etf_code,
      ROUND(holding_amount / 1000) AS holding_amount,
      ROUND(holding_percentage * 100, 2) AS holding_percentage
   FROM
      top_etf_holding
   WHERE
      s_code = '{}'
      AND unit IN ('股')
      AND holding_date = (
         SELECT
            holding_date
         FROM
            top_etf_holding
         ORDER BY
            holding_date DESC
         LIMIT
            1
      )
)
SELECT
   ROW_NUMBER() OVER (
      ORDER BY
         tb_02.holding_amount DESC
   ) AS num,
   tb_02.etf_code,
   tb_01.etf_name,
   tb_02.holding_amount,
   tb_02.holding_percentage
FROM
   tb_02
   LEFT JOIN tb_01 ON tb_02.etf_code = tb_01.etf_code
ORDER BY
   tb_02.holding_amount DESC;
"""
