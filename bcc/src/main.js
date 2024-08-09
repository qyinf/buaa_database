import Vue from 'vue'
import App from './App.vue'
import Router from "@/router";
//引入vuex
// import store from "@/store"
//引入vue-router
import VueRouter from "vue-router";
import ElementUI from 'element-ui';
import Vuetify from "vuetify";
import * as echarts from "echarts";
import 'element-ui/lib/theme-chalk/index.css';
import axios from "axios";
import vuetify from './plugins/vuetify'
import 'mavon-editor/dist/css/index.css'
import mavonEditor from 'mavon-editor'
import htmlToPdf from "@/components/htmlToPdf";
import '@mdi/font/css/materialdesignicons.css'
Vue.use(htmlToPdf)
Vue.use(ElementUI)
Vue.use(Vuetify)
Vue.use(mavonEditor)
Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.prototype.$axios = axios;
Vue.prototype.$echarts = echarts;

new Vue({
  el: "#app",
  render: h => h(App),
  router: Router,
  vuetify,
  beforeCreate() {
    Vue.prototype.$bus = this //安装全局事件总线（任意组件间通信）
  }
})
