import numpy as np
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import (ColumnDataSource, Range1d, LinearAxis, LinearColorMapper,
                          HoverTool, CategoricalColorMapper)
from bokeh.plotting import figure
from bokeh.palettes import all_palettes, Viridis
from bokeh.embed import components
from bokeh.resources import CDN
from sklearn.metrics import confusion_matrix

def eval_hc(num_data):
    log = 'HC'
    df = pd.read_csv(f'py_viz/data/evaluate_{log}.csv').dropna(subset=['WELL'])
    df = df[['WELL',f'{log}','DEPTH','prediction', 'prediction_correct']][df['prediction'].notnull()].reset_index(drop=True)

    # Convert label
    df[f'{log}'] = df[f'{log}'].replace({0: 'NULL', 1: 'Hydrocarbon Prospect Zone'})
    df.prediction = df.prediction.replace({0: 'NULL', 1: 'Hydrocarbon Prospect Zone'})
    df['color'] = df.prediction_correct.replace({True:'green', False:'red'})
    df.prediction_correct = df.prediction_correct.astype(str)

    # Set categorical color map
    colors_hc = ['#ffffff', '#ffd700']
    colors_cor = ['green', 'red']

    mapper_hc = CategoricalColorMapper(palette=colors_hc, factors=df[f'{log}'].unique().tolist())
    mapper_cor = CategoricalColorMapper(palette=colors_cor, factors=df.prediction_correct.unique().tolist())

    # Set up data

    data = df.iloc[:num_data]

    source = ColumnDataSource(data)

    d1 = source.data['index'].min()
    d2 = source.data['index'].max()
    wdt = 150
    hgh = 500
    tools = "crosshair, pan,reset,wheel_zoom"

    # track: HC
    a, b = -0.5, 0.5
    p1 = figure(width=int(wdt*1.15), height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools, title='Blind Well Test', y_axis_label='n_data')
    p1.extra_x_ranges = {f'{log}': Range1d(start=a, end=b)}
    p1.add_layout(LinearAxis(x_range_name=f'{log}', axis_label='Hydrocarbon'), 'above')
    p1.rect(x=0, y='index', source=source, width=1, height=1, x_range_name=f'{log}',
            fill_color={'field': f'{log}', 'transform': mapper_hc},
            line_color=None)
    p1.add_tools(HoverTool(tooltips="""
    <div>
        <style>
        div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
        div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px;"><b>WELL:</b> 
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>index:</b> @index</span><br>
        <span style="font-size: 8px;"><b>HC:</b> @HC</span>
    </div>
    """))

    # track: HC
    a, b = -0.5, 0.5
    p2 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p2.extra_x_ranges = {'p1': Range1d(start=a, end=b)}
    p2.add_layout(LinearAxis(x_range_name='p1', axis_label='Prediction'), 'above')
    p2.rect(x=0, y='index', source=source, width=1, height=1, x_range_name='p1',
            fill_color={'field': 'prediction', 'transform': mapper_hc},
            line_color=None)
    p2.add_tools(HoverTool(tooltips="""
    <div>
        <style>
        div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
        div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px;"><b>WELL:</b> 
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>index:</b> @index</span><br>
        <span style="font-size: 8px;"><b>prediction:</b> @prediction</span>
    </div>
    """))
   

    # track: Correction
    a, b = -0.5, 0.5
    p3 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p3.extra_x_ranges = {'p2': Range1d(start=a, end=b)}
    p3.add_layout(LinearAxis(x_range_name='p2', axis_label='True / False'), 'above')
    p3.rect(x=0, y='index', source=source, width=1, height=1, x_range_name='p2',
            fill_color={'field': 'prediction_correct', 'transform': mapper_cor},
            line_color=None)
    p3.add_tools(HoverTool(tooltips="""
    <div>
        <style>
        div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
        div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px;"><b>WELL:</b> 
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>index:</b> @index</span><br>
        <span style="font-size: 8px; color: @color;"><b>status:</b> @prediction_correct</span>
    </div>
    """))

    for p in [p1,p2,p3]:
        p.yaxis[0].axis_label_text_font_size = "10px"
        p.yaxis[0].major_label_text_font_size = "8px"
        for i in [0, 1]:
            p.xaxis[i].ticker = []
            p.xaxis[i].axis_label_text_font_size = "10px"
            p.xaxis[i].major_label_text_font_size = "8px"

    # track: Confussion Matrix
    cm = confusion_matrix(data[f'{log}'], data.prediction)
    df_cm = pd.DataFrame(cm, columns=data[f'{log}'].unique(), index=data[f'{log}'].unique())
    df_cm.index.name = 'Actual'
    df_cm.columns.name = 'Prediction'
    df_cm = df_cm.stack().rename('value').reset_index()
    colors = all_palettes['Blues'][256][::-1]
    mapper_cm = LinearColorMapper(palette=colors, low=df_cm.value.min(), high=df_cm.value.max())
    source_cm = ColumnDataSource(df_cm)

    p4 = figure(width=350, height=350, x_range=list(df[f'{log}'].unique()), y_range=list(df[f'{log}'].unique()), title='Confussion Matrix',
                tools=tools, y_axis_label='Prediction', x_axis_label='Actual')
    p4.rect(x='Actual', y='Prediction', width=1, height=1, source=source_cm,
            fill_color={'field': 'value', 'transform': mapper_cm}, line_color=None)
    p4.yaxis.major_label_orientation = 'vertical'
    p4.xaxis[0].axis_label_text_font_size = "10px"
    p4.yaxis[0].axis_label_text_font_size = "10px"
    p4.xaxis[0].major_label_text_font_size = "7px"
    p4.yaxis[0].major_label_text_font_size = "7px"
    p4.add_tools(HoverTool(tooltips="""
    <div>
        <style>
        div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
        div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px; color: #007acc;"><b>value:</b> @value</span><br>
    </div>
    """))

    plot = row([p1, p2, p3, p4])
    script, div = components(plot)
    cdn_js = CDN.js_files[0]

    return script, div, cdn_js
