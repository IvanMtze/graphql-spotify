import spotipy
import time
import requests as request

from spotipy import SpotifyClientCredentials, util


client_id='fc7aaf9de74d4f9a8a777caeadaefd1c'
client_secret='c4f142c99f754012896b87e1712093cc'

#Credentials to access the Spotify Music Data
manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager)


url_base = 'http://40.78.153.176:8082'

#Retrieve data from server

def get_song_from_redis(ids):
	try:
		r=request.get(url_base+"/api/track/"+ids)
		if 'content-length' in r.headers.keys() and r.headers['content-length']=='0':
			return {}

		meta=r.json()
		name = meta['name']
		album = meta['album_name']
		artist = meta['album_artists_name']
		release_date = meta['release_date']
		length = meta['duration_ms']
		popularity = meta['popularity']
		ids =  meta['id']
		return meta
	except:
		pass

def get_trackmood_from_redis(ids):
	try:
		r=request.get(url_base+"/api/trackmood/"+ids)
		if 'content-length' in r.headers.keys() and r.headers['content-length']=='0':
			return {}

		return r.json()
	except:
		pass

def get_audiofeatures_from_redis(ids):
	try:
		r=request.get(url_base+"/api/audiofeatures/"+ids)

		if 'content-length' in r.headers.keys() and r.headers['content-length']=='0':
			return {}

		features=r.json()

		acousticness = features['acousticness']
		danceability = features['danceability']
		energy = features['energy']
		instrumentalness = features['instrumentalness']
		liveness = features['liveness']
		valence = features['valence']
		loudness = features['loudness']
		speechiness = features['speechiness']
		tempo = features['tempo']
		key = features['key']
		time_signature = features['time_signature']

		return features
	except:
		pass

#Post data to server
def post_song_to_redis(track):
	try:
		pload={'name':track['name'],'album_artists_name': track['album_artists_name'],'album_name':track['album_name'],'duration_ms':track['duration_ms'],'id':track['id'],'popularity':track['popularity'],'release_date':track['release_date']}
		r=request.post(url_base+"/api/track/",json=pload)
	except:
		pass

def post_trackmood_to_redis(mood):
	try:
		pload={"id": mood['url_song'],"mood":mood['mood']}
		r=request.post(url_base+"/api/trackmood/",json=pload)
	except:
		pass

def post_audio_features_to_redis(audiofeatures):
	try:
		pload={"acousticness": audiofeatures['acousticness'],
	"danceability": audiofeatures['danceability'],"energy": audiofeatures['energy'],"instrumentalness": audiofeatures['instrumentalness'],"key": audiofeatures['key'],"liveness": audiofeatures['liveness'],"loudness": audiofeatures['loudness'],"speechiness": audiofeatures['speechiness'],"tempo": audiofeatures['tempo'],"time_signature": audiofeatures['time_signature'],"uri_song": audiofeatures['uri_song'],"valence": audiofeatures['valence']}
		r=request.post(url_base+"/api/audiofeatures/",json=pload)
	except:
		pass

def get_song_from_api(ids):
	meta = sp.track(ids)
	name = meta['name']
	album = meta['album']['name']
	artist = meta['album']['artists'][0]['name']
	release_date = meta['album']['release_date']
	length = meta['duration_ms']
	popularity = meta['popularity']
	ids =  meta['id']

	pload={'name':name,'album_artists_name': artist,'album_name':album,'duration_ms':length,'id':ids,'popularity':popularity,'release_date':release_date}
	return pload


def get_features_from_api(ids):
	features = sp.audio_features(ids)
	acousticness = features[0]['acousticness']
	danceability = features[0]['danceability']
	energy = features[0]['energy']
	instrumentalness = features[0]['instrumentalness']
	liveness = features[0]['liveness']
	valence = features[0]['valence']
	loudness = features[0]['loudness']
	speechiness = features[0]['speechiness']
	tempo = features[0]['tempo']
	key = features[0]['key']
	time_signature = features[0]['time_signature']
	pload={"acousticness":acousticness,"danceability": danceability,"energy":energy,"instrumentalness":instrumentalness,"key":key,"liveness":liveness,"loudness":loudness,"speechiness":speechiness,"tempo": tempo,"time_signature": time_signature,"uri_song":ids,"valence": valence}
	return pload


def get_songs_features(ids):

	meta={}
	features={}

	#Check if exist in cache on redis
	meta=get_song_from_redis(ids)
	if not meta:
		meta=get_song_from_api(ids)
		post_song_to_redis(meta)

	features=get_audiofeatures_from_redis(ids)
	if not features:
		features=get_features_from_api(ids)
		post_audio_features_to_redis(features)


	# meta
	name = meta['name']
	album = meta['album_name']
	artist = meta['album_artists_name']
	release_date = meta['release_date']
	length = meta['duration_ms']
	popularity = meta['popularity']
	ids =  meta['id']

	# features
	acousticness = features['acousticness']
	danceability = features['danceability']
	energy = features['energy']
	instrumentalness = features['instrumentalness']
	liveness = features['liveness']
	valence = features['valence']
	loudness = features['loudness']
	speechiness = features['speechiness']
	tempo = features['tempo']
	key = features['key']
	time_signature = features['time_signature']

	track = [name, album, artist, ids, release_date, popularity, length, danceability, acousticness,
			energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature]
	columns = ['id','release_date','popularity','length','danceability','acousticness','energy','instrumentalness',
				'liveness','valence','loudness','speechiness','tempo','key','time_signature']
	return track,columns


def predict_song_mood(ids,model):
	prediction=''
	resp=get_trackmood_from_redis(ids)
	if not resp:
		prediction=model.predict_mood(ids)
		post_trackmood_to_redis({'url_song':ids,'mood':prediction})
		resp={'url_song':ids,'mood':prediction}
	return resp

		

#print(get_songs_2H7PHVdQ3mXqEHXcvclTB0("features"))
