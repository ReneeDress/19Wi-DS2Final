import Vue from 'vue'
import App from './App.vue'
import ElementUI from '../node_modules/element-ui';
import '../node_modules/element-ui/lib/theme-chalk/index.css';
import VueRouter from "vue-router";
import axios from 'axios'
import qs from 'qs'

Vue.use(qs)
Vue.use(axios)
Vue.use(VueRouter);
Vue.use(ElementUI)

Vue.config.productionTip = false

Vue.prototype.$axios = axios

const router = new VueRouter({
  mode: "history",
  routes: [
    //{ path: "/", redirect: "/HelloWorld" },
    { path: "/", component: () => import("@/components/HelloWorld.vue") },
    { path: "/Detail", component: () => import("@/components/Detail.vue") },
    //{ path: "*", component: NotFoundComponent}
  ]
});

new Vue({
  render: h => h(App),
  router,
}).$mount('#app')
