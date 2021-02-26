<template>
	<div class="modal-card" style="width: 100%; min-width: 500px">
		<header class="modal-card-head">
			<p v-if="title" class="modal-card-title">{{title}}</p>
			<p v-else class="modal-card-title">Create a new alert</p>
			<button
				type="button"
				class="delete"
				@click="$emit('close')"/>
		</header>

		<section class="modal-card-body">
			<div class=" has-text-centered is-size-4" style="margin-bottom: 20px">Alert me when...</div>
			<div style="width: 100%; height:100px; display: flex; flex-direction: row;">
				
				<b-field
					label-position="on-border"
					label="Cryptocurrency"
					style="width: 150px"
				>
					<b-autocomplete
						v-model="crypto"
						:data="filteredDataArray"
						placeholder="BTC, ETH,..."
						@select="option => selected = option">
						<template #empty>No results found</template>
					</b-autocomplete>
				</b-field>

				<div class="has-text-centered" style="margin: 10px">
					<b>{{ alertOnRise ? "rises over" : "falls under" }}</b>
					<b-field>
						<b-switch v-model="alertOnRise">
						</b-switch>
					</b-field>
				</div>

				<b-field 
					label-position="on-border"
					label="Limit"
					style="width: 200px"
				>
					<b-numberinput 
						v-model="ceiling"
						controls-alignment="right" 
						controls-position="compact"
					></b-numberinput>
				</b-field>
				<b-icon
				pack="fas"
				icon="dollar-sign"
				size="is-large"
			>
			</b-icon>
			</div>
		</section>

		<footer class="card-footer has-background-white" style="border-radius: 0 0 7px 7px">
			<a 
				class="card-footer-item"
				@click="$emit('close')"
			>
				Cancel
			</a>
			<a class="card-footer-item has-text-success"
				@click="action()"
			>
				{{edit ? "Update alert" : "Add alert"}}
			</a>
		</footer>
	</div>
</template>

<script>
import * as api from '../helpers/api.js'
import cryptos from '@/assets/all_cryptos.json'

export default {
	name: 'AddNotifModal',
	props: {
		token: String,
		title: String,
		edit: Boolean,
		data: Object
	},

	data() {
		return {
			crypto: 'BTC',
			avaliableCryptos: cryptos.all_cryptos,
			alertOnRise: true,
			ceiling: 1000,
		}
	},
	methods: {
		action: function() {
			let payload = {
				crypto: this.$data.crypto,
				ceiling: this.$data.ceiling,
				alert_on_rise: this.$data.alertOnRise,
				alert_on_fall: !this.$data.alertOnRise,
			}

			if (this.$props.edit) {
				api.put(`/api/updatenotif/${this.$props.data.id}`, payload, true)
				.then(this.$emit('close'))
			}
			else {
				api.post('/api/addnotif', payload, true)
				.then(this.$emit('close'))
			}
		},
	},
	computed: {
		filteredDataArray() {
			return this.$data.avaliableCryptos.filter((option) => {
				return option
					.toString()
					.toLowerCase()
					.indexOf(this.$data.crypto.toLowerCase()) >= 0
			})
		}
	},
	mounted() {

		if (this.$props.edit) {
			if (this.$props.data) {
				this.$data.crypto = this.$props.data.crypto
				this.$data.alertOnRise = this.$props.data.alertOnRise
				this.$data.ceiling = this.$props.data.ceiling
			}
		}
	}
}
</script>