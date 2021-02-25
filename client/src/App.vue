<template>
	<div id="app">

			<!-- App -->
		<div v-if="token">
			<NotifsList 
				:token="token"
				:notifs="notifs"
				:loading="loadingNotifs"
				@refresh="fetchNotifs()"
			/>
		
			<AddNotifBtn 
				:token="token" 
				@refresh="fetchNotifs()"
			/>
			<Settings 
				:email="email" 
				:token="token"
				@refresh="fetchNotifs()"
			/>
		</div>

			<!-- Login -->
		<div v-else class="container hero-body" style="margin-top: 50px">
			<div class="columns is-centered is-5-tablet is-4-desktop is-3-widescreen">
				<div class="box">
					<div style="display: flex; flex-direction: row; justify-content: space-between;">
						<h1 class="is-size-3">{{isLogin ? "Login" : "Register"}}</h1>
						<b-button 
							class="is-primary"
							@click="isLogin=!isLogin"
						>{{isLogin ? "Register" : "Login"}}</b-button>						
					</div>
					<div class="is-divider"></div>
					<b-field label="Email">
						<b-input
							type="email"
							v-model="email"
							placeholder="Your email"
							required
							icon-pack="fas"
							icon="envelope">
						</b-input>
					</b-field>
					<b-field label="Username" v-if="!isLogin">
						<b-input
							type="username"
							v-model="username"
							placeholder="Your username"
							required
							icon-pack="fas"
							icon="user">
						</b-input>
					</b-field>
					<b-field label="Password">
						<b-input
							type="password"
							v-model="password"
							password-reveal
							placeholder="Your password"
							required
							icon-pack="fas"
							icon="lock">
						</b-input>
					</b-field>
					<div style="display: flex; flex-direction: row-reverse;">
						<b-button 
							@click="email = 'olivier@benaben.space'"
						>
							<b-icon
								style="margin-left: 3px"
								pack="fas"
								icon="star">
							</b-icon>
						</b-button>
						<b-button 
							class="is-success"
							@click="loginAction()"
						>
							{{isLogin ? "Login" : "Register"}}
							<b-icon
								style="margin-left: 3px"
								pack="fas"
								icon="frog">
							</b-icon>
						</b-button>
					</div>
				</div>
			</div>
		</div>

	</div>
</template>

<script>
import NotifsList from './components/NotifsList.vue'
import AddNotifBtn from './components/AddNotifBtn.vue'
import Settings from './components/Settings.vue'
import * as api from './helpers/api.js'

export default {
	name: 'App',
	components: {
		NotifsList, AddNotifBtn, Settings
	},

	data(){
		return {
			isLogin: true,
			username: '',
			email: '',
			password: '',

			token: false,

			notifs: [],
			loadingNotifs: true
		}
	},

	methods: {
		fetchNotifs(){
			api.get('/api/getnotifs')
			.then(res => {
				this.$data.notifs = res.notifications
				this.$data.loadingNotifs = false
			})
			.catch(console.warn)
		},


		register() {
			api.post('/registration/', {
				username: this.$data.username,
				email: this.$data.email,
				password1: this.$data.password,
				password2: this.$data.password,
			}, false)
			.then(res => {
				console.log(res)
				this.do_login(res.key)
			})
			.catch(e => {
				console.warn(e)
			})
		},

		login() {
			api.post('/login/', {
				email: this.$data.email,
				password: this.$data.password,
			}, false)
			.then(res => {
				if (res.key){
					this.do_login(res.key)
				}
				else {
					this.$toast.warning("Something went wrong")
				}
			})
			.catch(e => {
				this.$toast.warning(e)
			})
		},

		loginAction() {
			if (this.$data.isLogin)
				this.login()
			else
				this.register()
		},

		do_login (token) {
			this.$data.token = token;
			window.localStorage.setItem('token', token)
			this.$toast.success("Good to see you !")					
			this.fetchNotifs()
		}
	},
	created(){
		setInterval(()=>{
			if (this.$data.token)
				this.fetchNotifs();
		}, 60*1000) // safely update every minute
	}
}
</script>


<style>
	html,body{
		height: 100%;
		background-color: #48c78e;
	}

	#app {
		padding: 5px;
	}

	.is-divider{
		display: block;
		border-top: .1rem solid #dbdbdb;
		height: 1rem;
		width: 80%;
		margin-left: 10%;
	}
</style>