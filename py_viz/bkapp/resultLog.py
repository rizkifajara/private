import numpy as np
import pandas as pd

from getData import get_data_from_dataiku

from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import (ColumnDataSource, Range1d, LinearAxis, LogAxis,
                          PrintfTickFormatter, HoverTool)
from bokeh.models.mappers import CategoricalColorMapper
from bokeh.plotting import figure
from bokeh.palettes import all_palettes
from bokeh.embed import components
from bokeh.resources import CDN

def compute_cut_off(data, perc_cutoff):
    gr = data.GR.copy()
    cutoff = np.percentile(gr, perc_cutoff)
    mid = [cutoff for i in range(len(gr))]
    x1 = gr.where(gr >= cutoff)
    x2 = gr.where(gr < cutoff)
    return np.round(cutoff, 1), {'DEPTH': data.DEPTH, 'mid': mid, 'x1': x1, 'x2': x2}

def plot_result():
    df = get_data_from_dataiku('data_user_F-4_FINAL').dropna(subset=['WELL'])

    # Convert label
    df.HC = df.HC.replace({0: 'NULL',
                        1: 'Hydrocarbon Prospect Zone',
                        np.nan: 'NULL'})
    df.FACIES = df.FACIES.fillna('NULL')

    # Set categorical color map
    colors_hc = ['#ffffff', '#ffd700']
    colors_facies = list(all_palettes['Spectral'][len(df.FACIES.unique())-1])
    colors_facies[:0] = ['#ffffff']

    mapper_hc = CategoricalColorMapper(
        palette=colors_hc, factors=df.HC.unique().tolist())
    mapper_facies = CategoricalColorMapper(
        palette=colors_facies, factors=df.FACIES.unique().tolist())

    # Set up data
    # ------------------ custom input well -----------------------------

    data = df
    source = ColumnDataSource(data)

    default_cutoff = 50
    co, data_co = compute_cut_off(data, default_cutoff)
    cutoff_gr = ColumnDataSource(data_co)

    d1 = source.data['DEPTH'].min()
    d2 = source.data['DEPTH'].max()
    wdt = 110
    hgh = 400
    tools = "crosshair, pan,reset,wheel_zoom"

    # 1st track: GR (GAPI)
    a, b = 0, 150
    p1 = figure(width=int(wdt*1.2), height=hgh, x_range=[a, b], y_range=[d2, d1], title='15/9-F-4',
                y_axis_label='Depth (m)', tools=tools)
    p1.extra_x_ranges = {'GR': Range1d(start=a, end=b)}
    p1.add_layout(LinearAxis(x_range_name='GR', axis_label='GR'), 'above')
    p1.line(x='GR', y='DEPTH', line_color='green',
            x_range_name='GR', source=source)
    p1.harea(x1='x2', x2='mid', y='DEPTH', fill_color='gold',
            fill_alpha=0.5, source=cutoff_gr)
    p1.harea(x1='x1', x2='mid', y='DEPTH', fill_color='lime',
            fill_alpha=0.5, source=cutoff_gr)
    p1.xaxis[0].ticker = [a, co, b]
    p1.xaxis[0].formatter = PrintfTickFormatter(format="%3f")
    p1.xaxis[0].major_label_text_color = "green"
    p1.xaxis[0].axis_label_text_color = "green"
    p1.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;color: #229122;"><b>GR:</b> @GR{0.2f}</span>
    </div>
    """, mode="hline"))

    # 2nd track ILD (Ohm.m)
    a, b = 0.2, 2000
    p2 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools, x_axis_type='log')
    p2.extra_x_ranges = {'ILD': Range1d(start=a, end=b)}
    p2.add_layout(LogAxis(x_range_name='ILD', axis_label='ILD'), 'above')
    p2.line(x='ILD', y='DEPTH', line_color='black',
            x_range_name='ILD', source=source)
    p2.xaxis[0].ticker = [a, b]
    p2.xaxis[0].formatter = PrintfTickFormatter(format="%5f")
    p2.xgrid.minor_grid_line_color = 'navy'
    p2.xgrid.minor_grid_line_alpha = 0.05
    p2.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>ILD:</b> @ILD{0.2f}</span>
    </div>
    """, mode="hline"))

    # 3rd track: RHOB (g/cm3) and NPHI (m3/m3)
    a, b, c, d = 1.95, 2.95, 0.45, -0.15
    p3 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p3.extra_x_ranges = {'RHOB': Range1d(start=a, end=b),
                        'NPHI': Range1d(start=c, end=d)}
    p3.add_layout(LinearAxis(x_range_name='RHOB', axis_label='RHOB'), 'above')
    p3.line(x='RHOB', y='DEPTH', line_color='red',
            x_range_name='RHOB', source=source.data)
    p3.add_layout(LinearAxis(x_range_name='NPHI', axis_label='NPHI'), 'above')
    p3.line(x='NPHI', y='DEPTH', line_color='darkblue',
            x_range_name='NPHI', source=source)
    p3.xaxis[0].ticker = [a, b]
    p3.xaxis[0].major_label_text_color = "red"
    p3.xaxis[0].axis_label_text_color = "red"
    p3.xaxis[1].ticker = [c, d]
    p3.xaxis[1].major_label_text_color = "darkblue"
    p3.xaxis[1].axis_label_text_color = "darkblue"
    p3.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px; color: #FF2323;"><b>RHOB:</b> @RHOB{0.2f}</span><br>
        <span style="font-size: 8px; color: #121293;"><b>NPHI:</b> @NPHI{0.2f}</span>
    </div>
    """, mode="hline"))

    # 4th track: VSH (m3/m3)
    a, b = 0, 1
    p4 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p4.extra_x_ranges = {'VSH': Range1d(start=a, end=b)}
    p4.add_layout(LinearAxis(x_range_name='VSH', axis_label='VSH'), 'above')
    p4.line(x='VSH', y='DEPTH', line_color='lime',
            x_range_name='VSH', source=source)
    p4.xaxis[0].ticker = [a, b]
    p4.xaxis[0].major_label_text_color = "lime"
    p4.xaxis[0].axis_label_text_color = "lime"
    p4.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px; color: #0CFF0C;"><b>VSH:</b> @VSH{0.2f}</span>
    </div>
    """, mode="hline"))


    # 5th track: PHIE (m3/m3)
    a, b = 0.6, 0
    p5 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p5.extra_x_ranges = {'PHIE': Range1d(start=a, end=b)}
    p5.add_layout(LinearAxis(x_range_name='PHIE', axis_label='PHIE'), 'above')
    p5.line(x='PHIE', y='DEPTH', line_color='blue',
            x_range_name='PHIE', source=source)
    p5.xaxis[0].ticker = [a, b]
    p5.xaxis[0].major_label_text_color = "blue"
    p5.xaxis[0].axis_label_text_color = "blue"
    p5.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px; color: #0000FF;"><b>PHIE:</b> @PHIE{0.2f}</span>
    </div>
    """, mode="hline"))

    # 6th track: SW (v/v)
    a, b = 0, 1
    p6 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p6.extra_x_ranges = {'SW': Range1d(start=a, end=b)}
    p6.add_layout(LinearAxis(x_range_name='SW', axis_label='SW'), 'above')
    p6.line(x='SW', y='DEPTH', line_color='purple',
            x_range_name='SW', source=source)
    p6.xaxis[0].ticker = [a, b]
    p6.xaxis[0].major_label_text_color = "purple"
    p6.xaxis[0].axis_label_text_color = "purple"
    p6.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px; color: #870D87;"><b>SW:</b> @SW{0.2f}</span>
    </div>
    """, mode="hline"))

    # 7th track: PERM (mD)
    a, b = 0.1, 10000
    p7 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools, x_axis_type='log')
    p7.extra_x_ranges = {'PERM': Range1d(start=a, end=b)}
    p7.add_layout(LogAxis(x_range_name='PERM', axis_label='PERM'), 'above')
    p7.line(x='PERM', y='DEPTH', line_color='black',
            x_range_name='PERM', source=source)
    p7.xaxis[0].ticker = [a, b]
    p7.xaxis[0].formatter = PrintfTickFormatter(format="%5f")
    p7.xgrid.minor_grid_line_color = 'navy'
    p7.xgrid.minor_grid_line_alpha = 0.05
    p7.add_tools(HoverTool(tooltips="""
    <div>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>PERM:</b> @PERM{0.2f}</span>
    </div>
    """, mode="hline"))

    # 8th track: Hydrocarbon
    a, b = -0.5, 0.5
    p8 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p8.extra_x_ranges = {'HC': Range1d(start=a, end=b)}
    p8.add_layout(LinearAxis(x_range_name='HC', axis_label='Hydrocarbon'), 'above')
    p8.rect(x=0, y='DEPTH', source=source, width=1, height=1,
            fill_color={'field': 'HC', 'transform': mapper_hc},
            line_color=None)
    p8.xaxis[0].ticker = []
    p8.add_tools(HoverTool(tooltips="""
    <div>
        <style>
        div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
        div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>HC:</b> @HC</span>
    </div>
    """))

    # 9th track: Facies
    a, b = -0.5, 0.5
    p9 = figure(width=wdt, height=hgh, x_range=[a, b], y_range=[d2, d1],
                tools=tools)
    p9.extra_x_ranges = {'FACIES': Range1d(start=a, end=b)}
    p9.add_layout(LinearAxis(x_range_name='FACIES', axis_label='Facies'), 'above')
    p9.rect(x=0, y='DEPTH', source=source, width=1, height=1,
            fill_color={'field': 'FACIES', 'transform': mapper_facies},
            line_color=None)
    p9.xaxis[0].ticker = []
    p9.add_tools(HoverTool(tooltips="""
    <div>
        <style>
        div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
        div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px;"><b>DEPTH:</b> @DEPTH{0.2f}</span><br>
        <span style="font-size: 8px;"><b>FACIES:</b> @FACIES</span>
    </div>
    """))

    for p in [p1, p2, p4, p3, p5, p6, p7, p8, p9]:
        p.xaxis[-1].visible = False

    plot = row([p1, p2, p3, p4, p5, p6, p7, p8, p9])

    
    script, div = components(plot)
    cdn_js = CDN.js_files[0]

    # curdoc().add_root(row(plot))
    # curdoc().title = "Well Log Visualization"
    return script, div, cdn_js