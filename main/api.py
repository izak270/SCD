from flask import Flask, request, send_file, send_from_directory, Response
from flask_restful import Api, Resource
from openpyxl import workbook
import sys
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from main import Main
import numpy as np

app = Flask(__name__, static_url_path='')
api = Api(app)


class UploadFile(Resource):
    def post(self):
        Main.startSpreProcess()
        return {"data": "upload file"}


class StartFirstProcess(Resource):
    def get(self):
        print('start3')
        Main.startFirstProcess()
        try:
            return send_from_directory(directory='', path='Data_Frame_WithLabels.xlsx', as_attachment=True)
        except:
            print("Oops!", sys.exc_info(), "occurred.")
            print("Next entry.")
            print()

        return ('Data_Frame_WithLabels.xlsx')


class StartSecondProcess(Resource):
    def get(self):
        print('start second',Resource)
        Main.startSecondProcess()
        try:
            return send_from_directory(directory='', path='Data_Frame_WithLabels.xlsx', as_attachment=True)
        except:
            print("Oops!", sys.exc_info(), "occurred.")
            print("Next entry.")
            print()

        # return ('Data_Frame_WithLabels.xlsx')


class GetDataForDiagram(Resource):
    def get(self):
        print('get data for diagram',Resource)
        x = Main.startMain()
        return Response(x.to_json(orient="records"),mimetype="application/json")
        # try:
        #     return send_from_directory(directory='', path='Data_Frame_WithLabels.xlsx', as_attachment=True)
        # except:
        #     print("Oops!", sys.exc_info(), "occurred.")
        #     print("Next entry.")
        #     print()

        # return ('Data_Frame_WithLabels.xlsx')

api.add_resource(UploadFile, "/upload_file")
api.add_resource(StartFirstProcess, "/start_first_process")
api.add_resource(StartSecondProcess, "/start_second_process")
api.add_resource(GetDataForDiagram, "/data_for_diagram")

# if __name__ == "__main__":
app.run(debug=True)
