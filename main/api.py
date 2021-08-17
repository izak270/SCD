from flask import Flask, request
from flask_restful import Api, Resource
import Main
app = Flask('asdf')
api = Api(app)

class start(Resource):
    def get(self):
        Main.startMain()
        return {"data": "Hello world"}


class UploadFile(Resource):
    def post(self):
        audio_file = request.files
        print(audio_file)
        return {"data": "Hello world"}


api.add_resource(start, "/start")
api.add_resource(UploadFile, "/audio_file")

# if __name__ == "__main__":
app.run(debug=True)
