from flask import Flask, request, send_file, send_from_directory, Response
from flask_restful import Api, Resource
from openpyxl import workbook
import sys
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from main import Main
import settings


settings.init()

app = Flask(__name__, static_url_path=settings.PATH + '*')
api = Api(app)


class UploadFile(Resource):
    def post(self):
        try:
            file_list = request.files.getlist("uploadFile1")
            for file in file_list:
                if 'xml' in file.filename:
                    print('xml')
                    file.save(settings.PATH+'words/'+file.filename)
                else:
                    print('wav')
                    file.save(settings.PATH+'Signals/'+file.filename)
            Main.startSpreProcess()
        except:
            print("Oops!", sys.exc_info(), "occurred.")
            print("Next entry.")
            print()


class StartPreProcess(Resource):
    def get(self):
        print('start preprocess')
        try:
            Main.startPreProcess()
            return 'Finish pre process'
        except:
            print("Oops!", sys.exc_info(), "occurred.")
            print("Next entry.")
            print()
            return sys.exc_info()


class StartFirstProcess(Resource):
    def get(self):
        print('start3222')
        Main.startFirstProcess()
        try:
            return send_from_directory(directory='', path='xlsx/All_Words_With_Speaker_And_Label.xlsx', as_attachment=True)
        except:
            print("Oops!", sys.exc_info(), "occurred.")
            print("Next entry.")
            print()




class StartSecondProcess(Resource):
    def get(self):
        print('start second',Resource)
        x = Main.startSecondProcess()
        return Response(x.to_json(orient="records"), mimetype="application/json")



class GetXlsx(Resource):
    def get(self):
        print('get data for diagram', Resource)
        try:
            return send_from_directory(directory='', path='xlsx/Data_Frame_With_Labels_And_Clusters.xlsx', as_attachment=True)
        except:
            print("Oops!", sys.exc_info(), "occurred.")
            print("Next entry.")
            print()


api.add_resource(StartPreProcess, "/preprocess")
api.add_resource(UploadFile, "/upload_file")
api.add_resource(StartFirstProcess, "/start_first_process")
api.add_resource(StartSecondProcess, "/start_second_process")
api.add_resource(GetXlsx, "/data_for_diagram")

# if __name__ == "__main__":
app.run(debug=True)
