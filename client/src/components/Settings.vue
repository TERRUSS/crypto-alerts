 <template>
	<div id="settings" class="container">
		<button 
			class="fab fab-container button is-primary"
			@click="isComponentModalActive = true"
			>
			<b-icon
				pack="fas"
				icon="cog"
				size="is-large"
			>
			</b-icon>
		</button>

		<b-modal
			v-model="isComponentModalActive"
			has-modal-card
			trap-focus
			:destroy-on-hide="false"
			aria-role="dialog"
			aria-label="Settings"
			aria-modal>
			<template>
				<div 
					class="card"
				>
					<header class="modal-card-head">
						<p class="modal-card-title">Your settings</p>
						<button
							type="button"
							class="delete"
							@click="$emit(isComponentModalActive = false)"
						/>
					</header>
					<div class="card-content">

						<div class="has-text-centered">
							<b-button 
								class="is-primary"
								size='is-large'
								@click="$emit('refresh')"
							>
								<b-icon
									style="margin-right: 3px"
									pack="fas"
									icon="sync">
								</b-icon>
								Refresh alerts
							</b-button>
						</div><br>

						<div class="content is-size-12">
<!-- 							<b-field>
								<b-switch v-model="alerts">
								<b>{{alerts ? "Alerts enabled!" : "Alerts disabled"}}</b>
								</b-switch>
							</b-field>
 -->
							<b-field
								label="Your email"
							>
								<b-input disabled placeholder="Email" :value="email" type="email"></b-input>
							</b-field>
							<p>You will receive the notifications you set up at this address.</p>
						</div>

						<div class="columns">
							<div class="column">
								<b-button 
									class="is-danger"
									@click="deleteAccount()"
								>
									<b-icon
										style="margin-right: 3px"
										pack="fas"
										icon="user-slash">
									</b-icon>
									Delete account
								</b-button>
							</div>
						</div>

					</div>
					<footer class="card-footer">
						<a class="card-footer-item" 
							@click="isComponentModalActive = false"
						>
							Close
						</a>
					</footer>
				</div>
			</template>
		</b-modal>

	</div>
</template>

<script>
import * as api from '../helpers/api.js'
export default {
	name: 'Settings',
	props: ['email', 'token'],

	data() {
		return {
			alerts: true,

			isComponentModalActive: false,
		}
	},

	methods: {
		deleteAccount: function () {
			api.post("/deleteAccount")
			.then((r)=>{
				if (r.message)
					this.$toast.success(r.message)
			})
			.catch( r => {
				if (r.error)
					this.$toast.warning(r.error)
			})
		}
	}
}
</script>

<style scoped>
.fab {
	width: 80px;
	height: 80px;
	background: #d23f31;

	position: fixed;
	top: 10px;
	left: 10px;
	z-index: 999;
	cursor: pointer;

	border-radius: 100%;
	background: #016fb9;
}
</style>
