import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from yahoo_fin import stock_info as si

import datetime 
import pytz

app = dash.Dash(__name__)
server = app.server

price_l = {}
time_l = []
stock_l = []

tickers = si.tickers_nasdaq(True)
tickers = tickers[['Symbol', 'Security Name']][0:-1]
op_l = []
for i in range(len(tickers)):
    temp_dic = {}
    temp_dic['label']=tickers['Security Name'][i]
    temp_dic['value']=tickers['Symbol'][i]
    op_l.append(temp_dic)


app.layout = html.Div(children=[

    html.Center(html.H1(children='Real Time Stock Price Chart')),

    html.Center(html.H3(children='''
        By, Krutarth Bhatt (ASU ID: 1222317733 | Email: kmbhatt2@asu.edu)
    ''')),
    html.Hr(),
    dcc.Dropdown(
        id='stock-dropdown',
        options=op_l,
        placeholder="Select Stocks (Listed On Nasdaq)",
        multi=True,
        value=[]
    ),
    html.Div(id='hidden-div', style={'display':'none'}),
    dcc.Graph(
        id='live-graph',
        animate=False
#         animation=True
#         figure=fig
    ),
    dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        ),
    html.Center(html.H4('Know More About Me On:')),
    html.Center(html.A('My LinkedIn Profile', href='https://www.linkedin.com/in/krutarth-bhatt/')),
    html.Center(html.A('My Resume', href='https://drive.google.com/file/d/1iWuPcPtsPeOPJli0I41UR5U_FMP1g4Ho/view?usp=sharing')),
    
    
])

@app.callback( Output('hidden-div', 'children'),
#               Input('interval-component', 'n_intervals'),
              Input('stock-dropdown', 'value'))
def update_stocks_list(sl):
#     print(sl)
#     stock_l.clear()
#     stock_l.extend(sl)
    stock_l = list(sl)
#     print(stock_l)
    return "NA"



@app.callback(Output('live-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
#               Input('stock-dropdown', 'value'))
def update_graph_live(n):
    
    print("hi")
    print(n)
    if len(stock_l) == 0:
        
        time_l.clear()
        price_l.clear()
        fig = px.scatter()
        fig.update_layout(
#             title="Title",
            xaxis=dict(
                title="Time In New York"
            ),
            yaxis=dict(
                title="Stock Price"
            )
        )
        return fig
    else:
        
        for st in stock_l:
            try:
                price_l[st].append(si.get_live_price(st))
            except:
                price_l[st]=[]
                price_l[st].append(si.get_live_price(st))
            print('New Len of '+str(st))
            print(len(price_l[st]))
        
        len_l = []
        k_l = list(price_l)
        for k in k_l:
            if k not in stock_l:
                price_l.pop(k)
            else:
                len_l.append(len(price_l[k]))
                
                    
        
        utc = pytz.utc
        utc_dt = datetime.datetime.now()
        eastern = pytz.timezone('US/Eastern')
        loc_dt = utc_dt.astimezone(eastern)
        fmt = '%H:%M:%S %Z'
        time_l.append(loc_dt.strftime(fmt))
        
        print(len(time_l))
        print(max(len_l))
        n_remove = len(time_l) - max(len_l)
        print(n_remove)
        if n_remove == -1:
            n_remove = 0
        del time_l[:n_remove]
        
        df = {}
        df['Time In New York'] = time_l
        for st in stock_l:
            diff = [None]*(len(time_l)-len(price_l[st])) + price_l[st]
            print(st)
            print(len(diff))
            print(len(time_l))
            
#             diff = diff.extend(price_l[st])
            df[st] = diff
        df = pd.DataFrame(df)
        
        fig = (px.scatter(df, x='Time In New York', y=stock_l).update_traces(mode='lines+markers'))
        fig.update_layout(
#             title="Title",
            xaxis=dict(
                title="Time In New York"
            ),
            yaxis=dict(
                title="Stock Price"
            )
        )
        
        
        return fig
        
    
        

if __name__ == '__main__':
    app.run_server(debug=True)
