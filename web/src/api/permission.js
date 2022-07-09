import request from '@/utils/request'

export function fetchAccountList(query) {
  return request({
    url: '/api/account/list',
    method: 'get',
    params: query
  })
}

export function createAccount(data) {
  return request({
    url: '/api/account/create',
    method: 'post',
    data
  })
}

export function updateAccount(data) {
  return request({
    url: '/api/account/update',
    method: 'post',
    data
  })
}

export function deleteAccount(id) {
    return request({
        url: `/api/account/delete/${id}`,
        method: 'get',
    })
}

export function changeAccountStatus(condition) {
  return request({
    url: `/api/account/state`,
    method: 'put',
    params: condition
  })
}
