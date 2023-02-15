import request from '@/utils/request'



export function getVirusInfo(sha1) {
  return request({
    url: 'files/info',
    method: 'get',
    params: {sha1: sha1}
  })
}

export function getNetGraph(sha1) {
  return request({
    url: 'files/getnetgraph',
    method: 'get',
    params: {sha: sha1}
  })
}