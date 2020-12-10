<template>
  <multiselect
     placeholder="Wybierz Region"
     open-direction="bottom"
     selectLabel="Wybierz"
     :multiple="false"
     :searchable="true"
     :internal-search="true"
     :clear-on-select="false"
     :close-on-select="true"
     :options-limit="300"
     :limit="3"
     :max-height="600"
     :hide-selected="true"
     :options="regionOptions"
     :value="value"
     @select="val => $emit('input', val)"
    />
</template>

<script>
import Multiselect from 'vue-multiselect'
import {REGIONS} from "../../constants";

export default {
    name: "SelectRegionDropdown",
    props: {
        value: {
            type: String,
        },
    },
    components: {
        Multiselect,
    },
    computed: {
        regionOptions() {
            return Object.values(REGIONS);
        }
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
