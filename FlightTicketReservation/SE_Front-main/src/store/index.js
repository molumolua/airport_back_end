import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    identity: 1, //0表示未登录，1表示用户，2表示管理员
    phoneNumber: 0,
    user: [
      //
    ],
    manager: [
      //
    ],
    currentFlight: {},
  },
  getters: {
  },
  mutations: {
    changeIdentity(state, newIdentity) {
      state.identity = newIdentity;
    },
    setPhoneNumber(state, newPhoneNumber) {
      state.phoneNumber = newPhoneNumber;
    },
    updateCurrentFlight(state, flight) {
      state.currentFlight = flight;
    }
  },
  actions: {
  },
  modules: {
  }
})
