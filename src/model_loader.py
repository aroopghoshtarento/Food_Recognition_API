import config
from keras.models import load_model


class ModelLoader(object):
    model = None

    def __init__(self):
        if self.model is None:
            print('Loading model')
            self.model = load_model(config.MODEL_STORAGE_PATH)


    def getModel(self):
        return self.model
