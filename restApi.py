import json
from flask import Flask
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bbc_db'
api = Api(app)
mongo = PyMongo(app)


class getAllNews(Resource):
    """ REST Get All news articles """

    def get(self):
        res = [n for n in mongo.db.articles.find({})]
        return json.dumps(res, default=json_util.default)


class getHeadlines(Resource):
    """ REST API to get only Headlines """

    def get(self):
        res = [
            n['headline']
            for n in mongo.db.articles.find({'headlines': {
                "$ne": " "
            }})
        ]
        return json.dumps(res, default=json_util.default)


class getAuthors(Resource):
    """ REST API to get only Authors"""

    def get(self):
        res = [
            n['author']
            for n in mongo.db.articles.find({'author': {
                "$ne": " "
            }})
        ]
        return json.dumps(res, default=json_util.default)


# MAP API to URL
api.add_resource(getAllNews, '/')
api.add_resource(getHeadlines, '/getHeadlines')
api.add_resource(getAuthors, '/getAuthors')

if __name__ == '__main__':
    app.run(debug=True)
