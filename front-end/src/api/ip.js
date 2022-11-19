import request from '@/utils/request'

export function getIPList(data) {
  return request({
    url: '/ips/query',
    method: 'get',
    params: data
    // data
  })
}

export function getIpInfo(ip) {
  return request({
    url: 'ips/info',
    method: 'get',
    params: {ip: ip}
  })
}
