<template>
    <div>
        <div class="row">
          <div class="col-md-12 my-3">
              <h2>Twoje lekcje jeszcze się nie rozpoczęły</h2>
              <h4>Zostań na tej stronie i poczekaj na nauczyciela - nie musisz jej odświeżać.</h4>
              <small>Jeśli jednak wiesz, że lekcje rozpoczęły się a nadal widzisz ten komunikat to poproś nauczyciela o nowy link.</small>
          </div>
        </div>
    </div>
</template>

<script>
import {Students} from "@/api";

export default {
    name: 'app',
    async mounted() {
        setTimeout(this.attemptJoin, 10000);
    },
    methods: {
      attemptJoin() {
          window.location = Students.buildJoinUrl(this.$route.query.token);
      }
    }
};
</script>
