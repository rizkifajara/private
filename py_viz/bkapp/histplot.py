import pandas as pd

# from bokeh.io import curdoc
from bokeh.models import Legend, NumeralTickFormatter
from bokeh.plotting import figure
from bokeh.palettes import all_palettes
from bokeh.embed import components
from bokeh.resources import CDN

def plot_histogram(nameWell):
    df = pd.read_csv('py_viz/data/database_volve.csv').dropna(subset=['WELL'])
    obj_df = df[['FACIES','FORMATION','WELL']][df['FACIES'].notnull()]

    well = nameWell # custom select well
    obj_df_well = obj_df[obj_df['WELL'].isin([well])] 

    if len(obj_df_well!=0):
        hist_df = obj_df_well.groupby('FORMATION').FACIES.value_counts().reset_index(name='COUNTS')

    else:
        list_formation = df[df['WELL'].isin([well])].FORMATION.unique()
        hist_df = pd.DataFrame({'FORMATION':list_formation,
                    'FACIES':['NULL' for i in range(len(list_formation))],
                    'COUNTS':[0 for i in range(len(list_formation))]})

    hist_df_pivot = hist_df.pivot(index='FORMATION',columns='FACIES',values='COUNTS').fillna(0)
    hist_df_pivot = hist_df_pivot.apply(lambda x: (x/hist_df_pivot.values.sum()))

    list_facies = hist_df_pivot.columns.tolist()
    list_form = hist_df_pivot.index.tolist()
    if list_facies==['NULL']:
        colors = ('#ffffff')
    else:
        colors = all_palettes['Spectral'][len(list_facies)]

    source = {'FORMATION':list_form}
    for i in range(len(list_facies)):
        source[list_facies[i]]=list(hist_df_pivot.iloc[:,i])
        
    p = figure(x_range=list_form, height=400, width=len(list_form)*100+200, title=f"WELL: {well}",
            toolbar_location=None, tools='hover', tooltips="$name - @FORMATION:<br> <b>@$name{0.0f%}<b>",
            y_axis_label='Total Percentage', x_axis_label='Formation')

    v = p.vbar_stack(list_facies, x='FORMATION', width=0.5, color=colors, source=source)
    legend = Legend(items=[(x, [v[i]]) for i, x in enumerate(list_facies)], location=(10, 100))

    p.add_layout(legend, 'right')
    p.y_range.start = 0
    p.y_range.end = 1
    p.xgrid.grid_line_color = None
    p.outline_line_color = None
    p.legend.border_line_color = None
    p.yaxis.formatter = NumeralTickFormatter(format="0f%")

    script, div = components(p)
    cdn_js = CDN.js_files[0]

    return script, div, cdn_js