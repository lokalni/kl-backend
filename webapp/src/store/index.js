import Vue from 'vue'
import Vuex from 'vuex'
import {ROUTE_NAMES} from "@/router";
import router from "@/router";
import {Accounts} from '@/api';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    user: null,
  },
  mutations: {
    setUser(state, data) {
      state.user = data;
    }
  },
  actions: {
    async login(context, {email, password}) {
      const userData = await Accounts.login({email, password});
      window.console.log("User logged in:", userData);
      context.commit('setUser', userData);
    },
    async logout(context) {
      await Accounts.logout();
      context.commit('setUser', null);
      router.push({name: ROUTE_NAMES.MAIN});
    }
  },
  modules: {
  },
})
