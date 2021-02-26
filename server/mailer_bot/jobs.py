from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from dotenv import load_dotenv
from pathlib import Path
import os
import requests

from api.models import Subscription, CryptoValue

load_dotenv(dotenv_path=Path('.') / '.env')
API_KEY = os.getenv("COIN_API_KEY")
REFRESH_TIME = int( os.getenv("REFRESH_TIME") )

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DOMAIN = os.getenv("DOMAIN")


"""
	fetch the exchange rate of a crypto devise in USD
	@params
		devise : str (eg. 'BTC', 'XRP', ...)
	@return
		float : the exchange rate
"""
def getPrice(devise):
	endpoint = 'https://rest.coinapi.io/v1/exchangerate/'
	headers = {'X-CoinAPI-Key' : API_KEY}
	r = requests.get(endpoint+f'{devise}/USD', headers=headers)
	r = r.json()

	if ("error" in r):
		print("COINAPI ERROR :", r["error"])
		exit(1)
	return r["rate"]

"""
	init the database of cryptocurrencies with their value
	used for devises delta
"""
def initCryptoValuesDB():
	print("	*** Init crypto database ***")
	existingCryptos = Subscription.objects.values('crypto').distinct()

	for cur_crypto in existingCryptos:
		c, created = CryptoValue.objects.get_or_create(crypto=cur_crypto['crypto'])

		price = getPrice(cur_crypto['crypto'])
		c.last_price_value = price
		c.save()

		print(f'> {c.crypto} \t({c.last_price_value})')


	print()


"""
	send the nofification mail
	@params
		to: str, the reciver mail address (eg. john@doe.com)
		data: dict, containing the info :
			{
				"name": 'John',
				"crypto": 'BTH',
				"ceiling": 1000,
				"direction": 'fells under'
			}
			# will send to john@doe.com : "Hi John, the BTH just fells under 1000$" (in a pretty way oc)
"""
def sendMail(to, data):
	print('sending mail to', to, data)
	import smtplib

	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText

	me = EMAIL

	msg = MIMEMultipart('alternative')
	msg['Subject'] = f'Your crypto-notif : {data["crypto"]} just {data["direction"]} {data["ceiling"]}$'
	msg['From'] = 'CRYTPO-NOTIF'
	msg['To'] = to

	text = f'CRYTPO-NOTIF\nHi {data["name"]},\n{data["crypto"]} just {data["direction"]} {data["ceiling"]}$!'
	html = open('mailer_bot/templates/alert.html', 'r').read()
	html = html.replace('{{name}}', data["name"])
	html = html.replace('{{crypto}}', data["crypto"])
	html = html.replace('{{direction}}', data["direction"])
	html = html.replace('{{ceiling}}', str(data["ceiling"]))
	html = html.replace('{{service}}', DOMAIN)

	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	msg.attach(part1)
	msg.attach(part2)

	mail = smtplib.SMTP('smtp.gmail.com', 587)

	mail.ehlo()

	mail.starttls()

	mail.login(EMAIL, EMAIL_PASSWORD)
	mail.sendmail(me, to, msg.as_string())
	mail.quit()


def scanAlerts():
	print("	*** Scanning for alerts ***")

	notifs = Subscription.objects.order_by('crypto').all()

	for notif in notifs:
		print(f'> {notif.crypto} {"rose over" if notif.alert_on_rise else "fells under"} {notif.ceiling}', end='	')
		price = getPrice(notif.crypto)

		currentCrypto, created = CryptoValue.objects.get_or_create(crypto=notif.crypto)

		if (currentCrypto.last_price_value):
			if (notif.alert_on_rise):
				if (currentCrypto.last_price_value < notif.ceiling < price):
					print('\x1b[6;32m' + 'ALERT' + '\x1b[0m' + f'\t({price})')
					sendMail(notif.added_by.email, {
						"name": notif.added_by.username,
						"crypto": notif.crypto,
						"ceiling": notif.ceiling,
						"direction": 'rose over'
					})
				else:
					print('\x1b[6;34m' + 'NO CHANGE' + '\x1b[0m' + f'\t({price})')

			else:
				if (currentCrypto.last_price_value > notif.ceiling > price):

					print('\x1b[6;32m' + 'ALERT' + '\x1b[0m' + f'\t({price})')
					sendMail(notif.added_by.email, {
						"name": notif.added_by.username,
						"crypto": notif.crypto,
						"ceiling": notif.ceiling,
						"direction": 'fells under'
					})
				else:
					print('\x1b[6;34m' + 'NO CHANGE' + '\x1b[0m' + f'\t({price})')


		# FIXME : mb race condition here
			# price could have varied for the previous rows and we would have missed the alert...
			# adding an .order_by(crypto) to reduce the effect for now
		currentCrypto.last_price_value = price
		currentCrypto.save()

	print("	*** OK ***\n")


def start():

	initCryptoValuesDB()
	scanAlerts()

	scheduler = BackgroundScheduler()
	scheduler.add_job(scanAlerts, 'interval', minutes=REFRESH_TIME)
	scheduler.start()
