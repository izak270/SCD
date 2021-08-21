from flask import Flask, request, send_file, send_from_directory
from flask_restful import Api, Resource
from openpyxl import workbook
import sys
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from main import Main

app = Flask(__name__, static_url_path='')
api = Api(app)

class StartPreProcess(Resource):
    def post(self):
        print('start1')
        # Main.startMain()

        try:
            # return send_from_directory(
            #     app.config['main'], 'Data_Frame_WithLabels.xlsx', as_attachment=True
            # )
            # return 'yes'
            return send_from_directory(directory='', path='Data_Frame_WithLabels.xlsx', as_attachment=True)
        except:
            print("Oops!", sys.exc_info(), "occurred.")
            print("Next entry.")
            print()

        # return ('Data_Frame_WithLabels.xlsx')


class UploadFile(Resource):
    def post(self):
        # print(type(request.files))
        # audio_file = request.data
        # print(audio_file)
        # # if 'file' not in request.files:
        # #     print('No file part')
        # file = request.files['file']
        # # # If the user does not select a file, the browser submits an
        # # # empty file without a filename.
        # # if file.filename == '':
        # #     print('No selected file')
        # # if file:
        # filename = secure_filename(request.files[0])
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return {"data": "Hello world"}


api.add_resource(StartPreProcess, "/start_pre_process")
api.add_resource(UploadFile, "/audio_file")

# if __name__ == "__main__":
app.run(debug=True)
