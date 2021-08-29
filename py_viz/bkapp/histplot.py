from os import name
import pandas as pd

from getData import get_data_from_dataiku

# from bokeh.io import curdoc
from bokeh.models import Legend, NumeralTickFormatter, ColumnDataSource
from bokeh.plotting import figure
from bokeh.palettes import all_palettes
from bokeh.embed import components
from bokeh.resources import CDN

def get_form(nameWell):
    # df = get_data_from_dataiku('database_volve').dropna(subset=['WELL'])
    df = pd.read_csv('py_viz/data/database_volve.csv').dropna(subset=['WELL'])
    obj_df = df[['FACIES','FORMATION','WELL']]

    well = nameWell 
    obj_df_well = obj_df[obj_df['WELL'].isin([well])] 

    hist_df = obj_df_well.groupby('FORMATION').FACIES.value_counts().reset_index(name='COUNTS')
    
    hist_df_pivot = hist_df.pivot(index='FACIES',columns='FORMATION',values='COUNTS').fillna(0)

    col = hist_df_pivot.columns
    hist_df_pivot[col] = hist_df_pivot[col]/hist_df_pivot[col].sum()
    
    return hist_df_pivot, col.tolist()

def plot_histogram(data, nameWell, nameForm):
    well = nameWell
    if nameForm!=None:
        default_form = nameForm
        source = data[default_form]
        value = source.values.tolist()
        facies = source.index.tolist()
        source = ColumnDataSource(data=dict(facies=facies,
                                            value=value,
                                            color=all_palettes['Spectral'][len(facies)]))

        p = figure(x_range=facies, y_range=(0,1), height=300, width=600, title=f"{well} || {default_form}",
                toolbar_location=None, tools='hover', 
                tooltips="@facies:<br> <b>@value{0.0f%}<b>",
                y_axis_label='Total Percentage', x_axis_label='Facies')

        p.vbar(x='facies', top='value', width=0.4, color='color',legend_field='facies', source=source)

        p.xgrid.grid_line_color = None
        p.ygrid.minor_grid_line_color = '#f7f7f7'
        p.xaxis.major_label_text_color = None
        p.yaxis.formatter = NumeralTickFormatter(format="0f%")
        p.add_layout(p.legend[0],'right')
        p.legend.label_text_font_size = '8pt'
        p.legend.border_line_color = None

        script, div = components(p)
        print(div)
        cdn_js = CDN.js_files[0]

    else:
        script = '<script></script>'
        div = '''
        <div style="text-align: center;">
        <h1 style="font-family:courier; font-size:80px;">404</h1>
        <p>error: no facies in this data</p>
        </div>'''
        cdn_js = ''

    return script, div, cdn_js