from django.db import models

# Create your models here.
class CustomBooleanField(models.IntegerField):
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return True if value else False

class Tweets(models.Model):
    index = models.IntegerField()
    batch = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    username = models.TextField(max_length=255)
    name = models.TextField(max_length=255)
    tweet = models.TextField(max_length=280)
    geo = models.CharField(max_length=25)
    positive = models.BooleanField(default=False)
    happy = models.BooleanField(default=False)
    relief = models.BooleanField(default=False)
    neutral = models.BooleanField(default=False)
    anxious = models.BooleanField(default=False)
    sad = models.BooleanField(default=False)
    negative = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.batch}_{self.index}'