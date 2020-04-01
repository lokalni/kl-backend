import axios from 'axios';

const BACKEND_URL = process.env.BACKEND_URL;


class Resource {
    constructor(resourcePath) {
        this.path = resourcePath;
    }

    async _handler(promise) {
        // Add generic 404, 500, 400 errors handling
        const resp = await promise;
        return resp.data;
    }

    create(params = {}) {
        return this._handler(axios.put(`${BACKEND_URL}/${this.path}/`, params))
    }

    read(objId, params = {}) {
        return this._handler(axios.get(`${BACKEND_URL}/${this.path}/${objId}`, params));
    }

    list(params = {}) {
        return this._handler(axios.get(`${BACKEND_URL}/${this.path}/`, params));
    }

    update(objId, params = {}) {
        return this._handler(axios.post(`${BACKEND_URL}/${this.path}/${objId}`, params));
    }

    delete(objId) {
        return this._handler(axios.delete(`${BACKEND_URL}/${this.path}/${objId}`));
    }
}



export const Groups = new Resource('groups');
export const Students = new Resource('students');
