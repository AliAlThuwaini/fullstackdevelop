from flask import Flask, jsonify
import os

from flask.wrappers import Response
from flask_cors import CORS, cross_origin


# The below function (create_app) needs to be coded as is because this is what flask will look for when it runs
def create_app(test_config= None):
    #__name__ tells the app which directory it is housed in, so that if there is any additional configurations or relative paths it is looking for, it knows where it looks for. instance_relative_config: tells the app that there will be some configuration files in the same app directory. so, should be looking for them relative to the instance
    app = Flask(__name__, instance_relative_config=True)  

    #-----------------------------
        # Using CORS
    #-----------------------------

    #CORS(app)  #this is the short form and it includes all basic CORS. if to customize, see below:
    cors = CORS(app, resources={r'/api/*': {'origins': '*'}})


    app.config.from_mapping(
        #this is just for dev. for production, the key needs to be secret
        SECRET_KEY='dev',
        # database enabling:
        DATABASE=os.path.join(app.instance_path, 'flaskr_sqlite')   
    )

    if test_config is None:
        #load config from a given file in case test_config is None
        app.config.from_pyfile('config.py', silent=True)
 
    

#-----------------------------------------------------------
                        #Decorators#
#-----------------------------------------------------------

    #CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    #Allow CORS for speicifically '/messages' endpoint
    @app.route('/messages')
    @cross_origin() #This allows cross origin [for now, this is spcific for route '/messages'. If required to all pu tit under main route '/'] => need to imoport it from flask_cors to work!
    def get_messages():
        return 'GETTING MESSAGES'



    # app.route: this responds to GET requests coming from the client
    @app.route('/')
    def hello():
        # Becuase dict is not simple string, we need to jsonify in order to formatted it correctly
        return jsonify({'message': 'Hellow World'})

    @app.route('/smiley')    
    def smily():
        return ':)'



    

    # return the app instance
    return app