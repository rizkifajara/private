from threading import Thread
from flask import Flask, render_template, request
from flask_pymongo import pymongo
import pandas as pd
# from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from pymongo import MongoClient
import json
import os
# import dnspython
from tornado.ioloop import IOLoop

from bokeh.embed import server_document
from bokeh.server.server import Server

from py_viz.bkapp.vsh import eval_vsh
from py_viz.bkapp.phie import eval_phie
from py_viz.bkapp.sw import eval_sw
from py_viz.bkapp.perm import eval_perm
from py_viz.bkapp.facies import eval_facies
from py_viz.bkapp.hc import eval_hc
from py_viz.bkapp.histplot import plot_histogram

from math import cos, asin, sqrt

app = Flask(__name__)

num_data = 2000


@app.route("/")
def helloWorld():
    return render_template("home.html")


@app.route("/form")
def viewForm():
    return render_template("form.html")

@app.route("/postform", methods = ["POST"])
def upload_form():
    
    well_name = request.form.get("well_name")
    field_name = request.form.get("field_name")
    lat = request.form.get("form_lat")
    lon = request.form.get("form_lon")
    f = request.files['form_file']

    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test

    # return db

    open('tmp/' + f.filename, 'wb').write(f.read())
    
    database_name='hackuna_matata123'
    student_db=client[database_name]


# @app.route("/postform")
# def upload_form():

#     client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#     db = client.test

#     database_name='hackuna_matata123'
#     student_db=client[database_name]

    collection_name='user'
    collection=student_db[collection_name]
    # f = request.files.get('file')
    # # mf = dataiku.Folder('O2B4wCQL') # name of the folder in the flow
    # # target_path = '/%s' % f.filename
    # # mf.upload_stream(target_path, f)

    # well = request.form.get('well')
    # lat = request.form.get('lat')
    # lon = request.form.get('lon')


    df = pd.read_csv("tmp/"+f.filename)
    
    source = {
        "filename":f.filename,
          "coordinate ": {"BAND":None, "EASTING":None,
                          "LATITUDE": lat, "LONGITUDE": lon,
                          "NORTHING": None, "WELL":well_name,
                          "ZONE": None},
          "data":[]
        # "wellName": well_name,
        # "latitude": lat,
        # "longitude": lon
    }
    
          
    
    for i in range(len(df)):
        dict_df = {}
        
        for col in df.columns:
            dict_df['WELL']=well_name
            dict_df[col]=df[col].iloc[i]
            
        source['data'].append(dict_df)
    
    # print(source)
    
    collection.insert_one(source)
    
    return json.dumps("Data berhasil di input")
#     # df = pd.read_csv(mf.get_download_stream(f.filename))

#     source = {
#         # "filename":f.filename,
#         #   "coordinate ": {"BAND":None, "EASTING":None,
#         #                   "LATITUDE": lat, "LONGITUDE": lon,
#         #                   "NORTHING": None, "WELL":well,
#         #                   "ZONE": None},
#         #   "data":[]
#         "wellName": well,
#         "latitude": lat,
#         "longitude": lon
#     }


#     # for i in range(len(df)):
#     #     dict_df = {}

#     #     for col in df.columns:
#     #         dict_df['WELL']=well
#     #         dict_df[col]=df[col].iloc[i]

#     #     source['data'].append(dict_df)

#     print(source)

#     collection.insert_one(source)

#     return json.dumps({1})

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2

    return 12742 * asin(sqrt(hav))

def closest(data, v):
    for dd in data:
      dd['dist'] = distance(v['lat'],v['lon'],dd['lat'],dd['lon'])
      print(dd)
        #wow.jarak = distance(v['lat'],v['lon'],wow.get('lat'),wow.get('lon'))
    
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

@app.route('/table')
def well_table():
    

    # for line in df1:
    #     row = line.split(",")
    #     well = row[0]
    #     easting = row [1]
    #     northing = row[2]
    #     zone = row[3]
    #     band = row[4]
    #     latitude = row[5]
    #     longitude = row[6]
    # arr = df.to_dict()


    df = pd.read_csv("tmp/volve_coordinate.csv")
    
    list_coord = list()
    

    for i in range(len(df)):
        dict_coord = dict()
        dict_coord['lat'] = df['LATITUDE'][i]
        dict_coord['lon'] = df['LONGITUDE'][i]
        dict_coord['label'] = df['WELL'][i]
        dict_coord['dist'] = None
        list_coord.append(dict_coord)
        print(i)

    print(list_coord)

    v = {'lat': 56, 'lon': 10}
    nearest = closest(list_coord, v)

    print(nearest)

    # return nearest

    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test
    database_name='hackuna_matata123'
    student_db=client[database_name]
    collection_name='user'
    collection=student_db[collection_name]

    
    # print(dataaa.get("coordinate"))
    # return "ok"
    for document in collection.find({},{ "_id": 0, "data": 0 }):
        print(document)

    return "ok"
    # return("ok")
    # return render_template('table_well.html', data = dataaa)

@app.route('/well-log')
def log():
    # script = server_document("0.0.0.0:5006/bkapp")
    return render_template("wellLog.html")


@app.route('/hist')
def hist():
    script, div, cdn_js = plot_histogram(nameWell='15/9-F-5')
    return render_template("hist.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)

@app.route('/hc', methods=['GET'])
def hc_page():
    script, div, cdn_js = eval_hc(num_data=num_data)
    return render_template("evalLog/hc.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/facies', methods=['GET'])
def facies_page():
    script, div, cdn_js = eval_facies(num_data=num_data)
    return render_template("evalLog/facies.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/perm', methods=['GET'])
def perm_page():
    script, div, cdn_js = eval_perm(num_data=num_data)
    return render_template("evalLog/perm.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/sw', methods=['GET'])
def sw_page():
    script, div, cdn_js = eval_sw(num_data=num_data)
    return render_template("evalLog/sw.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/phie', methods=['GET'])
def phie_page():
    script, div, cdn_js = eval_phie(num_data=num_data)
    return render_template("evalLog/phie.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/vsh', methods=['GET'])
def vsh_page():
    script, div, cdn_js = eval_vsh(num_data=num_data)
    return render_template("evalLog/vsh.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
