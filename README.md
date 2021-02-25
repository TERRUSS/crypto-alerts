
# Crypto-Notifs

A simple cryptocurrency notification app in Django/Vue.js using CoinAPI
(ref https://seelk.slite.com/p/note/Q66BvgttzKN9ohAvYHK4t9)


## Getting Started

### Server

`cd server/`
You may want to use `pipenv` for the django server.

* Setup your API Key : 
	This project uses [CoinAPI](https://docs.coinapi.io/) in the backend.
	Since it is a payed service, you will need to [register](https://www.coinapi.io/Pricing) to get a key (a free one is ok).
	Next, update the `COIN_API_KEY` entry in the `server/template.env`file, and rename it to `.env`

	In short : 
	```
	echo "COIN_API_KEY=XXXXXXXX-MY-KEY" > .env
	```

* Switch to dev environment : `pipenv shell`
* Install the deps : `make init`
* Run the server in development mode (ie. expose the rest-api) : `make run`
* Run the server in production mode (like the dev mode, but detached for tty) : `make run-prod`

NOTE : You may want to get the client compiled `client/` to enjoy the web application client before start the server.

### Client

`cd client/`
* Install depencencies : `yarn # or npm i`
* build for development : `yarn serve`
* build for production : `yarn build`
	* This create a `build/` folder, which is server by the django server. Therefore, you may want to run this command before runnig the server for production