<template>
	<div id="notifs" class="container">
		<h1 class="is-size-1 has-text-white" style="margin-bottom: 40px;">Alert me when...</h1>
		<div 
			v-if="!loading"
		>			
			<div 
				class="card cnotif" aria-id="contentIdForA11y3"
				v-for="(notif, index) in notifs"
				:key="notif.id"
			>
				<div class="card-content">
					<div class="content is-size-5">
						<div style="width: 100%; display: flex; flex-direction: row; justify-content: space-between;">
							<p>
								<b>{{notif.crypto}}</b> 
								{{notif.alert_on_rise ? "reaches" : "falls under"}} 
								<b>{{notif.ceiling}}</b>$
							</p>
							<a>#{{notif.crypto}}</a>
						</div>
					</div>
				</div>
				<footer class="card-footer">
					<a 
						class="card-footer-item" 
						@click="isComponentModalActive = true; notif_index=index"
					>
						<b-icon
							pack="fas"
							icon="edit">
						</b-icon>
					</a>
					<a 
						class="card-footer-item has-text-danger"
						@click="deleteNotif(notif.id)"
					>
						<b-icon
							pack="fas"
							icon="trash">
						</b-icon>
					</a>
				</footer>
			</div>

			<div v-if="!notifs || !notifs.length">
				<div class="has-text-centered has-text-white">
					<b-icon
						pack="fas"
						size="is-large"
						icon="frog">
					</b-icon><br>
					Wow, such empty
				</div>
			</div>
		</div>

		<div v-else>
			<div 
				class="card cnotif" aria-id="contentIdForA11y3"
				v-for="index in 10"
				:key="index"
			>
				<div class="card-content">
					<div class="content is-size-5">
						<b-skeleton size="is-large" active :count="2"></b-skeleton>
					</div>
				</div>
				<footer class="card-footer">
					<a class="card-footer-item">
						<b-skeleton size="is-large" active></b-skeleton>
					</a>
					<a class="card-footer-item has-text-danger">
						<b-skeleton size="is-large" active></b-skeleton>
					</a>
				</footer>
			</div>
		</div>


		<b-modal
			v-model="isComponentModalActive"
			has-modal-card
			trap-focus
			:destroy-on-hide="false"
			:on-cancel="() => $emit('refresh')"
			aria-role="dialog"
			aria-label="Add Notif Modal"
			aria-modal>
			<template #default="props">
				<AddNotifModal 
					title="Edit alert"
					edit
					:data="notifs[notif_index]"
					@close="props.close; $emit('refresh')"
				></AddNotifModal>
			</template>
		</b-modal>

	</div>
</template>

<script>
import AddNotifModal from './AddNotifModal.vue'
import * as api from '../helpers/api.js'

export default {
	name: 'NotifsList',
	components: {AddNotifModal},
	props: ['notifs', 'loading'],

	data() {
		return {
			isComponentModalActive: false,

			notif_index: -1
		}
	},

	methods: {
		deleteNotif (notifID) {
			api.request_delete(`/api/deletenotif/${notifID}`)
			.then(()=>{
				this.$toast.danger("Alert deleted")
			})

			this.$emit("refresh")
		}
	}
}
</script>

<style scoped>
	#notifs {
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-align: center;
		margin-top: 20px;
		max-width: 700px;
	}

	.cnotif {
		margin-bottom: 40px;
	}
</style>
