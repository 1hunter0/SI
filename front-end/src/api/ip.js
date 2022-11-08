import request from '@/utils/request'

export function getIPList(data) {
  return request({
    url: '/ips/infos',
    method: 'post',
    params: data
    // data
  })
}
