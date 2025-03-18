from dash import Dash
import dash_bootstrap_components as dbc
import layout as lyt
import callbacks


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = lyt.create_layout_container()

# Callbacks
callbacks.init_callbacks(app)


if __name__ == "__main__":    
    app.run()
    