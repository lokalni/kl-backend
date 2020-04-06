<template>
    <div v-if="user" id="nav">
<!--        <router-link to="/">Informacje</router-link> |-->
        <router-link to="/groups">Moje klasy</router-link> |
        <a @click="doLogout">Wyloguj</a>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import {ROUTE_NAMES} from "@/router";
import router from '@/router';

export default {
    name: "TeacherNavbar.vue",
    methods: {
        ...mapActions(['logout']),
        async doLogout() {
          await this.logout();
          router.push({name: ROUTE_NAMES.MAIN});
        }
    },
    computed: {
        ...mapState(['user']),
    },

}
</script>

<style scoped>

</style>
