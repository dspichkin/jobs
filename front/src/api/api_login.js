import request from '@/utils/request'

export function login (username, password) {
  return request({
    // url: '/api/user/login',
    url: '/api/auth-jwt',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

export function getInfo () {
  return request({
    url: '/api/user/info',
    method: 'get'
    // params: { token }
  })
}

export function logout () {
  return request({
    url: '/api/user/logout',
    method: 'post'
  })
}
