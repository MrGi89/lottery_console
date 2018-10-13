import json
from flask import request, session
from flask_restful import Resource


class UserController(Resource):

    def get(self, action, id):

        if action == 'get':
            
            pass

        if action == 'get_all':

            pass
