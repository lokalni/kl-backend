<template>
  <div class="home">
    <TeacherNavbar/>
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import TeacherNavbar from '@/components/TeacherNavbar.vue'

export default {
  name: 'Home',
  components: {
    TeacherNavbar,
    HelloWorld
  }
}
</script>
