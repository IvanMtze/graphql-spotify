from helper import *
from model import MoodsPredicter

class Resolver():
	def __init__(self):
		self.model=MoodsPredicter()

	def get_prediction_song(self,ids):
		resp=predict_song_mood(ids,self.model)
		return resp


if __name__ == "__main__":
	resolver = Resolver()
	resolver.get_prediction_song('ID_STUFF')
