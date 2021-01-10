from django.db import models

# Create your models here.
class SongMood(models.Model):
	song_url = models.CharField(max_length=100)
	song_mood = models.CharField(max_length=100)

	def __str__(self):
		return self.song_url

