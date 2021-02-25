<template>
	<div>
		<button 
			class="fab fab-container button is-danger"
			@click="isComponentModalActive = true"
		>
			<b-icon
				pack="fas"
				icon="plus"
				size="is-large"
			>
			</b-icon>
		</button>

		<b-modal
			v-model="isComponentModalActive"
			has-modal-card
			trap-focus
			:destroy-on-hide="false"
			:on-cancel="() => { $emit('refresh') ;}"
			aria-role="dialog"
			aria-label="Add Notif Modal"
			aria-modal>
			<template>
				<AddNotifModal 
					@close="isComponentModalActive = false ; $emit('refresh')"
				></AddNotifModal>
			</template>
		</b-modal>
	</div>
</template>

<script>
import AddNotifModal from './AddNotifModal.vue'

export default {
	name: 'AddNotifBtn',
	components: {AddNotifModal},
	props: ['login'],

	data() {
		return {
			isComponentModalActive: false,
			formProps: {
				email: 'evan@you.com',
				password: 'testing'
			}
		}
	},
	mounted() {
	}
}
</script>

<style scoped>
.fab {
	width: 80px;
	height: 80px;
	background: #d23f31;

	position: fixed;
	bottom: 50px;
	right: 50px;
	z-index: 999;
	cursor: pointer;

	border-radius: 100%;
	background: #016fb9;
}
</style>
