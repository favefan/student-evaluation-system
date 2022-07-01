import request from '@/utils/request'

export function getRoutes() {
  return request({
    url: '/api/routes',
    method: 'get'
  })
}

export function getRoles() {
  return request({
    url: '/api/role/list',
    method: 'get'
  })
}

export function addRole(data) {
  return request({
    url: '/api/role',
    method: 'post',
    data
  })
}

export function updateRole(id, data) {
  return request({
    url: `/api/role/${id}`,
    method: 'post',
    data
  })
}

export function deleteRole(id) {
  return request({
    url: `/api/role/${id}`,
    method: 'get'
  })
}
