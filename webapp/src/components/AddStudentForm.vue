<template>
    <form @submit="studentSubmitted">
      <div class="form-row">
        <div class="col-4">
          <input v-model="name" type="text" class="form-control" placeholder="Imie, nazwisko">
        </div>
        <div class="col-auto">
          <button type="submit" class="btn btn-primary mb-2"
                  :disabled="!formValid"
          >Dodaj</button>
        </div>
      </div>
    </form>
</template>

<script>
export default {
    name: "AddStudentForm",
    data() {
        return {
          name: '',
        };
    },
    computed: {
      formValid() {
          return this.name;
      }
    },
    methods: {
        studentSubmitted() {
            const student = {name: this.name};
            this.$emit('submittedStudent', student);
            this.name = '';
            console.log("Student Submitted", student);
        }
    }
}
</script>

<style scoped>

</style>