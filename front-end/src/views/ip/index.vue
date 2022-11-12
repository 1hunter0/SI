<template>
<div class="app-container">
    <el-tabs v-model="tabs.activeName" type="card" @tab-remove="removeTab">
      <el-tab-pane label="IP列表" name="ipListPage" >
        <div class="filter-container">
          <el-input v-model="page.param.ip" placeholder="根据ip查询" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
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
            height="760"
            highlight-current-row
        >
          <el-table-column align="center" label="序号" type="index" width="50" :index="indexMethod" />
          <el-table-column label="IP" align="center">
            <template slot-scope="scope">
              {{ scope.row.ip }}
            </template>
          </el-table-column>
          <el-table-column label="国家" align="center">
            <template slot-scope="scope">
              {{ scope.row.country }}
            </template>
          </el-table-column>
          <el-table-column label="省份" align="center">
            <template slot-scope="scope">
              {{scope.row.province }}
            </template>
          </el-table-column>
          <el-table-column label="城市" align="center">
            <template slot-scope="scope">
              {{ scope.row.city }}
            </template>
          </el-table-column>
          <el-table-column label="运营商" align="center">
            <template slot-scope="scope">
              {{ scope.row.isp }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="地理位置">
            <template slot-scope="scope">
              {{ scope.row.latitude }}<br/>
              {{ scope.row.longitude }}
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
      >
        {{item.content}}
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import {getIPList} from '@/api/ip'
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
        param: {ip: ''}  // 可以根据ip地址模糊查询
      },
      tabs: { // 标签页数据
        activeName: 'ipListPage',
        detailTabs: [],
      }
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
      getIPList({page: this.page.page, limit: this.page.limit, query: this.page.param.ip}).then(response => {
        this.dataList = response.Data.ips
        this.page.total = response.Data.count
        this.listLoading = false
      })

    },
    handleFilter() {
      this.fetchData()
    },
    indexMethod(index) {
      return (this.page.page-1)*this.page.limit+index+1;
    },
    detailClick(ip) {
      // jduge if this tab already showed in tabs
      if(this.tabs.detailTabs.some(ele => {
        return ele.name === ip
      })) {
        this.tabs.activeName = ip
        return
      }

      this.tabs.detailTabs.push({
        title: ip + '详情',
        name: ip,
        content: ip + '具体数据'
      })
      this.tabs.activeName = ip
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
    }
  }
}
</script>

<style>

</style>
