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
from bson.objectid import ObjectId
# import dnspython

from bokeh.embed import server_document

from py_viz.bkapp.vsh import eval_vsh
from py_viz.bkapp.phie import eval_phie
from py_viz.bkapp.sw import eval_sw
from py_viz.bkapp.perm import eval_perm
from py_viz.bkapp.facies import eval_facies
from py_viz.bkapp.hc import eval_hc
from py_viz.bkapp.histplot import plot_histogram, get_form

from math import cos, asin, sqrt

from getData import get_data_from_dataiku

app = Flask(__name__)

num_data_global=1500


well_name_global = "15/9-F-5"

well_name_list = []


@app.route("/")
def viewForm():
    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test
    database_name='hackuna_matata123'
    student_db=client[database_name]
    collection_name='user'
    collection=student_db[collection_name]
    user_data_list = []
    for document in collection.find():
        user_data_list.append(document)
        # print(document)
    #print(user_data_list[0]["data"])

    return render_template("form.html", user_data=user_data_list)

@app.route("/delete/<id>/")
def delete_well(id):
    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test
    database_name='hackuna_matata123'
    student_db=client[database_name]
    collection_name='user'
    collection=student_db[collection_name]

    collection.delete_one({'_id': ObjectId(id)})

    return json.dumps("Data successfully removed")

@app.route("/page-2")
def analyze_page():
    return render_template("analyze.html")

@app.route("/well-name", methods=["POST", "GET"])
def get_well_name():
    return json.dumps(well_name)


@app.route("/send-well-list", methods=["GET","POST"])
def send_well_list():
    global well_name_list
    print(well_name_list)
    well_name_list = request.form.getlist("list_well_name[]")
    print(well_name_list)
    return "<div id='chart'></div>"



@app.route("/get-well-list", methods=["POST", "GET"])
def get_well_list():
    return json.dumps(well_name_list)

@app.route("/circles")
def circle_page():
    return render_template("circle.html")

@app.route("/postform", methods = ["POST"])
def upload_form():
    
    well_name = request.form.get("well_name")
    field_name = request.form.get("field_name")
    lat = request.form.get("form_lat")
    lon = request.form.get("form_lon")
    f = request.files['form_file']

    mf = dataiku.Folder('O2B4wCQL') # name of the folder in the flow
    target_path = '/%s' % f.filename
    mf.upload_stream(target_path, f)


    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test

    # return db

    open('tmp/' + f.filename, 'wb').write(f.read())
    
    database_name='hackuna_matata123'
    student_db=client[database_name]


    collection_name='user'
    collection=student_db[collection_name]


    df = pd.read_csv("tmp/"+f.filename)
    
    source = {
        "filename":f.filename,
          "coordinate ": {"BAND":None, "EASTING":None,
                          "LATITUDE": lat, "LONGITUDE": lon,
                          "NORTHING": None, "WELL":well_name,
                          "ZONE": None},
          "data":[]

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


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2

    return 12742000 * asin(sqrt(hav))

def closest(data, v):
    for dd in data:
      dd['dist'] = distance(v['lat'],v['lon'],dd['lat'],dd['lon'])
      print(dd)
        #wow.jarak = distance(v['lat'],v['lon'],wow.get('lat'),wow.get('lon'))
    
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

@app.route('/table/<id_well>/', methods=['GET'])
def well_table(id_well):
    
    df = get_data_from_dataiku("database_coordinate")

    # df = pd.read_csv("tmp/volve_coordinate.csv")
    
    list_coord = list()
    

    for i in range(len(df)):
        dict_coord = dict()
        dict_coord['lat'] = df['LATITUDE'][i]
        dict_coord['lon'] = df['LONGITUDE'][i]
        dict_coord['label'] = df['WELL'][i]
        dict_coord['dist'] = None
        list_coord.append(dict_coord)

    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test
    database_name='hackuna_matata123'
    student_db=client[database_name]
    collection_name='user'
    collection=student_db[collection_name]

    user_data_dict = collection.find_one({"_id": ObjectId(id_well)},{ "data": 0 })
    v = {"lat": float(user_data_dict['coordinate ']['LATITUDE']), "lon": float(user_data_dict['coordinate ']['LONGITUDE'])}
    print(v)

    nearest = closest(list_coord, v)

    sorted_list_coord = sorted(list_coord, key = lambda i: i['dist'])

    return render_template("analyze.html", data=sorted_list_coord, user_data=user_data_dict)


@app.route('/well-log', methods=["POST", "GET"])
def log():
    return render_template("wellLog.html")


@app.route('/hist', methods=["POST", "GET"])
def hist():
    global well_name
    well_name = request.form.get("value_well")
    if well_name == None:
        well_name = "15/9-F-5"
    else:
        well_name = str(well_name)
    data, list_formation = get_form(nameWell=well_name)
    form = request.form.get('value_form')
    if form==None:
        try:
            form=list_formation[0]
        except:
            form=None
    script, div, cdn_js = plot_histogram(data=data, nameWell=well_name, nameForm=form)
    return render_template("hist.html",
                            list_formation = list_formation,
                            form=form,
                            script=script,
                            div=div,
                            cdn_js=cdn_js)

@app.route('/hc', methods=['GET'])
def hc_page():
    script, div, cdn_js = eval_hc(num_data=num_data_global)
    return render_template("evalLog/hc.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/facies', methods=['GET'])
def facies_page():
    script, div, cdn_js = eval_facies(num_data=num_data_global)
    return render_template("evalLog/facies.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/perm', methods=['GET'])
def perm_page():
    script, div, cdn_js = eval_perm(num_data=num_data_global)
    return render_template("evalLog/perm.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/sw', methods=['GET'])
def sw_page():
    script, div, cdn_js = eval_sw(num_data=num_data_global)
    return render_template("evalLog/sw.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/phie', methods=['GET'])
def phie_page():
    script, div, cdn_js = eval_phie(num_data=num_data_global)
    return render_template("evalLog/phie.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/vsh', methods=['GET'])
def vsh_page():
    global num_data_global
    num_data = request.args.get('num')
    if num_data==None:
        num_data_global = 1500
    else:
        num_data_global = int(num_data)
    script, div, cdn_js = eval_vsh(num_data=num_data_global)
    return render_template("evalLog/vsh.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
