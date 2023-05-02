import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUI)
//挂载axios
Vue.prototype.$https = axios
//访问根路径
axios.defaults.baseURL = "http://127.0.0.1:8000"

Vue.config.productionTip = false
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
