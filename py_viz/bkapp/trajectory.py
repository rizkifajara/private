import pandas as pd

from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, Legend, HoverTool
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN

path_csv = "tmp/trajectory_database.csv"
df = pd.read_csv(path_csv)


def plot_trajectory(nameWell, data=df):
    df_well = data[data.WellName == nameWell]

    source = ColumnDataSource(data=dict(
        North=df_well.North,
        East=df_well.East,
        Dist=df_well.Res,
        TVD=df_well.TVD_ft
    ))

    # Set up plot
    p1 = figure(plot_height=200, plot_width=400, title="TVD Lateral Plot",
                tools="crosshair,pan,reset,save,wheel_zoom",
                y_range=[df_well.North.min()-1000, df_well.North.max()+1000], y_axis_label='South - North (ft)',
                x_range=[df_well.East.min()-1000, df_well.East.max()+1000], x_axis_label='West - East (ft)',
                )

    p1.cross('East', 'North', source=source, size=3,
             color='green', legend_label='Coordinate (ft)')
    p1.line('East', 'North', source=source, color='green',
            legend_label='Coordinate (ft)', line_width=0.2)

    p1.line([df_well.East.iloc[0], df_well.East.iloc[-1]], [df_well.North.iloc[0],
            df_well.North.iloc[-1]], line_color='black', legend_label='Trajectory line')
    p1.circle_dot(df_well.East[:1], df_well.North[:1], fill_color='white',
                  color='black', size=15, legend_label='Top Depth')
    p1.circle_x(df_well.East[-1:], df_well.North[-1:], fill_color='white',
                color='black', size=15, legend_label='Bottom Depth')
    p1.xaxis.major_label_orientation = 'vertical'
    p1.legend.border_line_alpha = 0

    legend = p1.legend[0]
    p1.center = [item for item in p1.center if not isinstance(item, Legend)]
    p1.add_layout(legend, 'right')

    p1.add_tools(HoverTool(tooltips="""
    <div>
        <style>
        div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
        div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px; color: gold;"><b>East:</b> $x{0.0f}</span><br>
        <span style="font-size: 8px; color: blue;"><b>North:</b> $y{0.0f}</span><br>
    </div>
    """))

    p2 = figure(plot_height=300, plot_width=300, title="TVD Profile Plot",
                tools="crosshair,pan,reset,save,wheel_zoom",
                y_range=[df_well.TVD_ft.max()*1.1, 0], y_axis_location='right',
                y_axis_label='TVD (ft)', x_axis_label='Distance (ft)'
                )
    # p2.cross('East', 'TVD', source=source, color='gold',
    #          size=3, legend_label='TVD x (West - East)')
    # p2.line('East', 'TVD', source=source, color='gold',
    #         legend_label='TVD x (West - East)', line_width=0.2)
    # p2.cross('North', 'TVD', source=source, color='blue',
    #          size=3, legend_label='TVD x (South - North)')
    # p2.line('North', 'TVD', source=source, color='blue',
    #         legend_label='TVD x (South - North)', line_width=0.2)
    p2.cross('Dist', 'TVD', source=source, color='green', size=3, legend_label='TVD x Resultan')

    p2.xaxis.major_label_orientation = 'vertical'
    p2.add_tools(HoverTool(tooltips="""
    <div>
        <style>
        div.bk-tooltip.bk-right>div.bk>div:not(:first-child) {display:none !important;} 
        div.bk-tooltip.bk-left>div.bk>div:not(:first-child) {display:none !important;}
        </style>
        <span style="font-size: 8px; color: #2a2a2a;"><b>TVP:</b> @TVD{0.0f}</span><br>
        <span style="font-size: 8px; color: gold;"><b>East:</b> @East{0.0f}</span><br>
        <span style="font-size: 8px; color: blue;"><b>North:</b> @North{0.0f}</span><br>
        <span style="font-size: 8px; color: green;"><b>Resultan:</b> @Dist{0.0f}</span><br>
    </div>
    """, mode="hline"))
    legend2 = p2.legend[0]
    p2.center = [item for item in p2.center if not isinstance(item, Legend)]
    p2.add_layout(legend2, 'left')
    p2.legend.border_line_alpha = 0

    for p in [p1, p2]:
        p.xaxis[0].axis_label_text_font_size = "10px"
        p.xaxis[0].major_label_text_font_size = "8px"
        p.yaxis[0].axis_label_text_font_size = "10px"
        p.yaxis[0].major_label_text_font_size = "8px"
        p.legend.label_text_font_size = "10px"

    plot = gridplot([p1, p2], ncols=2)

    script, div = components(plot)
    cdn_js = CDN.js_files[0]

    return script, div, cdn_js
