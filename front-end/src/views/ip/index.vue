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
            <img :src="item.content.IpInfo.ip | logoFilter" style="margin-top:20px;" class="logo-content">
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
          <el-main>
            Main
          </el-main>
        </el-container>
        <!-- <br/> -->
        <el-container class="bottom-container">
            <el-main>Main</el-main>
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
        temp_query: '', // 临时变量
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
    levelFilter(ip) {
      let level = ip.length % 2 // 0: 安全 1：危险
      const levelToDescription = {
        0: "安全",
        1: "危险",
      }
      return levelToDescription[level]
    },
    levelClassFilter(ip) {
      let level = ip.length % 2 // 0: 安全 1：危险
      const levelToClass = {
        0: "safe",
        1: "danger"
      }
      return [levelToClass[level],'value']
    },
    confidenceFilter(ip) {
      let confidence = ip.length % 3 // 0: 低 1:中 2:高
      const confidenceToDescription = {
        0: "低",
        1: "中",
        2: "高"
      }
      return confidenceToDescription[confidence]
    }
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
          this.tabs.detailTabs[this.tabs.detailTabs.length-1].content = response.Data
          loading.close()
        }).catch(err => {
          // nothing to do...
          console.log(err)
        })
      })
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
    /* background-color: #D3DCE6; */
    color: #333;
    text-align: center;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }

  .my-main-container {
    border: 1px solid #e2e4e6;
  }



  .top-container {
    margin-bottom: 20px;
    height: 300px;
  }

  .bottom-container {
    height: 500px;
  }


  .logo {
    text-align: center;
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

</style>
