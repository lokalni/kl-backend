<template>
    <div v-if="user" id="nav">
<!--        <router-link to="/">Informacje</router-link> |-->
        <template>
            <router-link :to="{name: ROUTE_NAMES.TEACHER_GROUPS}">Moje klasy</router-link> |
        </template>
        <template v-if="user.is_staff">
            <router-link :to="{name: ROUTE_NAMES.ADMIN_MODERATORS}">Moderatorzy</router-link> |
        </template>
        <a @click="doLogout">Wyloguj</a>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import {ROUTE_NAMES} from "@/router";
import router from '@/router';

export default {
    name: "Navbar",
    methods: {
        ...mapActions(['logout']),
        async doLogout() {
          await this.logout();
          router.push({name: ROUTE_NAMES.MAIN});
        }
    },
    computed: {
        ...mapState(['user']),
        ROUTE_NAMES: () => ROUTE_NAMES,
    },

}
</script>

<style scoped>

</style>
