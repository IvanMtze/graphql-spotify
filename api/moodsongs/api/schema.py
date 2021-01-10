import graphene
from graphene_django import DjangoObjectType
from moodsongs.api.models import SongMood
from moodsongs.api.main import Resolver
class SongMoodType(DjangoObjectType):
	class Meta:
		model=SongMood
		fields=("url_song","mood")

class Query(graphene.ObjectType):
	song_url = String(url_song=String(default_value=""))
	mood = String()
	responder=Resolver()
	def resolve_song_url(root,info,url):
		return responder.get_prediction_song(url)
schema = Schema(query=Query)
