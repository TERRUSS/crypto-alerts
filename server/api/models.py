from django.db import models
from django.conf import settings
from django.utils import timezone

		# All subscriptions
class Subscription(models.Model):
	crypto = models.CharField(max_length=200)
	ceiling = models.BigIntegerField()
	alert_on_fall = models.BooleanField()
	alert_on_rise = models.BooleanField()
	added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	created_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.crypto




		# Used to store intermediates values for cryptos
			# todo : delete entry while there are no more references in the subscription model
class CryptoValue(models.Model):
	crypto = models.CharField(max_length=200, primary_key=True)
	last_price_value = models.FloatField(null=True, blank=True)

	def __str__(self):
		return self.crypto