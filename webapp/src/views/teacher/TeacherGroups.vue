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
        <AddGroupForm @submittedGroup="onSubmittedGroup"/>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <GroupList :groups="groups"
                   @groupClicked="openGroupView"
                   @deleteGroup="onDeleteGroup"
        />
      </div>
    </div>
  </div>
</template>

<script>
  import {Groups} from '@/api';
  import GroupList from '@/components/GroupList.vue';
  import {ROUTE_NAMES} from "../../router";
  import TeacherNavbar from '@/components/TeacherNavbar.vue';
  import AddGroupForm from "../../components/AddGroupForm";

  export default {
    name: 'app',
    components: {
      AddGroupForm,
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
      async loadGroups() {
        this.groups = await Groups.list();
      },
      openGroupView(group) {
        this.$router.push({
          name: ROUTE_NAMES.TEACHER_GROUP_DETAIL,
          params: { id: group.id }
        });
      },
      async onSubmittedGroup(group) {
        await Groups.create({
          display_name: group.name,
          region: group.region,
        });
        await this.loadGroups();
        this.$toasted.show('Dodano!', {duration: 3000, type: 'success'});
      },
      async onDeleteGroup(group) {
        if (group.students_count > 0) {
          this.$toasted.show('Nie można usunąc grupy zawierającej studentów', {duration: 3000, type: 'error'});
          return;
        }
        await Groups.delete(group.id);
        await this.loadGroups();
        this.$toasted.show('Suckes', {duration: 3000, type: 'success'});
      }
    }
  };
</script>
