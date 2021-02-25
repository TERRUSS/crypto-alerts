import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

Vue.use(Buefy)

import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

Vue.use(Toast, {});

new Vue({
  render: h => h(App),
}).$mount('#app')
