from flask import Flask, request
from flask_restful import Api, Resource

app = Flask('asdf')
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {"data": "Hello world"}


class UploadFile(Resource):
    def post(self):
        audio_file = request.files
        print(audio_file)
        return {"data": "Hello world"}


api.add_resource(HelloWorld, "/helloworld")
api.add_resource(UploadFile, "/audio_file")

# if __name__ == "__main__":
app.run(debug=True)
