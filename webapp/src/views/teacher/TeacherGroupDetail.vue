<template>
  <div class="container">
    <Navbar/>
    <div class="row">
      <div class="col">
        <div class="btn-group float-left" role="group">
            <button type="button" class="btn btn-primary"
                    @click="startAndJoin">
              Rozpocznij lekcję
            </button>
        </div>
      </div>
    </div>
    <!-- Students list -->
    <div class="card my-3">
      <div class="card-body">
        <h3 class="card-title">
          Lista uczniów w klasie {{group.display_name}}
        </h3>
        </div>
        <p class="card-text mx-3">
            Każdy z uczniów zadeklarowanych w klasie posiada <u>indywidualny link</u>
            którego używa aby dołączyć do lekcji.
        </p>
        <p class="card-text mx-3">
            Przycisk <b>Resetuj Dostęp</b>
            generuje link od nowa w przypadku gdy uczeń go zgubi, bądź podzieli się nim z niepożądanymi osobami.
            Aby rozpocząć lekcje uczniowie muszą najpierw otrzymać poniższe linki
        </p>
        <div class="col-md-6">
          <AddStudentForm @submittedStudent="onSubmittedStudent"/>
        </div>
        <StudentList
            :students="students"
            @updatedStudent="onUpdatedStudent"
        />
    </div>
    <!-- Settings -->
    <div class="card my-3">
      <div class="card-body">
        <h3 class="card-title">
          Ustawienia
        </h3>
        </div>
        <div>Serwery preferowane</div>
    </div>

  </div>
</template>

<script>
import {Students, Groups} from '@/api';
import StudentList from '@/components/StudentList.vue';
import Navbar from '@/components/Navbar.vue';
import AddStudentForm from "../../components/AddStudentForm";

export default {
  name: 'app',
  components: {
    AddStudentForm,
    Navbar,
    StudentList,
  },
  data() {
    // TODO - move to vuex, maybe at API call level
    return {
      group: {},
      students: [],
    };
  },
  computed: {
    groupId() {
      return this.$route.params.id;
    }
  },
  async beforeMount() {
    await Promise.all([this.loadStudents(), this.loadGroup()]);
  },
  methods: {
    async loadGroup() {
      this.group = await Groups.read(this.groupId);
    },
    async startAndJoin() {
      const {redirect} = await Groups.startLesson({id: this.groupId});
      window.console.log("Received redirect url CHECK_DEPLOYMENT_CACHE", redirect);
      window.location = redirect;
    },
    async loadStudents() {
      this.students = await Students.list({group: this.groupId});
      window.console.log("Students Fetched", this.groups);
    },

    async onUpdatedStudent() {
      await this.loadStudents();
      this.$toasted.show('Sukces!', {duration: 3000, type: 'success'});

    },

    async onSubmittedStudent(student) {
      await Students.create({
        display_name: student.name,
        group: this.groupId
      });
      await this.loadStudents();
      this.$toasted.show('Dodano!', {duration: 3000, type: 'success'});
    },
  }
};
</script>
