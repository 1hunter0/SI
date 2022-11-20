<template>
<div class="app-container">
    <el-tabs v-model="tabs.activeName" type="card" @tab-remove="removeTab">
      <el-tab-pane label="IP列表" name="ipListPage" >
        <div class="filter-container">
          <el-input v-model.trim="page.temp_query" placeholder="根据ip查询" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
          <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-search" @click="handleFilter">
            查询
          </el-button>
        </div>

        <el-table
            v-loading="listLoading"
            :data="dataList"
            element-loading-text="Loading"
            border
            fit
            height="720"
            highlight-current-row
        >
          <el-table-column align="center" label="序号" type="index" width="60" :index="indexMethod" />
          <el-table-column label="IP" align="center">
            <template slot-scope="scope">
              {{ scope.row.ip }}
            </template>
          </el-table-column>
          <el-table-column label="国家" align="center">
            <template slot-scope="scope">
              {{ scope.row.country | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column label="省份" align="center">
            <template slot-scope="scope">
              {{scope.row.province | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column label="城市" align="center">
            <template slot-scope="scope">
              {{ scope.row.city | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column label="运营商" align="center">
            <template slot-scope="scope">
              {{ scope.row.isp | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="地理位置(经度 纬度)">
            <template slot-scope="scope">
              {{ scope.row.longitude | nullAndOtherFilter }}<br/>
              {{ scope.row.latitude | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click="detailClick(scope.row.ip)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination v-show="page.total>0" :total="page.total" :current-page="page.page" :page-size="page.limit" @current-change="fetchData" />
      </el-tab-pane>
      <el-tab-pane
        v-for="item in tabs.detailTabs"
        :key="item.name"
        :label="item.title"
        :name="item.name"
        closable
        :id="item.name"
        class="my-main-container"
      >
        <el-container class="top-container">
          <el-aside width="300px" class="logo">
            <img :src="item.content.IpInfo.ip | logoFilter" class="logo-content">
            <div class="logo-footer">
              <div class="risk">
                <div class="title">风险评估</div>
                <div :class="item.content.IpInfo.ip | levelClassFilter">{{item.content.IpInfo.ip | levelFilter}}</div>
              </div>
              <div class="degree">
                <div class="title">置信度</div>
                <div class="value" style="color: #2b2c2d">{{item.content.IpInfo.ip | confidenceFilter}}</div>
              </div>
            </div>
          </el-aside>
          <el-container direction="vertical">
            <el-main class="my-general-main">
              <div class="name-tag">
                <div class="name">
                  <div class="title">IP</div>
                  <span class="content">
                    {{item.content.IpInfo.ip}}
                  </span>
                  <el-tooltip effect="dark" content="复制" placement="top"><i class="el-icon-copy-document copy" v-clipboard:copy="item.name" v-clipboard:success="onCopySuccess" v-clipboard:error="onCopyError"></i></el-tooltip>
                </div>
                <div class="tag">
                  <span class="title">情报来源</span>
                  <el-tooltip effect="dark" content="该实体情报的来源，可能是外生情报，也可能是从企业内部历史日志中搜集来" placement="top"><span class="my-icon"><i class="el-icon-zoom-in tag-tip"></i></span></el-tooltip>
                  <div class="content">
                    <el-tag v-for="(origin, index1) in tagFilter(item.content.IpInfo.ip)" :type="origin | tagClassFilter" :key="index1" effect="plain" size="mini">{{origin}}</el-tag>
                  </div>
                </div>
              </div>
            </el-main>
            <el-main class="my-general-footer">
              <div class="item-wrap">
                <svg-icon icon-class="earth" />
                <span class="label-wrap">地理位置</span>
                <div class="value-wrap">{{item.content.IpInfo.country}}-{{item.content.IpInfo.province}}-{{item.content.IpInfo.city}}</div>
              </div>
              <div class="item-wrap">
                <i class="el-icon-map-location"></i>
                <span class="label-wrap">经纬度</span>
                <div class="value-wrap">{{item.content.IpInfo.longitude}}-{{item.content.IpInfo.latitude}}</div>
              </div>
              <div class="item-wrap">
                <svg-icon icon-class="sponer" />
                <span class="label-wrap">运营商</span>
                <div class="value-wrap">{{item.content.IpInfo.isp}}</div>
              </div>
            </el-main>
          </el-container>
        </el-container>
        <el-container class="bottom-container">
            <el-main>
              <el-tabs v-model="item.activeName" type="card">
                <el-tab-pane name="first">
                  <span slot="label">
                    <el-tooltip effect="dark" content="该ip作为主动方的所有告警日志" placement="top"><span>主动告警事件</span></el-tooltip>
                  </span>
                  <el-table
                    :data="item.firstPage.dataList"
                    fit
                    border
                    height="350"
                    highlight-current-row
                  >
                    <el-table-column label="ip_subject" align="center" width="120" fixed>
                      <template slot-scope="scope">
                        {{ scope.row.ip_subject }}
                      </template>
                    </el-table-column>
                    <el-table-column label="ip_object" align="center" width="120">
                      <template slot-scope="scope">
                        {{ scope.row.ip_object }}
                      </template>
                    </el-table-column>
                    <el-table-column label="dev_info" align="center" width="150">
                      <template slot-scope="scope">
                        {{ scope.row.dev_info }}
                      </template>
                    </el-table-column>
                    <el-table-column label="timestamp" align="center" width="180">
                      <template slot-scope="scope">
                        <i class="el-icon-time"></i>
                        {{ scope.row.timestamp }}
                      </template>
                    </el-table-column>
                    <el-table-column label="dev_category" align="center" width="150">
                      <template slot-scope="scope">
                        {{ scope.row.dev_category }}
                      </template>
                    </el-table-column>
                    <el-table-column label="dev_rule" align="center" width="300">
                      <template slot-scope="scope">
                        {{ scope.row.dev_rule }}
                      </template>
                    </el-table-column>
                    <el-table-column label="degree" align="center" width="80">
                      <template slot-scope="scope">
                        <el-tag :type="scope.row.degree | degreeClassFilter">{{ scope.row.degree}}</el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column label="hostname" align="center" width="150">
                      <template slot-scope="scope">
                        {{ scope.row.hostname }}
                      </template>
                    </el-table-column>
                  </el-table>
                  <el-pagination v-show="item.firstPage.total>0" :total="item.firstPage.total" :current-page="item.firstPage.page" :page-size="item.firstPage.limit" @current-change="fetchFirstData($event, item)" />

                </el-tab-pane>
                <el-tab-pane name="second">
                  <span slot="label">
                    <el-tooltip effect="dark" content="该ip作为被动方的所有告警日志" placement="top"><span>被动告警事件</span></el-tooltip>
                  </span>
                  <el-table
                    :data="item.secondPage.dataList"
                    fit
                    border
                    height="350"
                    highlight-current-row
                  >
                    <el-table-column label="ip_object" align="center" width="120" fixed>
                      <template slot-scope="scope">
                        {{ scope.row.ip_object }}
                      </template>
                    </el-table-column>
                    <el-table-column label="ip_subject" align="center" width="120">
                      <template slot-scope="scope">
                        {{ scope.row.ip_subject }}
                      </template>
                    </el-table-column>
                    <el-table-column label="dev_info" align="center" width="150">
                      <template slot-scope="scope">
                        {{ scope.row.dev_info }}
                      </template>
                    </el-table-column>
                    <el-table-column label="timestamp" align="center" width="180">
                      <template slot-scope="scope">
                        <i class="el-icon-time"></i>
                        {{ scope.row.timestamp }}
                      </template>
                    </el-table-column>
                    <el-table-column label="dev_category" align="center" width="150">
                      <template slot-scope="scope">
                        {{ scope.row.dev_category }}
                      </template>
                    </el-table-column>
                    <el-table-column label="dev_rule" align="center" width="300">
                      <template slot-scope="scope">
                        {{ scope.row.dev_rule }}
                      </template>
                    </el-table-column>
                    <el-table-column label="degree" align="center" width="80">
                      <template slot-scope="scope">
                        <el-tag :type="scope.row.degree | degreeClassFilter">{{ scope.row.degree}}</el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column label="hostname" align="center" width="150">
                      <template slot-scope="scope">
                        {{ scope.row.hostname }}
                      </template>
                    </el-table-column>
                  </el-table>
                  <el-pagination v-show="item.secondPage.total>0" :total="item.secondPage.total" :current-page="item.secondPage.page" :page-size="item.secondPage.limit" @current-change="fetchSecondData($event, item)" />
                </el-tab-pane>
                <el-tab-pane name="third">
                  <span slot="label">
                    <el-tooltip effect="dark" content="与此ip有关的所有样本" placement="top"><span>关联样本</span></el-tooltip>
                  </span>
                  与此ip有关的所有样本
                </el-tab-pane>
                <el-tab-pane name="forth">
                  <span slot="label">
                    <el-tooltip effect="dark" content="该ip的关联图" placement="top"><span>Graph</span></el-tooltip>
                  </span>
                  该ip的关联图
                </el-tab-pane>
              </el-tabs>
            </el-main>
        </el-container>
        <!-- {{item.content}} -->
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import {getIPList, getIpInfo} from '@/api/ip'
export default {
  name: 'IP',
  data() {
    return {
      listLoading: false,
      dataList: null,
      buttonLoading: false,
      page: {
        page: 1,  // 默认是第一页
        limit: 10,  // 每一页多少条记录
        total: 0,  // 总共有多少条记录
        param: {ip: ''},  // 可以根据ip地址模糊查询
        temp_query: '', // 临时变量,否则点击跳转页面会根据当前搜索框内容查询，出现bug
      },
      tabs: { // 标签页数据
        activeName: 'ipListPage',
        detailTabs: [],
      }
    }
  },
  filters: {
    nullAndOtherFilter(oldVal) {
      if (!oldVal) {
        return null
      }else if(oldVal == 'other') {
        return null
      }
      return oldVal
    },
    logoFilter(ip) {
      let level = ip.length % 2 // 0: 安全 1：危险
      const levelToLogo = {
        0: "https://ti.360.cn/img/white.03d4f02d.svg", // todo(tanrenxuan): replace with our picture
        1: "https://ti.360.cn/img/black.12b150fa.svg",
      }
      return levelToLogo[level]
    },
    levelFilter(ip) { // todo(tanrenxuan): replace with our field
      let level = ip.length % 2 // 0: 安全 1：危险
      const levelToDescription = {
        0: "安全",
        1: "危险",
      }
      return levelToDescription[level]
    },
    levelClassFilter(ip) { // todo(tanrenxuan): replace with our field
      let level = ip.length % 2 // 0: 安全 1：危险
      const levelToClass = {
        0: "safe",
        1: "danger"
      }
      return [levelToClass[level],'value']
    },
    confidenceFilter(ip) { // todo(tanrenxuan): replace with our field
      let confidence = ip.length % 3 // 0: 低 1:中 2:高
      const confidenceToDescription = {
        0: "低",
        1: "中",
        2: "高"
      }
      return confidenceToDescription[confidence]
    },
    tagClassFilter(origin) { // todo(tanrenxuan): replace with our field
      const originToTag = {
        '蜜罐': 'info',
        '日志易-waf': 'info',
        '日志易-云澈': '',
        '外生': 'success',
      }
      return originToTag[origin]
    },
    degreeClassFilter(degree) {
      const degreeToClass = {
        'low': "success",
        'middle': "warning",
        'high': "danger",
      }
      return degreeToClass[degree]
    },
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData(val) {
      if (val != null && val !== '') {
        this.page.page = val
      }
      this.listLoading = true
      getIPList({curr_page: this.page.page, page_size: this.page.limit, query: this.page.param.ip}).then(response => {
        this.dataList = response.Data.IPList
        this.page.total = response.Data.TotalNumber
        this.listLoading = false
      }).catch(err => {
        this.dataList = [],
        this.page.total = 0,
        this.listLoading = false
      })
    },
    handleFilter() {
      this.page.param.ip = this.page.temp_query
      this.fetchData(1)
    },
    indexMethod(index) {
      return (this.page.page-1)*this.page.limit+index+1;
    },
    startLoading(targetDom) {
      return this.$loading({
        target: targetDom,
        lock: true,//lock的修改符--默认是false
        text: "拼命加载中，请稍候...",//显示在加载图标下方的加载文案
        background: "rgba(0,0,0,0.8)",//遮罩层颜色
        spinner: "el-icon-loading",//自定义加载图标类名
      })
    },
    detailClick(ip) {
      // jduge if this tab already showed in tabs
      if(this.tabs.detailTabs.some(ele => {
        return ele.name === ip
      })) {
        this.tabs.activeName = ip
        return
      }
      // fetch ip details
      this.tabs.detailTabs.push({
        title: ip + '详情',
        name: ip,
        activeName: 'first',
        firstPage: {
          page: 1,  // 默认是第一页
          limit: 5,  // 每一页多少条记录
          total: 0,  // 总共有多少条记录
          dataList: []
        },
        secondPage: {
          page: 1,  // 默认是第一页
          limit: 5,  // 每一页多少条记录
          total: 0,  // 总共有多少条记录
          dataList: []
        },
        thirdPage: {
          page: 1,  // 默认是第一页
          limit: 5,  // 每一页多少条记录
          total: 0,  // 总共有多少条记录
          dataList: []
        },
        content: {
          IpInfo: {
            ip: '',
            country: '',
            province: '',
            city: '',
            isp: '',
            latitude: '',
            longitude: '',
          },
          Alarms: {
            subject_alarms: [],
            object_alarms: [],
          },
        } // loading time is too long, just show the tab first and then fetch data
      })
      this.tabs.activeName = ip
      this.$nextTick(function() {
        let loading = this.startLoading(document.getElementById(ip))
        getIpInfo(ip).then(response => {
          let currTab = this.tabs.detailTabs[this.tabs.detailTabs.length-1]
          currTab.content = response.Data
          currTab.firstPage.total = currTab.content.Alarms.subject_alarms.length
          currTab.firstPage.dataList = this.fetchDataFromTab(currTab.firstPage, currTab.content.Alarms.subject_alarms)
          currTab.secondPage.total = currTab.content.Alarms.object_alarms.length
          currTab.secondPage.dataList = this.fetchDataFromTab(currTab.secondPage, currTab.content.Alarms.object_alarms)
          loading.close()
        }).catch(err => {
          // nothing to do...
          console.log(err)
        })
      })
    },

    fetchDataFromTab(page, items) {
      let curr_page = page.page
      let page_size = page.limit
      let startNumber = (curr_page-1)*page_size
      let endNumber = (startNumber + page_size > items.length) ? items.length : startNumber + page_size
      return items.slice(startNumber, endNumber)
    },

    fetchFirstData(val, currTab) {
      currTab.firstPage.page = val
      currTab.firstPage.dataList = this.fetchDataFromTab(currTab.firstPage, currTab.content.Alarms.subject_alarms)
    },

    fetchSecondData(val, currTab){
      currTab.secondPage.page = val
      currTab.secondPage.dataList = this.fetchDataFromTab(currTab.secondPage, currTab.content.Alarms.object_alarms)
    },

    removeTab(targetName) {
      let tabList = this.tabs.detailTabs
      // re-calculator the activeName
      let currActiveName = this.tabs.activeName
      if(currActiveName === targetName) {
        tabList.forEach((tab, index) => {
          if (tab.name === targetName) {
            let nextTab = tabList[index + 1] || tabList[index - 1]
            if(nextTab) {
              currActiveName = nextTab.name
            }else {
              currActiveName = 'ipListPage'
            }
          }
        })
      }
      this.tabs.activeName =  currActiveName
      this.tabs.detailTabs = tabList.filter(tab => tab.name !== targetName)
    },

    onCopySuccess() {
      this.$message.success("复制成功");
    },
    onCopyError() {
      this.$message.error("复制失败");
    },

    tagFilter(ip) {
      const originLst = ['蜜罐', '日志易-waf', '日志易-云澈', '外生']
      let index = ip.length % 4
      return [originLst[index], originLst[(index + 2) % 4]]
    },
  },
  activated() {
    if(this.$route.query.ip) {
      alert('asd')
    }
  },

}
</script>

<style scoped>

  .el-aside {
    /* background-color: #E9EEF3; */
    color: #333;
    text-align: center;
  }


  .el-main {
    /* background-color: #E9EEF3; */
    color: #333;
  }

  .my-main-container {
    border: 1px solid #e2e4e6;
  }

  .top-container {
    margin-bottom: 20px;
    height: 300px;
  }

  .bottom-container {
    height: 450px;
  }


  .logo {
    text-align: center;
  }

  .logo .logo-content {
    margin-top:20px;
  }

  .logo .logo-footer {
    padding: 0 30px;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
  }

  .logo .logo-footer .risk {
    border-right: 1px solid #e2e4e6;
  }

  .logo .logo-footer>div {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
  }

  .logo .logo-footer>div .title {
    color: #969799;
    font-size: 12px;
  }

  .logo .logo-footer>div .value {
    font-size: 20px;
  }

  .logo .logo-footer .risk .safe {
    color: #52c41a;
  }

  .logo .logo-footer .risk .danger {
    color: #c41a1a;
  }

  .my-general-main {
    height: 200px;
    border-bottom: 1px solid #e2e4e6;
  }

  .my-general-main .name-tag {
    text-align: left;
    margin-top: 10px
  }

  .my-general-main .name-tag .name {
    padding-bottom: 40px;
    width: 100%;
  }

  .my-general-main .name-tag .name .title {
    width: 100%;
    font-size: 14px;
    color: #969799;
  }

  .my-general-main .name-tag .name .content {
    font-size: 32px;
    line-height: 35px;
    font-weight: 600;
    color: #2b2c2d;
    float: left;
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }

  .my-general-main .name-tag .name .copy {
    margin-left: 10px;
  }

  .my-general-main .name-tag .tag .title {
    color: #969799;
    font-size: 14px;
    line-height: 25px;
  }

  .my-general-main .name-tag .tag .my-icon {
    font-size: 10px;
    margin-left: 2px;
  }

  .my-general-footer {
    height: 100px
  }

  .my-general-footer .item-wrap {
    float: left;
    width: 33.333333%;
    min-height: 60px;
    padding: 2px 8px 0;
    height: 50%
  }

  .my-general-footer .item-wrap .icon-wrap {
    line-height: 35px;
    color: #2b2c2d;
  }

  .my-general-footer .item-wrap .label-wrap {
      font-size: 14px;
      color: #2b2c2d;
      margin-left: 4px
  }

  .my-general-footer .item-wrap .value-wrap {
    font-size: 12px;
    line-height: 20px;
    color: #646566;
    word-break: break-all;
  }





</style>
