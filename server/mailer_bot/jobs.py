from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv
from pathlib import Path
import os
import requests

from api.models import Subscription, CryptoValue

load_dotenv(dotenv_path=Path('.') / '.env')
API_KEY = os.getenv("COIN_API_KEY")


def getPrice(devise):
	endpoint = 'https://rest.coinapi.io/v1/exchangerate/'
	headers = {'X-CoinAPI-Key' : API_KEY}
	r = requests.get(endpoint+f'{devise}/USD', headers=headers)

	try:
		r.raise_for_status()
		r = r.json()
		return r["rate"]
	except:
		return None

def initCryptoValuesDB():
	print("	*** Init crypto database ***")
	existingCryptos = Subscription.objects.values('crypto').distinct()

	for cur_crypto in existingCryptos:
		c, created = CryptoValue.objects.get_or_create(crypto=cur_crypto['crypto'])
		# if (created):
		# 	c = created
		c.last_price_value = getPrice(cur_crypto['crypto'])
		c.save()

		print(f'> {c.crypto} \t({c.last_price_value})')


	print()

def sendAlerts():
	print("	*** Scanning for alerts ***")

	notifs = Subscription.objects.order_by('crypto').all()

	for notif in notifs:
		print(f'> {notif.crypto} {"rise over" if notif.alert_on_rise else "falls under"} {notif.ceiling}', end='	')
		price = getPrice(notif.crypto)

		currentCrypto, created = CryptoValue.objects.get_or_create(crypto=notif.crypto)
		# if (created):
		# 	currentCrypto = created

		if (currentCrypto.last_price_value):
			if (notif.alert_on_rise):
				if (currentCrypto.last_price_value < notif.ceiling < price):
					print('\x1b[6;32m' + 'ALERT' + '\x1b[0m' + f'\t({price})')
				else:
					print('\x1b[6;34m' + 'NO CHANGE' + '\x1b[0m' + f'\t({price})')

			else:
				if (currentCrypto.last_price_value > notif.ceiling > price):
					print('\x1b[6;32m' + 'ALERT' + '\x1b[0m' + f'\t({price})')
				else:
					print('\x1b[6;34m' + 'NO CHANGE' + '\x1b[0m' + f'\t({price})')


		# FIXME : race condition here
			# price could have varied for the previous rows and we would have missed the alert...
			# adding an .order_by(crypto) to reduce the effect for now
		currentCrypto.last_price_value = price
		currentCrypto.save()

	print("	*** OK ***\n")



def start():

	# initCryptoValuesDB()
	# sendAlerts()

	scheduler = BackgroundScheduler()
	scheduler.add_job(sendAlerts, 'interval', minutes=1)
	scheduler.start()
