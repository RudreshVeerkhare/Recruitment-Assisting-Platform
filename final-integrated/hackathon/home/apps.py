from django.apps import AppConfig
from django.conf import settings
import os
import pickle

class HomeConfig(AppConfig):
    name = 'home'
    
    lda_model_path = os.path.join(settings.MODELS, 'lda_model.pkl')
    df_path = os.path.join(settings.MODELS, 'data-frame.pkl')
    dict_path = os.path.join(settings.MODELS, 'dict.pkl')
 
    # load models into separate variables
    # these will be accessible via this class
    with open(lda_model_path, 'rb') as pickled:
       lda_model = pickle.load(pickled)
    with open(df_path, 'rb') as pickled:
       df = pickle.load(pickled)
    with open(dict_path, 'rb') as pickled:
       dictionary = pickle.load(pickled)