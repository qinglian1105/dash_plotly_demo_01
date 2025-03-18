from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import api_mapping as apg
import datetime


HOLDING_DATES = apg.call_api("get_unique_holding_date")
INIT_DATE = HOLDING_DATES[0]["value"]
ETF_CODES = apg.call_api("get_unique_etf_code")
MARKDOWN_TEXT = "About more information of Taiwan ETFs, please refer to  \
                [Yahoo Finance (Taiwan)](<https://tw.stock.yahoo.com/tw-etf/total-assets>)"


def create_metric_card(card_id, title, value, change, color_class):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6(
                                    title,
                                    className="card-title text-muted mb-1 text-center",
                                ),
                                html.H5(
                                    value,
                                    className="card-text fw-bold text-center",
                                    id=f"card-{card_id}-value",
                                ),
                                html.H6(
                                    change,
                                    className="card-title text-muted mb-1 text-center",
                                    id=f"card-{card_id}-change",
                                ),
                            ],
                            className="col",
                        ),
                    ],
                    className="row align-items-center text-center",
                )
            ],
            className=f"text-{color_class}",
        )
    )


def overview_metric_row(choose_date):
    stock = apg.call_api("get_stock", choose_date)
    stock_counts = apg.call_api("get_stock_counts", choose_date)
    bond = apg.call_api("get_bond", choose_date)
    cash = apg.call_api("get_cash", choose_date)
    values = [stock["stock"], stock_counts["stock_counts"], bond["bond"], cash["cash"]]
    changes = [stock["change"], stock_counts["change"], bond["change"], cash["change"]]
    card_ids = ["one", "two", "three", "four"]
    titles = [
        "Stock - Market Value",
        "Stocks - Counts",
        "Bonds - Amount",
        "Cash - Amount",
    ]
    color_classs = ["primary", "success", "warning", "info"]
    variables = zip(card_ids, titles, values, changes, color_classs)
    cols = [
        dbc.Col(
            create_metric_card(
                card_id=card_id,
                title=title,
                value=value,
                change=change,
                color_class=color_class,
            ),
            width=3,
        )
        for card_id, title, value, change, color_class in variables
    ]
    return dbc.Row(cols)


def create_table_top_stocks(choose_date):
    stocks_in_etfs = apg.call_api("get_top_stocks_in_etfs", choose_date)
    table_id = "tb-stocks-in-etfs"
    columns = [{"name": k, "id": k} for k in stocks_in_etfs[0].keys()]
    style_header = {
        "backgroundColor": "#f7f9e9",
        "fontweight": "bold",
        "textAlign": "center",
    }
    style_cell = {"textAlign": "center"}
    style_cell_conditional = [
        {
            "if": {"column_id": "Market Value (M)"},
            "textAlign": "right",
        }
    ]
    return dash_table.DataTable(
        id=table_id,
        data=stocks_in_etfs,
        columns=columns,
        style_header=style_header,
        style_cell=style_cell,
        style_cell_conditional=style_cell_conditional,
    )


def create_table_stocks_ranking(choose_date, etf_code):
    table_id = "tb-stock-ranking"
    if etf_code == "all":
        etf_code = apg.call_api("get_unique_etf_code_string")["code_str"]
    else:
        etf_code = f"'{etf_code}'"

    stock_ranking = apg.call_api("get_compare_top_stocks_in_etf", choose_date, etf_code)
    columns = [{"name": k, "id": k} for k in stock_ranking[0].keys()]
    style_header = {
        "backgroundColor": "#e9f6f9",
        "fontWeight": "bold",
        "textAlign": "center",
    }
    style_cell = {"textAlign": "center"}
    style_data = {"fontSize": "14px"}
    cell_style_conditional = [
        {
            "if": {"column_id": c},
            "textAlign": "right",
        }
        for c in [
            "Price(p)",
            "MV",
            "Amount(t1)",
            "Amount(t0)",
            "▲(t1-t0)",
            "▲(p*(t1-t0))",
        ]
    ]
    cell_style_conditional.append(
        {
            "if": {"column_id": "Industry"},
            "textAlign": "left",
        }
    )
    style_data_conditional = [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#f6f6f6",
        }
    ]

    return dash_table.DataTable(
        id=table_id,
        data=stock_ranking,
        columns=columns,
        style_header=style_header,
        style_cell=style_cell,
        style_data=style_data,
        style_cell_conditional=cell_style_conditional,
        style_data_conditional=style_data_conditional,
    )


def make_empty_line(num):
    return html.Div([html.Br() for _ in range(num)])


def create_combo_chart(categories, bar_values, line_values, style_params):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=categories,
            y=bar_values,
            name=style_params["name_bar"],
            width=0.3,
            hovertemplate="Percent: %{y}%<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=categories,
            y=line_values,
            name=style_params["name_line"],
            yaxis="y2",
            hovertemplate="Amount: %{y:,.0f}張<extra></extra>",
        )
    )
    fig.update_layout(
        title={"text": style_params["title"], "xanchor": "center", "x": 0.5},
        xaxis={"type": "category"},
        yaxis={"title": style_params["y_01"]},
        yaxis2={"title": style_params["y_02"], "overlaying": "y", "side": "right"},
        legend={"yanchor": "top", "y": 1.25, "xanchor": "right", "x": 1},
        hovermode="x unified",
    )
    return fig


def introduction_summary():
    summary = apg.get_introduction_summary_text()
    return [
        make_empty_line(2),
        html.H4("About this study"),
        make_empty_line(1),
        html.P(summary[0]),
        html.P(summary[1]),
        html.P(summary[2]),
        make_empty_line(1),
    ]


def introduction_table_etf_info():
    etf_info = apg.get_introduction_etf_info()
    columns = [{"name": k, "id": k} for k in etf_info[0].keys()]
    style_header = {
        "backgroundColor": "#ffffcc",
        "fontWeight": "bold",
    }
    style_cell = {"textAlign": "center"}

    return dash_table.DataTable(
        data=etf_info, columns=columns, style_header=style_header, style_cell=style_cell
    )


def create_table_etf_holding_with_selected_stock(s_code):
    dss = apg.call_api("get_eft_holding_with_selected_stock", s_code)
    columns = [{"name": k, "id": k} for k in dss[0].keys()]
    style_header = {
        "backgroundColor": "#ffeecc",
        "fontWeight": "bold",
        "textAlign": "center",
    }
    style_cell = {"textAlign": "center"}
    style_data_conditional = [
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "#f6f6f6",
        }
    ]

    return dash_table.DataTable(
        data=dss,
        columns=columns,
        style_header=style_header,
        style_cell=style_cell,
        style_data_conditional=style_data_conditional,
    )


def create_tooltip_more_infomation(s_code=""):
    text_title = html.Span(
        f"More Information about '{s_code}'...",
        id="popover-target",
        style={
            "cursor": "pointer",
            "text-decoration": "underline",
            "color": "blue",
        },
    )

    tooltip_title = f"{s_code} - 請參考以下網站 (Click)"
    if s_code == "":
        text_title = html.Span("", id="popover-target")
        tooltip_body = []
    else:
        info = [
            {
                "website": "1. K線圖  (Yahoo Finance)",
                "link": f"https://tw.stock.yahoo.com/quote/{s_code}.TW/technical-analysis",
            },
            {
                "website": "2. 籌碼狀況  (Yahoo Finance)",
                "link": f"https://tw.stock.yahoo.com/quote/{s_code}.TW/institutional-trading",
            },
            {
                "website": "3. 網站討論  (股市爆料同學會)",
                "link": f"https://www.cmoney.tw/forum/stock/{s_code}?tab=discuss",
            },
        ]

        tooltip_body = []
        for i in info:
            tooltip_body.append(
                html.A(
                    i["website"],
                    href=i["link"],
                    target="_blank",
                    style={"color": "blue", "text-decoration": "underline"},
                )
            )
            tooltip_body.append(make_empty_line(1))

    return [
        make_empty_line(1),
        text_title,
        dbc.Popover(
            [
                dbc.PopoverHeader(
                    tooltip_title,
                    style={"background-color": "#E0FFFF", "font-size": "15px"},
                ),
                dbc.PopoverBody(tooltip_body),
            ],
            id="popover",
            target="popover-target",
            trigger="hover",
            placement="right",
            style={
                "font-size": "14px",
                "padding": "5px",
            },
        ),
    ]


def content_tab_one():
    return [
        dbc.Container(
            [
                # Part_01: text
                dbc.Row(
                    introduction_summary(),
                    className="mb-4",
                ),
                # Part_02: table
                dbc.Row(
                    html.H6(
                        "Date: 2025-03-07",
                        style={"textAlign": "right"},
                    ),
                    style={"width": "90%"},
                ),
                dbc.Row(
                    style={"width": "90%"},
                    children=[
                        introduction_table_etf_info(),
                        make_empty_line(1),
                        dcc.Markdown(MARKDOWN_TEXT),
                    ],
                ),
            ],
            className="mb-4",
        ),
    ]


def content_tab_two():
    return [
        dbc.Container(
            [
                # Part_01: date picker
                dbc.Row(
                    [
                        dbc.Row([make_empty_line(1)]),
                        dcc.DatePickerSingle(
                            id="date-picker",
                            display_format="YYYY-MM-DD",
                            date=INIT_DATE,
                        ),
                    ],
                    className="g-4 mb-4",
                ),
                # Part_02: metrics
                dbc.Row(
                    [
                        dbc.Row([make_empty_line(1)]),
                        overview_metric_row(INIT_DATE),
                    ],
                    className="g-4 mb-4",
                ),
                # Part_03: charts
                dbc.Row(
                    [
                        # Pie
                        dbc.Col(
                            dcc.Graph(id="pie-chart"),
                            width=6,
                        ),
                        # Bar
                        dbc.Col(
                            dcc.Graph(id="bar-chart"),
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),
                # Part_04: table
                dbc.Row(
                    [
                        html.Div(
                            children=[
                                make_empty_line(1),
                                html.H5(
                                    "Top stocks of ETFs",
                                    style={"textAlign": "center"},
                                ),
                                make_empty_line(1),
                                create_table_top_stocks(INIT_DATE),
                            ]
                        )
                    ],
                    className="g-4 mb-4",
                ),
            ]
        )
    ]


def content_tab_three():
    return [
        dbc.Container(
            [
                dbc.Row(
                    [
                        make_empty_line(1),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="dropdown-date",
                                    options=HOLDING_DATES,
                                    placeholder="Select Date",
                                    style={"textAlign": "left"},
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="dropdown-etf",
                                    options=ETF_CODES,
                                    placeholder="Select ETF code",
                                    style={"textAlign": "left"},
                                ),
                            ]
                        ),
                        dbc.Col(
                            [
                                dbc.Button(
                                    "Submit",
                                    id="button-query",
                                    outline=True,
                                    color="primary",
                                    className="me-1",
                                )
                            ]
                        ),
                    ],
                    style={"width": "70%", "display": "flex"},
                ),
                dbc.Row(
                    [
                        make_empty_line(1),
                        html.Div(
                            id="your-selection",
                            style={
                                "color": "red",
                                "fontSize": 16,
                                "vertical-align": "bottom",
                            },
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Row(
                            [
                                dbc.Col(make_empty_line(1)),
                                dbc.Col(
                                    "Unit: Million / TWD",
                                    style={"textAlign": "right"},
                                ),
                            ]
                        ),
                        dbc.Row(
                            html.Div(
                                children=create_table_stocks_ranking(INIT_DATE, "all")
                            )
                        ),
                    ]
                ),
                dbc.Row(),
            ],
            fluid=True,
        )
    ]


def content_tab_four():
    return [
        dbc.Container(
            [
                dbc.Row(
                    [
                        make_empty_line(1),
                        dcc.Dropdown(
                            id="dropdown-etfs",
                            options=ETF_CODES[1:],
                            value=ETF_CODES[1]["value"],
                            placeholder="Select ETF Code",
                            style={"textAlign": "left"},
                        ),
                    ],
                    style={"width": "35%", "display": "flex"},
                ),
                dbc.Row(
                    [
                        html.Div(
                            dcc.Graph(id="line-etf-price", style={"height": "35vh"})
                        )
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Input(
                                id="input-categories",
                                placeholder="Enter Security Code",
                                type="text",
                                style={
                                    "width": "70%",
                                    "height": "100%",
                                    "textAlign": "center",
                                },
                            )
                        ),
                        dbc.Col(
                            dcc.Dropdown(
                                id="dropdown-search-etf-by-scode",
                                placeholder="Select ETF Code",
                            ),
                        ),
                        dbc.Col(),
                    ],
                    style={"width": "90%", "display": "flex"},
                ),
                dbc.Row(
                    [
                        html.Div(
                            id="your-option-one",
                            style={
                                "color": "red",
                                "fontSize": 16,
                                "vertical-align": "bottom",
                            },
                        ),
                        html.Div(
                            id="your-option-two",
                            style={
                                "color": "red",
                                "fontSize": 16,
                                "vertical-align": "bottom",
                            },
                        ),
                    ]
                ),
                dbc.Row(
                    [html.Div(dcc.Graph(id="combo-chart", style={"height": "40vh"}))],
                    className="mb-4",
                ),
            ],
            fluid=True,
        )
    ]


def content_tab_five():
    return [
        dbc.Container(
            [
                dbc.Row(make_empty_line(1)),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Input(
                                id="input-individual-stock",
                                placeholder="Enter Security Code",
                                type="text",
                                style={
                                    "width": "100%",
                                    "height": "100%",
                                    "textAlign": "center",
                                },
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Submit",
                                id="button-individual-stock",
                                outline=True,
                                color="primary",
                                className="me-1",
                            )
                        ),
                        dbc.Col(),
                    ],
                    style={"width": "50%", "display": "flex"},
                ),
                dbc.Row(
                    [
                        make_empty_line(1),
                        html.Div(
                            id="your-scode",
                            style={
                                "color": "indigo",
                                "fontSize": 16,
                                "vertical-align": "bottom",
                            },
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        make_empty_line(2),
                        html.H4(
                            "Latest Infomation of selected stock",
                            style={"textAlign": "center"},
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(html.Hr()),
                dbc.Row(
                    [
                        html.H6("Trading Date:", style={"textAlign": "left"}),
                        html.H6("Security Code:", style={"textAlign": "left"}),
                        html.H6("Security Name:", style={"textAlign": "left"}),
                        html.H6("Closing Price:", style={"textAlign": "left"}),
                        make_empty_line(1),
                    ],
                    id="individual-stock-info",
                ),
                dbc.Row(
                    html.Div(id="tb-etf-holding-with-selected-stock"),
                    style={"width": "90%"},
                ),
                dbc.Row(
                    html.Div(
                        id="more-infomation-selected-stock",
                        children=create_tooltip_more_infomation(),
                    )
                ),
            ]
        )
    ]


def create_layout_container():
    return dbc.Container(
        [
            # Part_01: topic
            dbc.Row(
                [
                    dbc.Col(
                        html.H3(
                            "The Statistics of Top Equity ETFs in Taiwan",
                            className="text-center my-4 py-3",
                        ),
                        width=12,
                    )
                ]
            ),
            # Part_02: tabs
            dbc.Row(
                [
                    # Tabs
                    dbc.Tabs(
                        style={"font-size": "110%"},
                        children=[
                            # Tab one
                            dbc.Tab(
                                label="Introduction",
                                tab_id="tab-1",
                                children=content_tab_one(),
                            ),
                            # Tab one
                            dbc.Tab(
                                label="Overiew",
                                tab_id="tab-2",
                                children=content_tab_two(),
                            ),
                            # Tab three
                            dbc.Tab(
                                label="Top 30 Stocks",
                                tab_id="tab-3",
                                children=content_tab_three(),
                            ),
                            # Tab four
                            dbc.Tab(
                                label="Trend",
                                tab_id="tab-4",
                                children=content_tab_four(),
                            ),
                            # Tab five
                            dbc.Tab(
                                label="Individual Stocks",
                                tab_id="tab-5",
                                children=content_tab_five(),
                            ),
                        ],
                    )
                ]
            ),
        ]
    )
