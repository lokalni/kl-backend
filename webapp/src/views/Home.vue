<template>
  <div class="home">
    <TeacherNavbar/>
    <img alt="Vue logo" src="../assets/logo.png">
    <InfoMain v-if='user' msg="Witaj w Teleklasie"/>
    <Login v-else/>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapState } from 'vuex';
import InfoMain from '@/components/InfoMain.vue';
import TeacherNavbar from '@/components/TeacherNavbar.vue';
import Login from '@/components/Login.vue';

export default {
  name: 'Home',
  components: {
    Login,
    TeacherNavbar,
    InfoMain
  },
  computed: {
    ...mapState(['user'])
  }
}
</script>
