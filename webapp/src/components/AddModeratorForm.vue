<template>
    <form @submit="moderatorSubmitted">
      <div class="form-group">
        <label for="exampleInputEmail1">Podaj unikalny identyfikator dla konferencji.</label>
        <input v-model="display_name" type="name" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Unikalny identyfikator.">
        <small id="emailHelp" class="form-text text-muted">Podaj unikalny identyfikator.</small>
      </div>
      <div class="form-group">
        <label for="exampleInputName1">Email</label>
        <input v-model= "email" type="email" class="form-control" id="exampleInputName1" placeholder="Adres email">
      </div>
      <button :disabled="!formValid" type="submit" class="btn btn-primary">Dodaj</button>
    </form>
</template>

<script>
export default {
    name: "AddModeratorForm",
    data() {
        return {
          display_name: '',
          email: '',
        };
    },
    computed: {
      formValid() {
          return this.display_name && this.email;
      }
    },
    methods: {
        moderatorSubmitted() {
            const moderator = {
                display_name: this.display_name,
                email: this.email,
            };
            this.$emit('moderatorSubmitted', moderator);
            this.name = '';
            console.log("moderatorSubmitted Submitted", moderator);
        }
    }
}
</script>

<style scoped>

</style>
