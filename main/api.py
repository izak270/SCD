from flask import Flask, request, send_file, send_from_directory
from flask_restful import Api, Resource
from openpyxl import workbook
import sys

app = Flask(__name__, static_url_path='')
api = Api(app)

class StartPreProcess(Resource):
    def post(self):
        # Main.startMain()
        print('start1')
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
        audio_file = request.files
        print(audio_file)
        return {"data": "Hello world"}


api.add_resource(StartPreProcess, "/start_pre_process")
api.add_resource(UploadFile, "/audio_file")

# if __name__ == "__main__":
app.run(debug=True)
