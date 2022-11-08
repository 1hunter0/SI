const Mock = require('mockjs')
const { start } = require('nprogress')

const data = Mock.mock({
  'items|30': [{
    ip: '@ip',
    country: '中国',
    province: '@province',
    city: '@city',
    'isp|1': ['中国电信', '中国移动', '中国联通'],
    'latitude|99-112.6': 102.620655,
    'longitude|26-33.6': 30.920677,
    // title: '@sentence(10, 20)',
    // 'status|1': ['published', 'draft', 'deleted'],
    // author: 'name',
    // display_time: '@datetime',
    // pageviews: '@integer(300, 5000)'
  }]
})

module.exports = [
  {
    url: '/ips/infos',
    type: 'post',

    response: config => {
      let {page, limit, query} = config.query
      page = page*1
      limit = limit * 1
      let startNumber = (page-1)*limit
      console.log(startNumber)
      let endNumber = (startNumber + limit > data.items.length) ? data.items.length : startNumber + limit
      console.log(endNumber)
      const items = data.items.slice(startNumber,endNumber)
      return {
        ErrCode: 20000,
        Data: {
          ips: items,
          count: data.items.length
        }
      }
    }
  },
  {

  }
]
