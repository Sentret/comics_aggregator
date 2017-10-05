from django.db import models

class ComicsBook(models.Model):
	title = models.CharField(max_length=100)
	image_url = models.URLField(max_length=50)
	price = models.IntegerField()
	href = models.URLField(max_length=50)
	source = models.CharField(max_length=25)

	def __str__(self):
		return self.title