from flask import Flask
from flask_mysqldb import MySQL
#from dash import Dash, html, dcc


server = Flask(__name__)


#app_dash = Dash(__name__, server=server, routes_pathname_prefix="/dash/")
#app_dash.layout = html.Div([html.H1('Hi there, I am app1 for dashboards')])
'''
app_dash.layout = html.Div([
        dcc.Textarea(
            id="textArea",
            value="teste"
        ),
        html.H2("Titulo"),
        html.A("Voltar ao site", href="http://127.0.0.1:5000/home_site"),
        dcc.Dropdown(
            id="dropdown",
            #options=[{"label": x, "value": x} for x in days],
            #value=days[0],
            clearable=False,
        ),
        dcc.Graph(id="bar-chart"),
    ])
'''
server.config.from_pyfile('config.py')
db = MySQL(server)

from views import *

if __name__ == '__main__':
    server.run(debug=True, port=5000)
