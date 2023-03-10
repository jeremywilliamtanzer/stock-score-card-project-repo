from fastapi import FastAPI

api = FastAPI()

@api.get('/')
def index():
    return {'ok': 'api connected'}

#always add @api.get as a root
@api.get('/my_calc')
def my_calc(feature1, features2):
    return {'results': (float(feature1) + float(features2))}
