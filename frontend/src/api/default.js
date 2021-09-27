import axios from 'axios'

const _axios = axios.create({
    baseURL: "http://localhost:8081",
    timeout: 30000,
})

export default _axios;