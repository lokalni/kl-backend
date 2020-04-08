<template>
    <form @submit="moderatorSubmitted">
      <div class="form-group">
        <input v-model="display_name" type="name" class="form-control" placeholder="Unikalny identyfikator">
      </div>
      <div class="form-group">
        <input v-model= "email" type="email" class="form-control" placeholder="Adres email">
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
            this.display_name = this.email = '';
            console.log("moderatorSubmitted Submitted", moderator);
        }
    }
}
</script>

<style scoped>

</style>
