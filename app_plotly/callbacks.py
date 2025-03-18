from dash import html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import api_mapping as apg
import layout as lyt


def init_callbacks(app):
    @app.callback(
        [
            Output("card-one-value", "children"),
            Output("card-two-value", "children"),
            Output("card-three-value", "children"),
            Output("card-four-value", "children"),
            Output("card-one-change", "children"),
            Output("card-two-change", "children"),
            Output("card-three-change", "children"),
            Output("card-four-change", "children"),
            Output("pie-chart", "figure"),
            Output("bar-chart", "figure"),
            Output("tb-stocks-in-etfs", "data"),
        ],
        [Input("date-picker", "date")],
    )
    def update_tab_two(choose_date):
        stock = apg.call_api("get_stock", choose_date)
        stock_counts = apg.call_api("get_stock_counts", choose_date)
        bond = apg.call_api("get_bond", choose_date)
        cash = apg.call_api("get_cash", choose_date)

        industry = apg.call_api("get_stock_by_industry", choose_date)
        pie_figure = px.pie(
            values=industry["values"],
            names=industry["names"],
            title=industry["title"],
            hole=0.5,
        )

        by_etfs = apg.call_api("get_stock_by_etfs", choose_date)
        bar_figure = px.bar(
            by_etfs["df"],
            x=by_etfs["label"]["x"],
            y=by_etfs["label"]["y"],
            color=by_etfs["label"]["x"],
            title=by_etfs["title"],
        )

        stocks_in_etfs = apg.call_api("get_top_stocks_in_etfs", choose_date)

        return (
            stock["stock"],
            stock_counts["stock_counts"],
            bond["bond"],
            cash["cash"],
            stock["change"],
            stock_counts["change"],
            bond["change"],
            cash["change"],
            pie_figure,
            bar_figure,
            stocks_in_etfs,
        )

    @app.callback(
        Output("your-selection", "children"),
        Output("tb-stock-ranking", "data"),
        Input("button-query", "n_clicks"),
        State("dropdown-date", "value"),
        State("dropdown-etf", "value"),
        State("tb-stock-ranking", "data"),
        prevent_initial_call=True,
    )
    def update_tab_three(n_clicks, dropdown_date, dropdown_etf, existing_data):
        if dropdown_date is None or dropdown_etf is None:
            return "Please Select 'Date' and 'ETF code'...", existing_data
        else:
            if dropdown_etf == "all":
                etf_code = apg.call_api("get_unique_etf_code_string")["code_str"]
            else:
                etf_code = f"'{dropdown_etf}'"
            stock_ranking = apg.call_api(
                "get_compare_top_stocks_in_etf", dropdown_date, etf_code
            )
            return (
                f"Your Selection:  '{dropdown_date}',  '{dropdown_etf}'",
                stock_ranking,
            )

    @app.callback(
        Output("line-etf-price", "figure"),
        Input("dropdown-etfs", "value"),
    )
    def update_tab_four_etf_price(etf_code):
        ds = apg.call_api("get_etf_historical_close", etf_code)
        title = "The Price of ETF"
        xaxis = {"title": "Date", "type": "category"}
        yaxis = {"title": "Price"}
        figure_etf_price = {
            "data": [go.Scatter(x=ds["x"], y=ds["y"], name=ds["name"])],
            "layout": go.Layout(
                title=title, xaxis=xaxis, yaxis=yaxis, hovermode="x unified"
            ),
        }
        return figure_etf_price

    @app.callback(
        Output("dropdown-search-etf-by-scode", "options"),
        Input("input-categories", "value"),
        prevent_initial_call=True,
    )
    def update_tab_four_search_etf_by_scode(input_scode):
        results = apg.call_api("get_etf_code_by_scode", input_scode)
        return results

    @app.callback(
        Output("combo-chart", "figure"),
        State("input-categories", "value"),
        Input("dropdown-search-etf-by-scode", "value"),
        allow_duplicate=True,
        prevent_initial_call=True,
    )
    def update_tab_four_holding_percentage_by_scode(input_scode, input_etf):
        results = apg.call_api(
            "get_holding_percentage_and_amount", input_scode, input_etf
        )
        style_params = {
            "name_bar": "Holding Percentage",
            "name_line": "Holding Amount",
            "title": "Holding Percentage and Amount in ETF",
            "y_01": "Bar Value (%)",
            "y_02": "Line Value (Unit)",
        }
        figure_combo = lyt.create_combo_chart(
            results["category"],
            results["bar_value"],
            results["line_value"],
            style_params,
        )
        return figure_combo

    @app.callback(
        Output("your-scode", "children"),
        Output("individual-stock-info", "children"),
        Output("tb-etf-holding-with-selected-stock", "children"),
        Output("more-infomation-selected-stock", "children"),
        Input("button-individual-stock", "n_clicks"),
        State("input-individual-stock", "value"),
        allow_duplicate=True,
    )
    def update_tab_five_stock_info(n_clicks, input_scode):
        if not n_clicks:
            return ("↑ Please enter the stock code and then summit.", "", "", "")
        else:
            ds = apg.call_api("chk_stock_in_db_latest", input_scode)
            if ds is None:
                return (f"Sorry, '{input_scode}' not in DB. Please retry.", "", "", "")
            else:
                info = [
                    html.H6(
                        f"Trading Date: {ds['holding_date']}",
                        style={"textAlign": "left"},
                    ),
                    html.H6(
                        f"Security Code: {ds['s_code']}", style={"textAlign": "left"}
                    ),
                    html.H6(
                        f"Security Name: {ds['s_name']}", style={"textAlign": "left"}
                    ),
                    html.H6(
                        f"Closing Price: {ds['s_close']}", style={"textAlign": "left"}
                    ),
                    lyt.make_empty_line(1),
                ]
                tb = lyt.create_table_etf_holding_with_selected_stock(input_scode)
                tooltip_body = lyt.create_tooltip_more_infomation(input_scode)
                return (
                    f"The code you entered is  '{input_scode}'",
                    info,
                    tb,
                    tooltip_body,
                )
