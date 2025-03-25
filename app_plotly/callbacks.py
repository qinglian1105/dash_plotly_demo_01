from dash import html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import api_mapping as apg
import layout as lyt


def init_callbacks(app):
    @app.callback(
        [
            Output("overivew-metrics", "children"),
            Output("pie-chart", "figure"),
            Output("bar-chart", "figure"),
            Output("tb-stocks-in-etfs", "data"),
        ],
        [Input("date-picker", "date")],
    )
    def update_tab_overview(choose_date):
        overview_metrics = lyt.overview_metric_row(choose_date)

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
            overview_metrics,
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
    def update_tab_top_30_stocks(n_clicks, dropdown_date, dropdown_etf, existing_data):
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
    def update_tab_trend_etf_price(etf_code):
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
    def update_tab_trend_search_etf_by_scode(input_scode):
        results = apg.call_api("get_etf_code_by_scode", input_scode)
        return results

    @app.callback(
        Output("combo-chart", "figure"),
        State("input-categories", "value"),
        Input("dropdown-search-etf-by-scode", "value"),
        allow_duplicate=True,
        prevent_initial_call=True,
    )
    def update_tab_trend_holding_percentage_by_scode(input_scode, input_etf):
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
    def update_tab_individual_stocks(n_clicks, input_scode):
        if not n_clicks:
            return ("↑ Please enter the stock code and then summit.", "", "", "")
        else:
            ds = apg.call_api("chk_stock_in_db_latest", input_scode)
            if ds is None:
                return (f"Sorry, '{input_scode}' not in DB. Please retry.", "", "", "")
            else:
                position = ds["s_close"].find("(")
                price = ds["s_close"][0 : position - 1]
                change = ds["s_close"][position + 1 : -1]
                if "▲" in ds["s_close"]:
                    sign_color = "#ff3300"
                elif "▼" in ds["s_close"]:
                    sign_color = "#009933"
                else:
                    sign_color = "#000000"

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
                    html.Div(
                        [
                            html.Span(
                                f"Closing Price: {price} (", style={"font-weight": 500}
                            ),
                            html.Span(
                                change, style={"color": sign_color, "font-weight": 500}
                            ),
                            html.Span(")", style={"font-weight": 500}),
                        ]
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

    @app.callback(
        Output("treemap-industry-leading", "figure"),
        Input("dropdown-date-industry-leading", "value"),
    )
    def update_tab_industry_leading(selected_date):
        ds = apg.call_api("get_top_stock_of_top_industry_of_etf", selected_date)
        fig = px.treemap(
            {
                "Industry": ds["industry_name"],
                "Stock": ds["s_name"],
                "Market Value": ds["mv"],
                "extra_01": ds["industry_name"],
                "extra_02": ds["rank"],
            },
            path=["Industry", "Stock"],
            values="Market Value",
            hover_data=["extra_01", "extra_02"],
        )

        fig.update_traces(
            hovertemplate="Name: %{label}<br>Industry: %{customdata[0]}<br>Rank: %{customdata[1]}<br>Marke Value: %{value} (百萬)<extra></extra>",
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Arial",
                namelength=0,
            ),
        )
        fig.update_layout(
            title={
                "text": f"Distribution by Industry by Market Value of ETFs Holding -  {selected_date}",
                "xanchor": "center",
                "x": 0.5,
            }
        )

        return fig

    @app.callback(
        Output("scatter-holding-of-etf", "figure"),
        Input("dropdown-date-holding-of-etf", "value"),
    )
    def update_tab_holding_of_etf(selected_date):
        ds = apg.call_api("get_top_percentage_of_etf", selected_date)
        fig = px.scatter(
            ds,
            x="ETF",
            y="Percentage(%)",
            color="Stock",
        )

        fig.update_traces(marker=dict(size=10))
        fig.update_layout(
            title={
                "text": f"Stock Holding Percentage of ETF ({selected_date})",
                "xanchor": "center",
                "x": 0.5,
            },
            scattermode="group",
            xaxis_title="ETF code",
            yaxis_title="Percentage (%)",
            legend_title="Stock Name",
            scattergap=0.3,
        )

        return fig
