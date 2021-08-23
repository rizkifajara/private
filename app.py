from flask import Flask, render_template, request
# from flask_pymongo import PyMongo
import pandas as pd
# from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
# from pymongo import MongoClient
# import json
import os
# import dnspython

app = Flask(__name__)

@app.route("/")
def helloWorld():
    return render_template("home.html")

@app.route("/form")
def viewForm():
    return render_template("form.html")

# @app.route("/postform")
# def upload_form():
    
#     client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#     db = client.test
    
#     database_name='hackuna_matata123'
#     student_db=client[database_name]

#     collection_name='user'
#     collection=student_db[collection_name]
#     # f = request.files.get('file')
#     # mf = dataiku.Folder('O2B4wCQL') # name of the folder in the flow
#     # target_path = '/%s' % f.filename
#     # mf.upload_stream(target_path, f)

#     well = request.form.get('well')
#     lat = request.form.get('lat')
#     lon = request.form.get('lon')


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




if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

