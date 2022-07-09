import request from '@/utils/request'

export function fetchPersonnelList(query) {
  return request({
    url: '/api/personnel/list',
    method: 'get',
    params: query
  })
}

export function createPersonnel(data) {
  return request({
    url: '/api/personnel/create',
    method: 'post',
    data
  })
}

export function updatePersonnel(data) {
  return request({
    url: '/api/personnel/update',
    method: 'post',
    data
  })
}

export function deletePersonnel(id) {
    return request({
        url: `/api/personnel/delete/${id}`,
        method: 'get',
    })
}

export function changePersonnelStatus(condition) {
  return request({
    url: `/api/personnel/state`,
    method: 'put',
    params: condition
  })
}

export function uploadExcel(data) {
  return request({
    url: '/api/personnel/upload',
    method: 'post',
    data
  })
}

export function uploadExcelContent(data, is_student) {
  return request({
    url: `/api/personnel/upload_content/${is_student}`,
    method: 'post',
    data
  })
}
