
# Crypto-Notifs

A simple cryptocurrency notification app in Django/Vue.js using CoinAPI
(ref https://seelk.slite.com/p/note/Q66BvgttzKN9ohAvYHK4t9)


## Getting Started

### Server

`cd server/`
You may want to use `pipenv` for the django server.

* Setup your API Key and email account : 
	This project uses [CoinAPI](https://docs.coinapi.io/) in the backend.
	Since it is a payed service, you will need to [register](https://www.coinapi.io/Pricing) to get a key (a free one is ok).
	Next, update the `COIN_API_KEY` entry in the `server/template.env`file, and rename it to `.env`

	Or : 
	```
	echo "COIN_API_KEY=XXXXXXXX-MY-KEY" > .env
	```

As well, you can specify a `REFRESH_TIME` constant in minutes, corresponding to the time the server waits between the fetchs of currencies exchange rate (thus, the precision of the alert). Default is 15 minutes, to match with the free tiers subscription to CoinAPI (`24*60 min in a day / 100 requests = 15 min of interval`) ; you will have to upgrade for a better precision.

Next, you will have to provide SMTP credentials in the same file for the mail account used to notify the clients. In short your `.env` file should look like this :
```
COIN_API_KEY=XXXXXXXX-MY-KEY
REFRESH_TIME=15

EMAIL='mail@example.com'
EMAIL_PASSWORD='p@sswrlD'
DOMAIN='https://your.domain.name' # <- this is for the mail body
```

* Switch to dev environment : `pipenv shell`
* Install the deps : `make init`
* Run the server in development mode (ie. expose the rest-api) : `make run`

NOTE : You may want to get the client compiled `client/` to enjoy the web application client before start the server.

NOTE2 : Also, change the SECRET_KEY value in `server/crypto_notif/settings.py` before pushing to production ;)
### Client

`cd client/`
* Install depencencies : `yarn # or npm i`
* build for development : `yarn serve`
* build for production : `yarn build`
	* This create a `build/` folder, which is server by the django server. Therefore, you may want to run this command before runnig the server for production
