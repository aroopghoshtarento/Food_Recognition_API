from flask_restful import fields, marshal_with, reqparse, Resource
import os
import config
import logging
import magic
import cv2
from flask.json import jsonify
from app import model
from repositories import FoodRecognition

import keras
from keras.applications.inception_v3 import preprocess_input

def check_image_file_id(id):
    if os.path.exists(os.path.join(config.FILE_STORAGE_PATH, id)) and os.path.isfile(os.path.join(config.FILE_STORAGE_PATH, id)):
        f           = magic.Magic(mime=True, uncompress=True)
        fileType    = f.from_file(os.path.join(config.FILE_STORAGE_PATH, id))
        if   fileType == 'image/jpeg' or fileType == 'image/jpg'  or fileType == 'image/png':
            logging.debug("file id %s is a valid %s image file" % (id, fileType))
            return id
        else:
            logging.debug("file id %s is not a valid image file" % (id))
            raise ValueError("file id {} doesn't exists".format(id))
    else:
        logging.debug("file id %s doesn't exists" % (id))
        raise ValueError("file id {} doesn't exists".format(id))

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('Content-Type', location='headers', type=str, help='Please set Content-Type as application/json')
#parser.add_argument('image_file_id', location='json', type=check_image_file_id, help='Please provide valid image_file_id in JPEG/PNG format', required=True)

class RectResource(Resource):

    process_image = None

    def __init__(self):
        if self.process_image is None:
            self.process_image = preprocess_input


    def get(self):
        args            = parser.parse_args()
        food_recog      = FoodRecognition(config.FILE_STORAGE_PATH,model, self.process_image)
        recipe_name     = food_recog.main()
        # keras.backend.tensorflow_backend.clear_session()

        return {
            'status': {
                'code' : 200,
                'message' : 'api successful'
            },
            'recipe_name': str(recipe_name)
        }
