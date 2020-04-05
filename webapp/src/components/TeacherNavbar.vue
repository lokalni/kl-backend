<template>
    <div v-if="user" id="nav">
<!--        <router-link to="/">Informacje</router-link> |-->
        <router-link to="/groups">Grupy</router-link> |
        <a @click="logout">Wyloguj</a>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';

export default {
    name: "TeacherNavbar.vue",
    methods: {
        ...mapActions(['logout']),
    },
    computed: {
        ...mapState(['user']),
    }
}
</script>

<style scoped>

</style>