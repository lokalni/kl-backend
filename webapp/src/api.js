import axios from 'axios';
import Vue from 'vue'
import router from "@/router";
import {ROUTE_NAMES} from "@/router";

const TOAST_DURATION = 6000;
const BACKEND_URL = process.env.BACKEND_URL;



// Set withCredentials on $axios before creating instance
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
// axios.defaults.headers.post['Content-Type'] ='application/x-www-form-urlencoded';

// Create a custom axios instance
const api = axios.create({
    baseURL: `${BACKEND_URL}/api/v1`,
    responseType: 'json',
    timeout: 10000,
    // withCredentials: true,
    headers: {
      // 'X-Requested-With': 'XMLHttpRequest',
      'Content-Type': 'application/json'
    }
});


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
            window.console.log("EXC", e);
            const detail = (e.response.data || {}).detail || '';
            const respCode = e.response.status;

            if (respCode === 400) {
                Vue.toasted.show(`Wystąpił błąd! ${detail}`, {
                    duration: TOAST_DURATION,
                    type: 'error',
                });
            } else if (respCode === 403) {
                Vue.toasted.show(`Nie jesteś zalogowany. Użyj swojego linku.`, {
                    duration: TOAST_DURATION,
                    type: 'warn',
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
        return this._handler(api.post(`/${this.path}/`, params))
    }

    read(objId, params = {}) {
        return this._handler(api.get(`/${this.path}/${objId}`, {params}));
    }

    list(params = {}) {
        return this._handler(api.get(`/${this.path}/`, {params}));
    }

    update(objId, params = {}) {
        return this._handler(api.post(`/${this.path}/${objId}`, {params}));
    }

    delete(objId) {
        return this._handler(api.delete(`/${this.path}/${objId}/`));
    }
}


class GroupResource extends Resource {
    startLesson({id}) {
        return this._handler(api.post(`/${this.path}/${id}/start_lesson/`));
    }
}


class StudentResource extends Resource {
    resetAccess({id}) {
        return this._handler(api.post(`/${this.path}/${id}/reset_access/`));
    }

    buildJoinUrl(token) {
        return `${BACKEND_URL}/rooms/join/${token}`;
    }
}

class AccountsResource extends Resource {
    getSession() {
        return this._handler(api.get(`/${this.path}/get_session/`))
    }

    login({email, password}) {
        return this._handler(api.post(`/${this.path}/login/`, {email, password}));
    }

    logout() {
        return this._handler(api.post(`/${this.path}/logout/`));
    }
}


export const Groups = new GroupResource('groups');
export const Students = new StudentResource('students');
export const Accounts = new AccountsResource('accounts');
