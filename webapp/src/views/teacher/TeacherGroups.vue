<template>
  <div class="container">
    <TeacherNavbar/>
    <div class="row">
      <div class="col-md-12 my-3">
        <h2>Twoje Grupy</h2>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <GroupList :groups="groups" @groupClicked="openGroupView"/>
      </div>
    </div>
  </div>
</template>

<script>
  import {Groups} from '@/api';
  import GroupList from '@/components/GroupList.vue';
  import {ROUTE_NAMES} from "../../router";
  import TeacherNavbar from '@/components/TeacherNavbar.vue';

  export default {
    name: 'app',
    components: {
      GroupList,
      TeacherNavbar,
    },
    data() {
      // TODO - move to vuex, maybe at API call level
      return {
        groups: [],
      };
    },
    computed: {
    },
    async mounted() {
      this.groups = await Groups.list();
    },
    methods: {
      openGroupView(group) {
        this.$router.push({
          name: ROUTE_NAMES.TEACHER_GROUP_DETAIL,
          params: { id: group.id }
        });
      }
    }
  };
</script>
