import axios from 'axios';
import Vue from 'vue'

const TOAST_DURATION = 6000;
const BACKEND_URL = process.env.BACKEND_URL;


class Resource {
    constructor(resourcePath) {
        this.path = resourcePath;
    }

    async _handler(promise) {
        // Add generic 404, 500, 400 errors handling
        try {
            const resp = await promise;
            return resp.data;
        } catch (e) {
            window.console.log(e);
            const detail = (e.response.data || {}).detail || '';
            const respCode = e.response.status;

            if (respCode === 400) {
                Vue.toasted.show(`Wystąpił błąd! ${detail}`, {
                    duration: TOAST_DURATION,
                    type: 'error',
                });
            } else if (respCode === 500) {
                Vue.toasted.show(`Nieznany błąd!`, {
                    duration: TOAST_DURATION,
                    type: 'error',
                });  
            }
            throw e;
        }

    }

    create(params = {}) {
        return this._handler(axios.post(`${BACKEND_URL}/${this.path}/`, params))
    }

    read(objId, params = {}) {
        return this._handler(axios.get(`${BACKEND_URL}/${this.path}/${objId}`, {params}));
    }

    list(params = {}) {
        return this._handler(axios.get(`${BACKEND_URL}/${this.path}/`, {params}));
    }

    update(objId, params = {}) {
        return this._handler(axios.post(`${BACKEND_URL}/${this.path}/${objId}`, {params}));
    }

    delete(objId) {
        return this._handler(axios.delete(`${BACKEND_URL}/${this.path}/${objId}/`));
    }
}


class GroupResource extends Resource {
    startLesson({id}) {
        return this._handler(axios.post(`${BACKEND_URL}/${this.path}/${id}/start_lesson/`));
    }
}


class StudentResource extends Resource {
    resetAccess({id}) {
        return this._handler(axios.post(`${BACKEND_URL}/${this.path}/${id}/reset_access/`));
    }

    buildJoinUrl(token) {
        return `${BACKEND_URL}/rooms/join/${token}`;
    }
}


export const Groups = new GroupResource('groups');
export const Students = new StudentResource('students');
