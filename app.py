import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

#swiftness

swiftness = np.arange(0, 1850, 50)

swiftness_cdr = 0.0214705496745448*swiftness

swiftness_dom_cdr = 1-(1*(1-(swiftness_cdr/100))*(1-0.2))

swiftness_dom_cj_cdr = 1-(1*(1-(swiftness_cdr/100))*(1-0.2)*(1-0.15))

swiftness_dom_awk1_cdr = 1-(1*(1-(swiftness_cdr/100))*(1-0.2)*(1-0.1))

swiftness_dom_awk1_cj_cdr = 1-(1*(1-(swiftness_cdr/100))*(1-0.2)*(1-0.1)*(1-0.15))

swiftness_dom_awk2_cdr = 1-(1*(1-(swiftness_cdr/100))*(1-0.2)*(1-0.25))

swiftness_dom_awk2_cj_cdr = 1-(1*(1-(swiftness_cdr/100))*(1-0.2)*(1-0.25)*(1-0.15))

swiftness_dom_awk3_cdr = 1-(1*(1-(swiftness_cdr/100))*(1-0.2)*(1-0.50))

swiftness_dom_awk3_cj_cdr = 1-(1*(1-(swiftness_cdr/100))*(1-0.2)*(1-0.50)*(1-0.15))

def downtime(x):
    v = ((5*(1-x))-2)*60
    return v


# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

app = Dash(__name__)

server = app.server

#starting from 3 to 0 so the awk3 is plotted first and its line gets placed behind in the graph
boxes = {
    "Base (Swiftness + DOM)": ["Base","Base + CJ"],
    "Base + AWK1": ["Base + AWK1","Base + AWK1 + CJ"],
    "Base + AWK2": ["Base + AWK2","Base + AWK2 + CJ"],
    "Base + AWK3": ["Base + AWK3"]
}

all_plots = [
            "Base","Base + CJ",
            "Base + AWK1","Base + AWK1 + CJ",
            "Base + AWK2","Base + AWK2 + CJ",
            "Base + AWK3"
]


app.layout = html.Div([
    html.Div([
        dcc.Graph(
        id='graph', config={'displayModeBar':False, 'showAxisDragHandles':False},
        ),
    ], id='div-wrapper'),
    dcc.Checklist(
        options=list(boxes.keys()),
        value=list(boxes.keys()),
        id='checklist',
        labelStyle={'display': 'block'}
    )
], id='parent-div')


@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))
def update_line_chart(checked_boxes):

    downtime_df = pd.DataFrame({
    "Swiftness": swiftness,
    "Base": downtime(swiftness_dom_cdr),
    "Base + CJ": downtime(swiftness_dom_cj_cdr),
    "Base + AWK1": downtime(swiftness_dom_awk1_cdr),
    "Base + AWK1 + CJ": downtime(swiftness_dom_awk1_cj_cdr),
    "Base + AWK2": downtime(swiftness_dom_awk2_cdr),
    "Base + AWK2 + CJ": downtime(swiftness_dom_awk2_cj_cdr),
    "Base + AWK3": downtime(swiftness_dom_awk3_cdr),
    })

    cdr_df = pd.DataFrame({
    "Swiftness": swiftness,
    "Swiftness CDR": swiftness_cdr,
    "Base": swiftness_dom_cdr,
    "Base + CJ": swiftness_dom_cj_cdr,
    "Base + AWK1": swiftness_dom_awk1_cdr,
    "Base + AWK1 + CJ": swiftness_dom_awk1_cj_cdr,
    "Base + AWK2": swiftness_dom_awk2_cdr,
    "Base + AWK2 + CJ": swiftness_dom_awk2_cj_cdr,
    "Base + AWK3": swiftness_dom_awk3_cdr,
    "Base + AWK3 + CJ": swiftness_dom_awk3_cj_cdr,
    })

    colormap = {
                "Base": "#636efa",
                "Base + CJ": "#636efa",
                "Base + AWK1": "#EF553B",
                "Base + AWK1 + CJ": "#EF553B",
                "Base + AWK2": "#00cc96",
                "Base + AWK2 + CJ": "#00cc96",
                "Base + AWK3": "#ab63fa",
                "Base + AWK3 + CJ": "#ab63fa",
                }

    fig = go.Figure()

    def visibility(checkbox):
        if checkbox not in checked_boxes:
            return 'legendonly'
        else:
            return True
    
    dashedornot=['solid','dot']

    checkboxes_titles = []
    for i in boxes:
        checkboxes_titles.append(i)

    for i in range(len(checkboxes_titles)):
        for j in range(len(boxes[checkboxes_titles[i]])):
            fig.add_trace(go.Scatter(
                x=downtime_df['Swiftness'],
                y=downtime_df[boxes[checkboxes_titles[i]][j]], name=boxes[checkboxes_titles[i]][j],
                mode='lines+markers',
                line = dict(color=colormap[boxes[checkboxes_titles[i]][j]],dash=dashedornot[j]),
                visible=visibility(checkboxes_titles[i])
            ))

    fig.update_layout(
        title='Swiftness x Inner Awakening Buff downtime',
        xaxis_title='Swiftness',
        yaxis_title='Downtime (secs)',
        yaxis={'range':[-9,120],'dtick':10},
        xaxis={'range':[0,1800],'dtick':100},
        height=600,
        hovermode="x",
        hoverlabel=dict(namelength=-1),
        template='plotly_dark',
        font={'family':'Calibri, sans-serif','size':14}
    )
    return fig

if __name__ == '__main__':
    print("Running")
    app.run_server(debug=True)
    
