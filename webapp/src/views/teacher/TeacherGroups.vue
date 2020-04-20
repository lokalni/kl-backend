<template>
  <div class="container">
    <Navbar/>
    <div class="row">
      <div class="col-md-12 my-3">
        <h2>Lista twoich klas</h2>
        <h5>Tutaj możesz dodać swoje klasy, a następnie dodać uczniów do klasy klikając w <u>nazwę klasy</u>. Po zadeklarowaniu uczniów i rozesłaniu do nich linków dostępowych możesz rozpocząć lekcję.</h5>
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
  import { mapState } from 'vuex';
  import {ROUTE_NAMES} from "@/router";
  import {Groups} from '@/api';
  import GroupList from '@/components/GroupList.vue';
  import Navbar from '@/components/Navbar.vue';
  import AddGroupForm from "@/components/AddGroupForm";

  export default {
    name: 'app',
    components: {
      AddGroupForm,
      GroupList,
      Navbar,
    },
    data() {
      // TODO - move to vuex, maybe at API call level
      return {
        groups: [],
      };
    },
    computed: {
      ...mapState(['user']),
    },
    async mounted() {
      await this.loadGroups();
    },
    methods: {
      async loadGroups() {
        const groups = await Groups.list();
        const baseUrl = this.user.moderator.access_url;
        this.groups = groups.map(g => ({
          ...g,
          quick_access_url: `${baseUrl}?g=${g.slug}`,
        }));
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
