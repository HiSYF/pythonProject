import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/articles/',
    method: 'get',
    params
  })
}
export function getLmt(params) {
  return request({
    url: '/lmt/',
    method: 'get',
    params
  })
}
export function putLmt(id, updatedData) {
  return request({
    url: `/lmt/${id}`, // 根据后端接口的实际路径进行修改
    method: 'put',
    data: updatedData // 传入要更新的数据
  })
}
export function delLmt(params) {
  return request({
    url: '/lmt/',
    method: 'del',
    params
  })
}
