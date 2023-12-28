import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/token/',
    method: 'post',
    data
  })
}
export function getPubKey() {
  return request({
    url: '/getPubKey/',
    method: 'get'
  })
}
export function getInfo(token) {
  return request({
    url: '/user/info/',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
