<template>
  <div class="home">
    <TeacherNavbar/>
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld v-if='user' msg="Welcome to Your Vue.js App"/>
    <Login v-else/>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapState } from 'vuex';
import HelloWorld from '@/components/HelloWorld.vue';
import TeacherNavbar from '@/components/TeacherNavbar.vue';
import Login from '@/components/Login.vue';

export default {
  name: 'Home',
  components: {
    Login,
    TeacherNavbar,
    HelloWorld
  },
  computed: {
    ...mapState(['user'])
  }
}
</script>
