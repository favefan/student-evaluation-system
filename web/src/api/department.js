import request from '@/utils/request'

export function fetchDepartmentList(query) {
  return request({
    url: '/api/department/list',
    method: 'get',
    params: query
  })
}

export function createDepartment(data) {
  return request({
    url: '/api/department/create',
    method: 'post',
    data
  })
}

export function updateDepartment(data) {
  return request({
    url: '/api/department/update',
    method: 'post',
    data
  })
}

export function deleteDepartment(id) {
    return request({
        url: `/api/department/delete/${id}`,
        method: 'get',
    })
}

export function changeDepartmentStatus(condition) {
  return request({
    url: `/api/department/change_status`,
    method: 'get',
    params: condition
  })
}
