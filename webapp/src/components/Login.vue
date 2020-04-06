<template>
    <div class="container">
        <h1>Logowanie</h1>
        <form @submit="loginAndRedirect">
          <div class="form-group">
            <label for="exampleInputEmail1">Email</label>
            <input v-model='email'
                   type="email"
                   class="form-control"
                   id="exampleInputEmail1"
                   aria-describedby="emailHelp"
                   placeholder="Adres email">
    <!--        <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>-->
          </div>
          <div class="form-group">
            <label for="exampleInputPassword1">Hasło</label>
            <input v-model='password'
                   type="password"
                   class="form-control"
                   id="exampleInputPassword1"
                   placeholder="Hasło">
          </div>
          <button type="submit" class="btn btn-primary">Zaloguj się</button>
        </form>
    </div>
</template>

<script>
import { mapActions } from 'vuex';
import { ROUTE_NAMES } from "@/router";

export default {
    name: "Login.vue",
    data() {
        return {
            email: '',
            password: '',
        };
    },
    methods: {
        ...mapActions(['login']),
        async loginAndRedirect() {
            try {
                await this.login({email: this.email, password: this.password});
                this.$router.push({
                  name: ROUTE_NAMES.TEACHER_GROUPS,
                });
            } catch (e) {
                window.console.log(e);
                this.$toasted.show('Niepoprawny login lub hasło.', {duration: 3000, type: 'error'});
            }
        },
    }
}
</script>

<style scoped>

</style>
