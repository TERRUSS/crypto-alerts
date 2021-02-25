import * as config from './config.js'

function post (ressource, data, send_token) {
	return new Promise( (resolve, reject) => {
		let headers = {
			"Content-Type": "application/json;charset=UTF-8"
		}
		if (send_token!== false)
			headers = {
				...headers,
				'Authorization': 'Token '+window.localStorage.getItem('token')
			}

		console.log('fetching', ressource, headers)


		fetch(config.api_endpoint+ressource, {
			'method': "POST",
			'headers': headers,
			// mode: 'cors',
			'body': JSON.stringify(data)
		})
		.then(response => {
			if (!response.ok) {
				reject("email/password tuple doesn't match")
			}
			else return response
		})
		.then(response => response.json())
		.then(response => {
			resolve(response)
		})
		.catch(e => {
			reject(JSON.stringify(e))
		})
	})
}

function get (ressource) {
	// console.log(data)
	return new Promise( (resolve, reject) => {
		fetch(config.api_endpoint+ressource, {
			method: "GET",
			headers: {
				"Content-Type": "application/json;charset=UTF-8",
				'Authorization': 'Token '+window.localStorage.getItem('token'),
			},
		})
		.then(response => {
			if (!response.ok) {
				reject("email/password tuple doesn't match")
			}
			else return response
		})
		.then(response => response.json())
		.then(response => {
			resolve(response)
		})
		.catch(e => {
			reject(JSON.stringify(e))
		})
	})
}

function put (ressource, data, send_token) {
	return new Promise( (resolve, reject) => {
		let headers = {
			"Content-Type": "application/json;charset=UTF-8"
		}
		if (send_token!== false)
			headers = {
				...headers,
				'Authorization': 'Token '+window.localStorage.getItem('token')
			}

		console.log('fetching', ressource, headers)


		fetch(config.api_endpoint+ressource, {
			'method': "PUT",
			'headers': headers,
			// mode: 'cors',
			'body': JSON.stringify(data)
		})
		.then(response => {
			if (!response.ok) {
				reject("email/password tuple doesn't match")
			}
			else return response
		})
		.then(response => response.json())
		.then(response => {
			resolve(response)
		})
		.catch(e => {
			reject(JSON.stringify(e))
		})
	})
}

function request_delete (ressource, data, send_token) {
	return new Promise( (resolve, reject) => {
		let headers = {
			"Content-Type": "application/json;charset=UTF-8"
		}
		if (send_token!== false)
			headers = {
				...headers,
				'Authorization': 'Token '+window.localStorage.getItem('token')
			}

		console.log('fetching', ressource, headers)


		fetch(config.api_endpoint+ressource, {
			'method': "DELETE",
			'headers': headers,
			// mode: 'cors',
			'body': JSON.stringify(data)
		})
		.then(response => {
			if (!response.ok) {
				reject("email/password tuple doesn't match")
			}
			else return response
		})
		.then(response => response.json())
		.then(response => {
			resolve(response)
		})
		.catch(e => {
			reject(JSON.stringify(e))
		})
	})
}

export {
	post, get, put, request_delete
}


// olivier@benaben.space
// dRanX24MmbUGyf2
// 95b4458c41c672bb402aa5c951aca27b4039e79e