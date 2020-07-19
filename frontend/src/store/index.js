import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    app_ip: null,
    app_port: 8000,
    manager_ip: null,
    manager_port: 8001,
    version: null,
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  }
})
