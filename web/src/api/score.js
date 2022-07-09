import request from '@/utils/request'

export function fetchScoreList(query) {
  return request({
    url: '/api/score/list',
    method: 'get',
    params: query
  })
}

export function createScore(data) {
  return request({
    url: '/api/score/create',
    method: 'post',
    data
  })
}

export function updateScore(data) {
  return request({
    url: '/api/score/update',
    method: 'post',
    data
  })
}

export function deleteScore(id) {
    return request({
        url: `/api/score/delete/${id}`,
        method: 'get',
    })
}

export function changeScoreStatus(condition) {
  return request({
    url: `/api/score/state`,
    method: 'put',
    params: condition
  })
}


export function uploadExcelContent(data) {
  return request({
    url: '/api/score/import',
    method: 'post',
    data
  })
}
