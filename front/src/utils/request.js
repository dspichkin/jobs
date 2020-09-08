import axios from 'axios'
import { Message } from 'element-ui'
import { getToken } from '@/utils/auth'
import store from '../store'

let SERVER_URL = ''
if (process.env.VUE_APP_SERVER_URL) {
  SERVER_URL = process.env.VUE_APP_SERVER_URL
}
if (process.env.BASE_API) {
  SERVER_URL += process.env.BASE_API
}
const service = axios.create({
  baseURL: SERVER_URL, // api  base_url
  timeout: 5000
})

service.interceptors.request.use(
  (config) => {
    if (store.getters.token) {
    //   // config.headers['X-Token'] = getToken();
      config.headers.Authorization = `JWT ${getToken()}`
      config.headers['Content-Type'] = 'application/json'
    }
    return config
  },
  (error) => {
    // Do something with request error
    // console.log(error) // for debug
    Promise.reject(error)
  }
)

// response
service.interceptors.response.use(
  (response) => {
    /**
     * code
     */
    const res = response.data
    if (response.status === 200) {
      if (res.Error) {
        Message({
          message: res.Error,
          type: 'error',
          duration: 5 * 1000
        })
        return Promise.reject(new Error('something bad happened'))
      }

      /*
      if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
        MessageBox.confirm(
          '你已被登出，可以取消继续留在该页面，或者重新登录',
          '确定登出',
          {
            confirmButtonText: '重新登录',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          store.dispatch('FedLogOut').then(() => {
            location.reload()
          })
        })
      }

      */
    }

    return response.data
  },
  (error) => {
    console.log('status', error)
    console.log('err', error.data) // for debug
    Message({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
