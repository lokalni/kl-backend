<template>
    <multiselect
            label="hostname"
            track-by="id"
            placeholder="Szukaj po domena, nazwa"
            open-direction="bottom"
            noOptions="Brak pasujących serwerów"
            selectLabel="Wybierz"
            :multiple="false"
            :searchable="true"
            :internal-search="false"
            :clear-on-select="true"
            :close-on-select="true"
            :options-limit="300"
            :limit="3"
            :max-height="600"
            :hide-selected="true"
            :options="matchingServers"
            :customLabel="server => `${server.display_name} @ ${server.hostname} (${server.region || 'no region'})`"
            @search-change="searchServers"
            @select="serverSelected"
    >
    </multiselect>
</template>

<script>
    import Multiselect from 'vue-multiselect'
    import {Servers} from '@/api';

    export default {
        name: "AddServerForm",
        props: {
            preloadFilter: {
                type: Object,
                default: () => {},
            }
        },
        data() {
            return {
                matchingServers: [],
            };
        },
        components: {
            Multiselect,
        },
        async beforeMount() {
            await this.preloadServers();
        },
        methods: {
            async preloadServers(){
                this.matchingServers = await Servers.list(this.preloadFilter);
                if (this.matchingServers.length === 0) {
                    this.matchingServers = await Servers.list();
                }
            },
            serverSelected(server) {
                this.$emit('submittedServer', server);
            },
            async searchServers(query) {
                this.matchingServers = await Servers.search(query);
            }
        }
    }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
