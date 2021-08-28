import numpy as np
import pandas as pd

from getData import get_data_from_dataiku

from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import (ColumnDataSource, Range1d, LinearAxis, LogAxis,
                          HoverTool, Column)
from bokeh.plotting import figure
from bokeh.palettes import all_palettes
from bokeh.themes import Theme
from bokeh.embed import components
from bokeh.resources import CDN


def eval_sw(num_data):
    log, color = 'SW', 'purple'
    df = get_data_from_dataiku(f'evaluate_{log}').dropna(subset=['WELL'])
    # df = pd.read_csv(f'py_viz/data/evaluate_{log}.csv').dropna(subset=['WELL'])
    df['abs_error'] = df['error'].abs()
    df = df[['WELL',f'{log}','DEPTH','prediction','abs_error']][df['prediction'].notnull()].reset_index(drop=True)

    # Set up data

    data = df.iloc[:num_data]
    
    category = pd.cut(data['abs_error'].values, 2)
    palette = ['green', 'red']
    stat = ['good', 'bad']
    colors, status = [], []
    for i in category.codes:
        colors.append(palette[i])
        status.append(stat[i])

    data.insert(0, 'color', colors)
    data.insert(0, 'status', status)
    source = ColumnDataSource(data)

    d1 = source.data['index'].min()
    d2 = source.data['index'].max()
    wdt = 150
    hgh = 500
    tools = "crosshair, pan,reset,wheel_zoom"

    # track: SW (m3/m3)
    a, b = 0, 1
    p1 = figure(width=int(wdt*1.15), height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools, title=f'Blind Well Test', y_axis_label='n_data' ,x_axis_label='Prediction')
    p1.extra_x_ranges = {f'{log}': Range1d(start=a, end=b)}
    p1.add_layout(LinearAxis(x_range_name=f'{log}', axis_label=f'{log}'), 'above')
    p1.line(x=f'{log}', y='index', line_color=f'{color}', x_range_name=f'{log}', source=source)
    p1.line(x='prediction', y='index', line_dash="4 4", line_color='red', x_range_name=f'{log}', source=source)
    p1.xaxis[0].major_label_text_color = f"{color}"
    p1.xaxis[0].axis_label_text_color = f"{color}"
    p1.xaxis[1].major_label_text_color = "red"
    p1.xaxis[1].axis_label_text_color = "red"
    p1.yaxis[0].axis_label_text_font_size = "10px"
    p1.yaxis[0].major_label_text_font_size = "8px"
    p1.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>WELL:</b> @WELL</span><br> 
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>index:</b> @index</span><br>
        <span style="font-size: 8px; color: #0CFF0C;"><b>SW:</b> @SW{0.2f}</span><br>
        <span style="font-size: 8px; color: red;"><b>Prediction:</b> @prediction{0.2f}</span>
    </div>
    """, mode="hline"))
    for i in [0, 1]:
        p1.xaxis[i].ticker = [a, b]
        p1.xaxis[i].axis_label_text_font_size = "10px"
        p1.xaxis[i].major_label_text_font_size = "8px"

    # track: Error
    a, b = 0, data['abs_error'].max()
    p2 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p2.extra_x_ranges = {'error': Range1d(start=a, end=b)}
    p2.add_layout(LinearAxis(x_range_name='error', axis_label='abs_error'), 'above')
    p2.hbar(y='index', left=0, right='abs_error',height=0.02, source=source, color='color')
    p2.xaxis[0].ticker = [a,b]
    p2.xaxis[-1].visible = False
    p2.xgrid.grid_line_color = None
    p2.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>WELL:</b> @WELL</span><br> 
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>index:</b> @index</span><br>
        <span style="font-size: 8px;"><b>abs_error:</b> @abs_error{0.2f}</span><br>
        <span style="font-size: 8px; color: @color;"><b>status:</b> @status</span>
    </div>
    """, mode="hline"))
    a,b = 0, 1
    x,y = np.linspace(a,b), np.linspace(a,b)
    p3 = figure(width=400, height=400, x_range=[a,b], y_range=[a,b], title='Predicted - Actual Data Distribution',
                tools=tools, y_axis_label='Prediction' ,x_axis_label='Actual')
    p3.scatter(x=f'{log}', y='prediction', color='color', alpha=0.5, source=source)
    p3.line(x=x, y=y, color='#2a2a2a', line_dash="4 4", line_width=2, legend_label='proper approach to predicted value')
    p3.xgrid.grid_line_dash="4 4"
    p3.ygrid.grid_line_dash="4 4"
    p3.legend.location = 'bottom_right'
    p3.legend.label_text_font_size = "10px"
    p3.add_tools(HoverTool(tooltips="""
    <div>
        <style>
            div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
            div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px;"><b>WELL:</b> @WELL</span><br> 
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>index:</b> @index</span><br>
        <span style="font-size: 8px;"><b>SW:</b> @SW{0.2f}</span><br>
        <span style="font-size: 8px;"><b>Result:</b> @prediction{0.2f}</span><br>
        <span style="font-size: 8px; color: @color;"><b>status:</b> @status</span>
    </div>
    """))

    for p in [p2,p3]:
        p.xaxis[0].axis_label_text_font_size = "10px"
        p.yaxis[0].axis_label_text_font_size = "10px"
        p.xaxis[0].major_label_text_font_size = "8px"
        p.yaxis[0].major_label_text_font_size = "8px"

    plot = row([p1, p2, p3])
    script, div = components(plot)
    cdn_js = CDN.js_files[0]

    # doc.add_root(plot)
    # doc.title = f"Model Evaluation for {log}"
    # doc.theme = Theme('theme.yaml')
    return script, div, cdn_js
