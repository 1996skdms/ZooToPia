/* eslint-disable */
import axios from 'axios'
const _axios = axios.create({
    baseURL: "http://localhost:8080/api",
    timeout: 100000,
})

export default _axios;