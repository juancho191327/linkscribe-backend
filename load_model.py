import typing
from pathlib import Path

class model_load(object):
    def __init__(self):
        self.model=self.__load_sklearn_model()
      
    def __load_sklearn_model(self):
        """"
        Load sklearn model from path
        """
        path = 'models/sklearn/web_scrapper.pk'
        import pickle
        with open(path, "rb") as f:
            return pickle.load(f) 
    
    def predict(self,data):
        prediction=self.model.predict(data)
        modelo=model_load()
        return (modelo.clases(prediction[0]))
    
    def clases(self,data):
        clases=['Adult', 'Business/Corporate', 'Computers and Technology',
       'E-Commerce', 'Education', 'Food', 'Forums', 'Games',
       'Health and Fitness', 'Law and Government', 'News', 'Photography',
       'Social Networking and Messaging', 'Sports', 'Streaming Services',
       'Travel']
        return clases[data]





