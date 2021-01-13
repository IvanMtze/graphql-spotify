#Script to obtain data 
from helper import *

#Basic stuff
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns

#Librerias para crear el modelo multiclase
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils

import tensorflow as tf
tf.compat.v1.disable_eager_execution()
tf.compat.v1.disable_v2_behavior()

#Para validación de modelo
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn.preprocessing import LabelEncoder,MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score


class MoodsPredicter(): 
	def __init__(self):
		self.df = pd.read_csv("./data/data_moods.csv")

		self.col_features = self.df.columns[6:-3]
		self.X= MinMaxScaler().fit_transform(self.df[self.col_features])
		self.X2 = np.array(self.df[self.col_features])
		self.Y = self.df['mood']

		#Encode the categories
		self.encoder = LabelEncoder()
		self.encoder.fit(self.Y)
		self.encoded_y =self.encoder.transform(self.Y)


		#Convertir a  dummy (NND)
		self.dummy_y = np_utils.to_categorical(self.encoded_y)

		self.X_train,self.X_test,self.Y_train,self.Y_test = train_test_split(self.X,self.encoded_y,test_size=0.2,random_state=15)

		self.target = pd.DataFrame({'mood':self.df['mood'].tolist(),'encode':self.encoded_y}).drop_duplicates().sort_values(['encode'],ascending=True)
		

	def base_model(self):
		#Modelo
		self.model = Sequential()
		#Agrega 1 capa con 8 nodos, entrada de 4 dimensiones con funcion relu
		self.model.add(Dense(8,input_dim=10,activation='relu'))
		#Agrega 1 capa con salida 3 y funcion softmax
		self.model.add(Dense(4,activation='softmax'))
		#Compila el modelo usando funcion de perdida de sigmoid y adam optim
		self.model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
		return self.model

	def configure(self):
		#Configura el modelo
		self.estimator = KerasClassifier(build_fn=base_model,epochs=300,batch_size=200,verbose=0)

		#Evalua el modelo usando KFold cross validation
		self.kfold = KFold(n_splits=10,shuffle=True)
		self.results = cross_val_score(estimator,X,encoded_y,cv=kfold)
		#print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100,results.std()*100))

		self.estimator.fit(self.X_train,self.Y_train)
		self.y_preds = self.estimator.predict(self.X_test)

		#Matriz de confusión
		self.cm = confusion_matrix(Y_test,y_preds)
		self.ax = plt.subplot()
		sns.heatmap(self.cm,annot=True,ax=self.ax)

		self.labels = self.target['mood']
		self.ax.set_xlabel('Predicted labels')
		self.ax.set_ylabel('True labels')
		self.ax.set_title('Confusion Matrix')
		self.ax.xaxis.set_ticklabels(self.labels)
		self.ax.yaxis.set_ticklabels(self.labels)
		#plt.show()


	def predict_mood(self,id_song):
		#Cruza el modelo y scaler en un Pipeline
		pip = Pipeline([('minmaxscaler',MinMaxScaler()),('keras',KerasClassifier(build_fn=self.base_model,epochs=300,batch_size=200,verbose=0))])
		#Ajusta el Pipeline
		pip.fit(self.X2,self.encoded_y)

		#Obtiene las caracteristicas de la cancion
		preds = get_songs_features(id_song)

		#Pre-procesa las caracteristicas para la entrada del modelo
		preds_features = np.array(preds[0][6:-2]).reshape(-1,1).T

		#Predice las caracteristicas de la cancion
		results = pip.predict(preds_features)

		mood = np.array(self.target['mood'][self.target['encode']==int(results)])
		name_song = preds[0][0]
		artist = preds[0][2]
		return str(mood[0].upper())

#print("Accuracy Score",accuracy_score(Y_test,y_preds))
#smp = MoodsPredicter()
#print(mp.predict_mood('2H7PHVdQ3mXqEHXcvclTB0'))
