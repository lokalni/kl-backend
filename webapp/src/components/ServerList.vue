<template>
    <table class="table table-striped table-hover">
        <thead>
        <tr>
            <th scope="col">Domena</th>
            <th scope="col">Region</th>
            <th scope="col">Aktywny</th>
            <th scope="col">Aktualizacja</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(server, idx) in servers"
            :key="server.id"
        >
            <td>{{server.hostname}}</td>
            <td>{{server.region}}</td>
            <td>
                <span v-if="server.enabled" class="fas fa-check-circle text-success"></span>
                <span v-else class="fa fa-times-circle text-warning"></span>
            </td>
            <td>
                {{ fmtTimestamp(server.last_heartbeat) }}
            </td>
            <td>
                <button v-if="idx > 0"
                        type="button"
                        class="btn btn-primary ml-1"
                        @click="() => changeServerPriority(idx, -1)"
                >
                    <span class="fas fa-chevron-circle-up"/>
                </button>
                <button v-if="idx < servers.length-1"
                        type="button"
                        class="btn btn-primary ml-1"
                        @click="() => changeServerPriority(idx, +1)"
                >
                    <span class="fas fa-chevron-circle-down"/>
                </button>
                <button type="button" class="btn btn-danger ml-1"
                        @click="() => removeServer(server)"
                >Usuń
                </button>
            </td>
        </tr>
        </tbody>
    </table>
</template>

<script>
    import {fmtTimestamp} from "../utils";

    export default {
        name: "GroupList",
        props: {
            servers: {
                type: Array
            },
        },
        methods: {
            fmtTimestamp: fmtTimestamp,
            removeServer(server) {
                this.$emit('serversChanged', this.servers.filter(s => s.id !== server.id));
            },
            changeServerPriority(serverIdx, change) {
                this.$emit('serversChanged', this.servers.map((s, idx) => {
                    if (idx === serverIdx) return this.servers[serverIdx + change];
                    else if (idx === serverIdx + change) return this.servers[serverIdx];
                    else return s;
                }));
            }
        }
    }
</script>

<style scoped>

</style>
