import Vue from 'vue'
import App from './App.vue'
import 'element-ui/lib/theme-chalk/index.css'
import 'frontend1080-ui/lib/index.css'
import axios from 'axios'

//挂载axios
Vue.prototype.$https = axios
//访问根路径
axios.defaults.baseURL = "http://127.0.0.1:1101"

Vue.config.productionTip = false
new Vue({
  render: h => h(App),
}).$mount('#app')
