from flask import Flask
from flask import request
from main import  Resolver 

app = Flask(__name__)

resolver=Resolver()
@app.route('/mood/<uri>')
def hello(uri):
	return resolver.get_prediction_song(uri)

if __name__ == "__main__":
	try:
		app.run()
	except:
		pass
