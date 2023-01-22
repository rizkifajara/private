from flask import Flask, render_template, request
from flask_pymongo import pymongo
import pandas as pd
import json
import os
from bson.objectid import ObjectId

from py_viz.bkapp.facies import eval_facies
from py_viz.bkapp.hc import eval_hc
from py_viz.bkapp.histplot import plot_histogram, get_form
from py_viz.bkapp.resultLog import plot_result
from py_viz.bkapp.trajectory import plot_trajectory

from math import cos, asin, sqrt

app = Flask(__name__)

well_name_list = []
mongoClient = os.environ.get('MONGO_URL')
client = pymongo.MongoClient(mongoClient)
database_name = os.environ.get('DB_NAME')
hackuna_db = client[database_name]
collection_name = os.environ.get('COLLECTION_NAME')
collection = hackuna_db[collection_name]

num_data_global = 1500

@app.route("/form")
def viewForm():
    user_data_list = []
    for document in collection.find():
        document['data'] = [document['data'][0]]
        user_data_list.append(document)
    return render_template("form.html", user_data=user_data_list)


@app.route("/")
def viewLanding():
    return render_template("login.html")


@app.route("/delete/<id>")
def delete_well(id):

    try:
        collection.delete_one({'_id': ObjectId(id)})
        return render_template("redirect_delete.html")

    except Exception as e:

        return(str(e))


@app.route("/page-2")
def analyze_page():
    return render_template("analyze.html")


@app.route("/well-name", methods=["POST", "GET"])
def get_well_name():
    return json.dumps(well_name)


@app.route("/send-well-list", methods=["GET", "POST"])
def send_well_list():
    global well_name_list
    well_name_list = request.form.getlist("list_well_name[]")
    return "<div id='chart'></div>"


@app.route("/get-well-list", methods=["POST", "GET"])
def get_well_list():
    return json.dumps(well_name_list)


@app.route("/circles")
def circle_page():
    return render_template("circle.html")


@app.route("/volveform", methods=["POST"])
def volveForm():

    collection_name = 'volve'
    collection = hackuna_db[collection_name]

    wellName = request.form["well_name"]
    east = request.form.get("easting")
    north = request.form.get("northing")
    zoneForm = request.form.get("zone")
    bandForm = request.form.get("band")
    latitudeForm = request.form.get("latitude")
    longitudeForm = request.form.get("longitude")

    sendForm = {
        "well_name": wellName,
        "easting": east,
        "northing": north,
        "zone": zoneForm,
        "band": bandForm,
        "latitude": latitudeForm,
        "longitude": longitudeForm
    }

    collection.insert_one(sendForm)

    return json.dumps("data berhasil diinput")


@app.route("/postform", methods=["POST"])
def upload_form():
    
    try :
        well_name = request.form.get("well_name")
        field_name = request.form.get("field_name")
        lat = request.form.get("form_lat")
        lon = request.form.get("form_lon")
        f = request.files['form_file']

        if f.filename == '':
            return "Belum memilih file"

        if lat== '' or lat == '':
            return "Belum mengisi lat lon"

        if well_name == '':
            return "Belum mengisi well name"

        if field_name == '':
            return "Belum mengisi field name"

        open('tmp/' + f.filename, 'wb').write(f.read())
        
        df = pd.read_csv("tmp/"+f.filename)
        
        source = {
            "filename":f.filename,
            "mnemonic_edit":None,
            "coordinate ": {"BAND":None, "EASTING":None,
                            "LATITUDE": lat, "LONGITUDE": lon,
                            "NORTHING": None, "WELL":well_name,
                            "ZONE": None},
            "data":[]

        }
        
        true_col = ["GR", "ILD", "RHOB", "NPHI", "VSH", "PHIE", "SW", "PERM", "FACIES", "HC", "WELL"]
        auto_mnemonic = {
            "RHOZ": "RHOB", "ZDEN": "RHOB", "ZDNC": "RHOB", "HDEN": "RHOB",
            "Vshale": "VSH",
            "CNC": "NPHI", "TNPH":"NPHI", "TPHC":"NPHI",
            "ILD":"RT", "LLD": "RT", "HLLD": "RT", "IDFL": "RT",
            "SWE": "SW"
        }

        replace_mc = []
        for i in range(len(df)):
            dict_df = {}
            for col in df.columns:
                new_col = auto_mnemonic.get(col, col)
                if col not in true_col:
                    df = df.rename(columns={col: new_col})
                    if col!=new_col: replace_mc.append({"before": col, "after": new_col})

                dict_df[new_col] = df[new_col].iloc[i]
            
            dict_df['id'] = i
            dict_df["WELL"] = well_name
            source["data"].append(dict_df)
        
        source["mnemonic_edit"] = replace_mc

        collection.insert_one(source)
        
        return render_template("redirect_form.html")
    
    except Exception as e:

        return(str(e))


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * \
        cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2

    return 12742000 * asin(sqrt(hav))


def closest(data, v):
    for dd in data:
        dd['dist'] = distance(v['lat'], v['lon'], dd['lat'], dd['lon'])

    return min(data, key=lambda p: distance(v['lat'], v['lon'], p['lat'], p['lon']))


@app.route('/table/<id_well>/', methods=['GET'])
def well_table(id_well):

    # df = get_data_from_dataiku("database_coordinate")
    df = pd.read_csv('./tmp/volve_coordinate.csv')

    list_coord = list()

    for i in range(len(df)):
        dict_coord = dict()
        dict_coord['lat'] = df['LATITUDE'][i]
        dict_coord['lon'] = df['LONGITUDE'][i]
        dict_coord['label'] = df['WELL'][i]
        dict_coord['dLon'] = df['TRAJECTORY_X'][i]
        dict_coord['dLat'] = df['TRAJECTORY_Y'][i]
        dict_coord['dist'] = None
        list_coord.append(dict_coord)

    user_data_dict = collection.find_one(
        {"_id": ObjectId(id_well)}, {"data": 0})
    v = {"lat": float(user_data_dict['coordinate ']['LATITUDE']), "lon": float(
        user_data_dict['coordinate ']['LONGITUDE'])}

    nearest = closest(list_coord, v)

    sorted_list_coord = sorted(list_coord, key=lambda i: i['dist'])

    return render_template("analyze.html", data=sorted_list_coord, user_data=user_data_dict)


@app.route('/well-log', methods=["POST", "GET"])
def log():
    global well_name
    well_name = request.form.get("value_well")
    if well_name == None:
        well_name = str("15/9-F-5")
    else:
        well_name = str(well_name)
    return render_template("evalLog/wellLog.html",
                            NameWell=well_name)


@app.route('/hist', methods=["POST", "GET"])
def hist():
    global well_name
    well_name = request.form.get("value_well")
    # print(well_name)
    if well_name == None:
        well_name = "15/9-F-5"
    else:
        well_name = str(well_name)
    data, list_formation = get_form(nameWell=well_name)
    form = request.form.get('value_form')
    if form == None:
        try:
            form = list_formation[0]
        except:
            form = None
    script, div, cdn_js = plot_histogram(
        data=data, nameWell=well_name, nameForm=form)
    return render_template("evalLog/hist.html",
                           list_formation=list_formation,
                           form=form,
                           script=script,
                           div=div,
                           cdn_js=cdn_js,
                           NameWell=well_name)

@app.route('/eval', methods=['GET'])
def eval_page():
    return render_template("evalLog/eval.html")

@app.route('/result', methods=['POST','GET'])
def result_page():
    global well_name
    well_name = "15/9-F-5"
    return render_template("evalLog/result.html",
                           NameWell=well_name)


@app.route('/hc', methods=['GET'])
def hc_page():
    global num_data_global
    script, div, cdn_js = eval_hc(num_data=8000)
    return render_template("evalLog/hc.html",
                            script=script,
                            div=div,
                            cdn_js=cdn_js)


@app.route('/facies', methods=['GET'])
def facies_page():
    global num_data_global
    script, div, cdn_js = eval_facies(num_data=8000)
    return render_template("evalLog/facies.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/well-job')
def nice():
    return render_template("good.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
