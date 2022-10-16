import Vue from 'vue'
import 'normalize.css/normalize.css'

import App from './App.vue'
import ElementUI from 'element-ui'
import '@/styles/index.scss' // global css
import 'element-ui/lib/theme-chalk/index.css'

import '@/icons' // icon
import '@/permission' // permission control

import store from './store'
import router from './router'

Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
