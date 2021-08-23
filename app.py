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

from py_viz.bkapp.vsh import eval_vsh
from py_viz.bkapp.phie import eval_phie
from py_viz.bkapp.sw import eval_sw
from py_viz.bkapp.perm import eval_perm
from py_viz.bkapp.facies import eval_facies
from py_viz.bkapp.hc import eval_hc

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
    f = request.files.get['form_file']

    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test

    # return db

    
    
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
    # # f = request.files.get('file')
    # # mf = dataiku.Folder('O2B4wCQL') # name of the folder in the flow
    # # target_path = '/%s' % f.filename
    # # mf.upload_stream(target_path, f)

    # well = request.form.get('well')
    # lat = request.form.get('lat')
    # lon = request.form.get('lon')


    # # df = pd.read_csv(mf.get_download_stream(f.filename))
    
    # source = {
    #     # "filename":f.filename,
    #     #   "coordinate ": {"BAND":None, "EASTING":None,
    #     #                   "LATITUDE": lat, "LONGITUDE": lon,
    #     #                   "NORTHING": None, "WELL":well,
    #     #                   "ZONE": None},
    #     #   "data":[]
    #     "wellName": well,
    #     "latitude": lat,
    #     "longitude": lon
    # }
    
          
    
    # # for i in range(len(df)):
    # #     dict_df = {}
        
    # #     for col in df.columns:
    # #         dict_df['WELL']=well
    # #         dict_df[col]=df[col].iloc[i]
            
    # #     source['data'].append(dict_df)
    
    # print(source)
    
    # collection.insert_one(source)
    
    # return json.dumps({1})
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
