<template>
  <div class="app-container">
    <el-tabs v-model="tabs.activeName" type="card" @tab-remove="removeTab">
      <el-tab-pane label="Virus列表" name="virusListPage">
        <div class="filter-container">
          <el-input v-model.trim="page.temp_query" placeholder="查询病毒样本" style="width: 200px;" class="filter-item"
            @keyup.enter.native="handleFilter" />
          <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-search"
            @click="handleFilter">
            查询
          </el-button>
        </div>

        <el-table v-loading="listLoading" :data="dataList" element-loading-text="Loading" border fit height="720"
          highlight-current-row>
          <el-table-column align="center" label="序号" type="index" width="60" :index="indexMethod" />
          <el-table-column label="MD5" align="center">
            <template slot-scope="scope">
              {{ scope.row.md5 }}
            </template>
          </el-table-column>
          <el-table-column label="SHA1" align="center">
            <template slot-scope="scope">
              {{ scope.row.sha1 | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column label="文件名称" align="center">
            <template slot-scope="scope">
              {{ scope.row.file_name | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column label="文件类型" align="center">
            <template slot-scope="scope">
              {{ scope.row.file_type | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column label="提交时间" align="center">
            <template slot-scope="scope">
              {{ scope.row.submit_time | nullAndOtherFilter }}
            </template>
          </el-table-column>
          <el-table-column align="center" label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click="detailClick(scope.row.sha1)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-pagination v-show="page.total > 0" :total="page.total" :current-page="page.page" :page-size="page.limit"
          @current-change="fetchData" />
      </el-tab-pane>
      <el-tab-pane v-for="item in tabs.detailTabs" :key="item.name" :label="item.title" :name="item.name" closable
        :id="item.name" class="my-main-container">
        <el-container class="top-container">
          <el-aside width="300px" class="logo">
            <img :src="item.content.VirusInfo.sha1 | logoFilter" class="logo-content">
            <div class="logo-footer">
              <div class="risk">
                <div class="title">风险评估</div>
                <div :class="item.content.VirusInfo.sha1 | levelClassFilter">{{ item.content.VirusInfo.sha1 | levelFilter }}</div>
              </div>
              <div class="degree">
                <div class="title">置信度</div>
                <div class="value" style="color: #2b2c2d">{{ item.content.VirusInfo.sha1 | confidenceFilter }}</div>
              </div>
            </div>
          </el-aside>
          <el-container direction="vertical">
            <el-main class="my-general-main">
              <div class="name-tag">
                <div class="name">
                  <div class="title">FILE</div>
                  <span class="content">
                    {{ item.content.VirusInfo.sha1 }}
                  </span>
                  <el-tooltip effect="dark" content="复制" placement="top"><i class="el-icon-copy-document copy"
                      v-clipboard:copy="item.name" v-clipboard:success="onCopySuccess"
                      v-clipboard:error="onCopyError"></i></el-tooltip>
                </div>
                <div class="tag">
                  <span class="title">情报标签</span>
                  <el-tooltip effect="dark" content="情报标签命中恶意家族或攻击团伙仅表示历史上曾用过该基础设施，不作为决策依据，仅供参考" placement="top"><span
                      class="my-icon"><i class="el-icon-zoom-in tag-tip"></i></span></el-tooltip>
                  <div class="content">
                    <el-tag v-for="(origin, index1) in tagFilter(item.content.VirusInfo.sha1)"
                      :type="origin | tagClassFilter" :key="index1" effect="plain" size="mini">{{ origin }}</el-tag>
                  </div>
                </div>
              </div>
            </el-main>
            <el-main class="my-general-footer">
              <div class="item-wrap">
                <svg-icon icon-class="file-size" />
                <!--<svg-icon icon-class="earth" />
                icon="el-icon-search"-->
                <span class="label-wrap">文件类型</span>
                <div class="value-wrap">
                  {{ item.content.VirusInfo.file_type }}</div>
              </div>
              <div class="item-wrap">
                <i class="el-icon-time"></i>
                <span class="label-wrap">提交时间</span>
                <div class="value-wrap">{{ item.content.VirusInfo.submit_time }}</div>
              </div>
              <div class="item-wrap">
                <svg-icon icon-class="sponer" />
                <span class="label-wrap">威胁等级</span>
                <div class="value-wrap">{{ item.content.VirusInfo.threat_level }}</div>
              </div>
            </el-main>
          </el-container>
        </el-container>
        <el-container class="bottom-container">
          <el-main>
            <el-tabs v-model="item.activeName" type="card">
              <el-tab-pane name="first">
                <span slot="label">
                  <el-tooltip effect="dark" content="该病毒文件的基本信息" placement="top"><span>基本信息</span></el-tooltip>
                </span>
                <el-table :data="item.firstPage.dataList" fit border height="650" highlight-current-row>
                  <el-table-column label="multi_engines" align="center" width="180" fixed>
                    <template slot-scope="scope">
                      {{ scope.row.VirusInfo.multi_engines }}
                    </template>
                  </el-table-column>
                  <el-table-column label="multiengines_results" align="center" width="180">
                    <template slot-scope="scope">
                      {{ scope.row.VirusInfo.multiengines_results }}
                    </template>
                  </el-table-column>
                  <el-table-column label="sandbox_behaviors" align="center" width="180">
                    <template slot-scope="scope">
                      {{ scope.row.VirusInfo.sandbox_behaviors }}
                    </template>
                  </el-table-column>
                  <el-table-column label="sandbox_type_list" align="center" width="180">
                    <template slot-scope="scope">
                      {{ scope.row.VirusInfo.sandbox_type_list }}
                    </template>
                  </el-table-column>
                  <el-table-column label="threat_score" align="center" width="180">
                    <template slot-scope="scope">
                      {{ scope.row.VirusInfo.threat_score }}
                    </template>
                  </el-table-column>
                </el-table>
                <el-pagination v-show="item.firstPage.total > 0" :total="item.firstPage.total"
                  :current-page="item.firstPage.page" :page-size="item.firstPage.limit"
                  @current-change="fetchFirstData($event, item)" />

              </el-tab-pane>
              <el-tab-pane name="second">
                <span slot="label">
                  <el-tooltip effect="dark" content="该病毒文件的关联图" placement="top"><span >Graph</span></el-tooltip>
                </span>
                <div id="relativeGraphEchart"><ECharts ref="chart" :option="option" /></div>
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
import { getVirusInfo, getNetGraph } from '@/api/virus'
import { plugin, createComponent } from 'echarts-for-vue';
import * as echarts from 'echarts';
import Vue from 'vue';
Vue.use(plugin, { echarts });  
export default {
  name: 'Virus',
  components: {
      ECharts: createComponent({ echarts }),      // use as a component
  },
  data() {

    return {
      listLoading: false,
      dataList: null,
      buttonLoading: false,
      page: {
        page: 1,  // 默认是第一页
        limit: 10,  // 每一页多少条记录
        total: 0,  // 总共有多少条记录
        param: { sha1: '' },  // 可以根据sha1模糊查询
        temp_query: '', // 临时变量,否则点击跳转页面会根据当前搜索框内容查询，出现bug
      },
      tabs: { // 标签页数据
        activeName: 'virusListPage',
        detailTabs: [],
      },
      option : {
        title: {
          text: '',
          subtext: '',
          top: 'bottom',
          left: 'right'
        },
        tooltip: {},
        legend: [
          {
            // selectedMode: 'single',
            data: ['A','B','C']
            // data: graph.categories.map(function (a) {
            //   return a.name;
            // })
          }
        ],
        animationDuration: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            name: 'Node',
            type: 'graph',
            layout: 'none',
            data: [
      {
        "id": "0",
        "name": "Myriel",
        "symbolSize": 19.12381,
        "x": -266.82776,
        "y": 299.6904,
        "value": 28.685715,
        "category": 0
      },
      {
        "id": "1",
        "name": "Napoleon",
        "symbolSize": 2.6666666666666665,
        "x": -418.08344,
        "y": 446.8853,
        "value": 4,
        "category": 0
      },
      {
        "id": "2",
        "name": "MlleBaptistine",
        "symbolSize": 6.323809333333333,
        "x": -212.76357,
        "y": 245.29176,
        "value": 9.485714,
        "category": 1
      },
      {
        "id": "3",
        "name": "MmeMagloire",
        "symbolSize": 6.323809333333333,
        "x": -242.82404,
        "y": 235.26283,
        "value": 9.485714,
        "category": 1
      },
      {
        "id": "4",
        "name": "CountessDeLo",
        "symbolSize": 2.6666666666666665,
        "x": -379.30386,
        "y": 429.06424,
        "value": 4,
        "category": 0
      },
      {
        "id": "5",
        "name": "Geborand",
        "symbolSize": 2.6666666666666665,
        "x": -417.26337,
        "y": 406.03506,
        "value": 4,
        "category": 0
      },
      {
        "id": "6",
        "name": "Champtercier",
        "symbolSize": 2.6666666666666665,
        "x": -332.6012,
        "y": 485.16974,
        "value": 4,
        "category": 0
      },
      {
        "id": "7",
        "name": "Cravatte",
        "symbolSize": 2.6666666666666665,
        "x": -382.69568,
        "y": 475.09113,
        "value": 4,
        "category": 0
      },
      {
        "id": "8",
        "name": "Count",
        "symbolSize": 2.6666666666666665,
        "x": -320.384,
        "y": 387.17325,
        "value": 4,
        "category": 0
      },
      {
        "id": "9",
        "name": "OldMan",
        "symbolSize": 2.6666666666666665,
        "x": -344.39832,
        "y": 451.16772,
        "value": 4,
        "category": 0
      },
      {
        "id": "10",
        "name": "Labarre",
        "symbolSize": 2.6666666666666665,
        "x": -89.34107,
        "y": 234.56128,
        "value": 4,
        "category": 1
      },
      {
        "id": "11",
        "name": "Valjean",
        "symbolSize": 66.66666666666667,
        "x": -87.93029,
        "y": -6.8120565,
        "value": 100,
        "category": 1
      },
      {
        "id": "12",
        "name": "Marguerite",
        "symbolSize": 4.495239333333333,
        "x": -339.77908,
        "y": -184.69139,
        "value": 6.742859,
        "category": 1
      },
      {
        "id": "13",
        "name": "MmeDeR",
        "symbolSize": 2.6666666666666665,
        "x": -194.31313,
        "y": 178.55301,
        "value": 4,
        "category": 1
      },
      {
        "id": "14",
        "name": "Isabeau",
        "symbolSize": 2.6666666666666665,
        "x": -158.05168,
        "y": 201.99768,
        "value": 4,
        "category": 1
      },
      {
        "id": "15",
        "name": "Gervais",
        "symbolSize": 2.6666666666666665,
        "x": -127.701546,
        "y": 242.55057,
        "value": 4,
        "category": 1
      },
      {
        "id": "16",
        "name": "Tholomyes",
        "symbolSize": 17.295237333333333,
        "x": -385.2226,
        "y": -393.5572,
        "value": 25.942856,
        "category": 2
      },
      {
        "id": "17",
        "name": "Listolier",
        "symbolSize": 13.638097333333334,
        "x": -516.55884,
        "y": -393.98975,
        "value": 20.457146,
        "category": 2
      },
      {
        "id": "18",
        "name": "Fameuil",
        "symbolSize": 13.638097333333334,
        "x": -464.79382,
        "y": -493.57944,
        "value": 20.457146,
        "category": 2
      },
      {
        "id": "19",
        "name": "Blacheville",
        "symbolSize": 13.638097333333334,
        "x": -515.1624,
        "y": -456.9891,
        "value": 20.457146,
        "category": 2
      },
      {
        "id": "20",
        "name": "Favourite",
        "symbolSize": 13.638097333333334,
        "x": -408.12122,
        "y": -464.5048,
        "value": 20.457146,
        "category": 2
      },
      {
        "id": "21",
        "name": "Dahlia",
        "symbolSize": 13.638097333333334,
        "x": -456.44113,
        "y": -425.13303,
        "value": 20.457146,
        "category": 2
      },
      {
        "id": "22",
        "name": "Zephine",
        "symbolSize": 13.638097333333334,
        "x": -459.1107,
        "y": -362.5133,
        "value": 20.457146,
        "category": 2
      },
      {
        "id": "23",
        "name": "Fantine",
        "symbolSize": 28.266666666666666,
        "x": -313.42786,
        "y": -289.44803,
        "value": 42.4,
        "category": 2
      },
      {
        "id": "24",
        "name": "MmeThenardier",
        "symbolSize": 20.95238266666667,
        "x": 4.6313396,
        "y": -273.8517,
        "value": 31.428574,
        "category": 7
      },
      {
        "id": "25",
        "name": "Thenardier",
        "symbolSize": 30.095235333333335,
        "x": 82.80825,
        "y": -203.1144,
        "value": 45.142853,
        "category": 7
      },
      {
        "id": "26",
        "name": "Cosette",
        "symbolSize": 20.95238266666667,
        "x": 78.64646,
        "y": -31.512747,
        "value": 31.428574,
        "category": 6
      },
      {
        "id": "27",
        "name": "Javert",
        "symbolSize": 31.923806666666668,
        "x": -81.46074,
        "y": -204.20204,
        "value": 47.88571,
        "category": 7
      },
      {
        "id": "28",
        "name": "Fauchelevent",
        "symbolSize": 8.152382000000001,
        "x": -225.73984,
        "y": 82.41631,
        "value": 12.228573,
        "category": 4
      },
      {
        "id": "29",
        "name": "Bamatabois",
        "symbolSize": 15.466666666666667,
        "x": -385.6842,
        "y": -20.206686,
        "value": 23.2,
        "category": 3
      },
      {
        "id": "30",
        "name": "Perpetue",
        "symbolSize": 4.495239333333333,
        "x": -403.92447,
        "y": -197.69823,
        "value": 6.742859,
        "category": 2
      },
      {
        "id": "31",
        "name": "Simplice",
        "symbolSize": 8.152382000000001,
        "x": -281.4253,
        "y": -158.45137,
        "value": 12.228573,
        "category": 2
      },
      {
        "id": "32",
        "name": "Scaufflaire",
        "symbolSize": 2.6666666666666665,
        "x": -122.41348,
        "y": 210.37503,
        "value": 4,
        "category": 1
      },
      {
        "id": "33",
        "name": "Woman1",
        "symbolSize": 4.495239333333333,
        "x": -234.6001,
        "y": -113.15067,
        "value": 6.742859,
        "category": 1
      },
      {
        "id": "34",
        "name": "Judge",
        "symbolSize": 11.809524666666666,
        "x": -387.84915,
        "y": 58.7059,
        "value": 17.714287,
        "category": 3
      },
      {
        "id": "35",
        "name": "Champmathieu",
        "symbolSize": 11.809524666666666,
        "x": -338.2307,
        "y": 87.48405,
        "value": 17.714287,
        "category": 3
      },
      {
        "id": "36",
        "name": "Brevet",
        "symbolSize": 11.809524666666666,
        "x": -453.26874,
        "y": 58.94648,
        "value": 17.714287,
        "category": 3
      },
      {
        "id": "37",
        "name": "Chenildieu",
        "symbolSize": 11.809524666666666,
        "x": -386.44904,
        "y": 140.05937,
        "value": 17.714287,
        "category": 3
      },
      {
        "id": "38",
        "name": "Cochepaille",
        "symbolSize": 11.809524666666666,
        "x": -446.7876,
        "y": 123.38005,
        "value": 17.714287,
        "category": 3
      },
      {
        "id": "39",
        "name": "Pontmercy",
        "symbolSize": 6.323809333333333,
        "x": 336.49738,
        "y": -269.55914,
        "value": 9.485714,
        "category": 6
      },
      {
        "id": "40",
        "name": "Boulatruelle",
        "symbolSize": 2.6666666666666665,
        "x": 29.187843,
        "y": -460.13132,
        "value": 4,
        "category": 7
      },
      {
        "id": "41",
        "name": "Eponine",
        "symbolSize": 20.95238266666667,
        "x": 238.36697,
        "y": -210.00926,
        "value": 31.428574,
        "category": 7
      },
      {
        "id": "42",
        "name": "Anzelma",
        "symbolSize": 6.323809333333333,
        "x": 189.69513,
        "y": -346.50662,
        "value": 9.485714,
        "category": 7
      },
      {
        "id": "43",
        "name": "Woman2",
        "symbolSize": 6.323809333333333,
        "x": -187.00418,
        "y": -145.02663,
        "value": 9.485714,
        "category": 6
      },
      {
        "id": "44",
        "name": "MotherInnocent",
        "symbolSize": 4.495239333333333,
        "x": -252.99521,
        "y": 129.87549,
        "value": 6.742859,
        "category": 4
      },
      {
        "id": "45",
        "name": "Gribier",
        "symbolSize": 2.6666666666666665,
        "x": -296.07935,
        "y": 163.11964,
        "value": 4,
        "category": 4
      },
      {
        "id": "46",
        "name": "Jondrette",
        "symbolSize": 2.6666666666666665,
        "x": 550.3201,
        "y": 522.4031,
        "value": 4,
        "category": 5
      },
      {
        "id": "47",
        "name": "MmeBurgon",
        "symbolSize": 4.495239333333333,
        "x": 488.13535,
        "y": 356.8573,
        "value": 6.742859,
        "category": 5
      },
      {
        "id": "48",
        "name": "Gavroche",
        "symbolSize": 41.06667066666667,
        "x": 387.89572,
        "y": 110.462326,
        "value": 61.600006,
        "category": 8
      },
      {
        "id": "49",
        "name": "Gillenormand",
        "symbolSize": 13.638097333333334,
        "x": 126.4831,
        "y": 68.10622,
        "value": 20.457146,
        "category": 6
      },
      {
        "id": "50",
        "name": "Magnon",
        "symbolSize": 4.495239333333333,
        "x": 127.07365,
        "y": -113.05923,
        "value": 6.742859,
        "category": 6
      },
      {
        "id": "51",
        "name": "MlleGillenormand",
        "symbolSize": 13.638097333333334,
        "x": 162.63559,
        "y": 117.6565,
        "value": 20.457146,
        "category": 6
      },
      {
        "id": "52",
        "name": "MmePontmercy",
        "symbolSize": 4.495239333333333,
        "x": 353.66415,
        "y": -205.89165,
        "value": 6.742859,
        "category": 6
      },
      {
        "id": "53",
        "name": "MlleVaubois",
        "symbolSize": 2.6666666666666665,
        "x": 165.43939,
        "y": 339.7736,
        "value": 4,
        "category": 6
      },
      {
        "id": "54",
        "name": "LtGillenormand",
        "symbolSize": 8.152382000000001,
        "x": 137.69348,
        "y": 196.1069,
        "value": 12.228573,
        "category": 6
      },
      {
        "id": "55",
        "name": "Marius",
        "symbolSize": 35.58095333333333,
        "x": 206.44687,
        "y": -13.805411,
        "value": 53.37143,
        "category": 6
      },
      {
        "id": "56",
        "name": "BaronessT",
        "symbolSize": 4.495239333333333,
        "x": 194.82993,
        "y": 224.78036,
        "value": 6.742859,
        "category": 6
      },
      {
        "id": "57",
        "name": "Mabeuf",
        "symbolSize": 20.95238266666667,
        "x": 597.6618,
        "y": 135.18481,
        "value": 31.428574,
        "category": 8
      },
      {
        "id": "58",
        "name": "Enjolras",
        "symbolSize": 28.266666666666666,
        "x": 355.78366,
        "y": -74.882454,
        "value": 42.4,
        "category": 8
      },
      {
        "id": "59",
        "name": "Combeferre",
        "symbolSize": 20.95238266666667,
        "x": 515.2961,
        "y": -46.167564,
        "value": 31.428574,
        "category": 8
      },
      {
        "id": "60",
        "name": "Prouvaire",
        "symbolSize": 17.295237333333333,
        "x": 614.29285,
        "y": -69.3104,
        "value": 25.942856,
        "category": 8
      },
      {
        "id": "61",
        "name": "Feuilly",
        "symbolSize": 20.95238266666667,
        "x": 550.1917,
        "y": -128.17537,
        "value": 31.428574,
        "category": 8
      },
      {
        "id": "62",
        "name": "Courfeyrac",
        "symbolSize": 24.609526666666667,
        "x": 436.17184,
        "y": -12.7286825,
        "value": 36.91429,
        "category": 8
      },
      {
        "id": "63",
        "name": "Bahorel",
        "symbolSize": 22.780953333333333,
        "x": 602.55225,
        "y": 16.421427,
        "value": 34.17143,
        "category": 8
      },
      {
        "id": "64",
        "name": "Bossuet",
        "symbolSize": 24.609526666666667,
        "x": 455.81955,
        "y": -115.45826,
        "value": 36.91429,
        "category": 8
      },
      {
        "id": "65",
        "name": "Joly",
        "symbolSize": 22.780953333333333,
        "x": 516.40784,
        "y": 47.242233,
        "value": 34.17143,
        "category": 8
      },
      {
        "id": "66",
        "name": "Grantaire",
        "symbolSize": 19.12381,
        "x": 646.4313,
        "y": -151.06331,
        "value": 28.685715,
        "category": 8
      },
      {
        "id": "67",
        "name": "MotherPlutarch",
        "symbolSize": 2.6666666666666665,
        "x": 668.9568,
        "y": 204.65488,
        "value": 4,
        "category": 8
      },
      {
        "id": "68",
        "name": "Gueulemer",
        "symbolSize": 19.12381,
        "x": 78.4799,
        "y": -347.15146,
        "value": 28.685715,
        "category": 7
      },
      {
        "id": "69",
        "name": "Babet",
        "symbolSize": 19.12381,
        "x": 150.35959,
        "y": -298.50797,
        "value": 28.685715,
        "category": 7
      },
      {
        "id": "70",
        "name": "Claquesous",
        "symbolSize": 19.12381,
        "x": 137.3717,
        "y": -410.2809,
        "value": 28.685715,
        "category": 7
      },
      {
        "id": "71",
        "name": "Montparnasse",
        "symbolSize": 17.295237333333333,
        "x": 234.87747,
        "y": -400.85983,
        "value": 25.942856,
        "category": 7
      },
      {
        "id": "72",
        "name": "Toussaint",
        "symbolSize": 6.323809333333333,
        "x": 40.942253,
        "y": 113.78272,
        "value": 9.485714,
        "category": 1
      },
      {
        "id": "73",
        "name": "Child1",
        "symbolSize": 4.495239333333333,
        "x": 437.939,
        "y": 291.58234,
        "value": 6.742859,
        "category": 8
      },
      {
        "id": "74",
        "name": "Child2",
        "symbolSize": 4.495239333333333,
        "x": 466.04922,
        "y": 283.3606,
        "value": 6.742859,
        "category": 8
      },
      {
        "id": "75",
        "name": "Brujon",
        "symbolSize": 13.638097333333334,
        "x": 238.79364,
        "y": -314.06345,
        "value": 20.457146,
        "category": 7
      },
      {
        "id": "76",
        "name": "MmeHucheloup",
        "symbolSize": 13.638097333333334,
        "x": 712.18353,
        "y": 4.8131495,
        "value": 20.457146,
        "category": 8
      }
    ],
            links: [
      {
        "source": "1",
        "target": "0"
      },
      {
        "source": "2",
        "target": "0"
      },
      {
        "source": "3",
        "target": "0"
      },
      {
        "source": "3",
        "target": "2"
      },
      {
        "source": "4",
        "target": "0"
      },
      {
        "source": "5",
        "target": "0"
      },
      {
        "source": "6",
        "target": "0"
      },
      {
        "source": "7",
        "target": "0"
      },
      {
        "source": "8",
        "target": "0"
      },
      {
        "source": "9",
        "target": "0"
      },
      {
        "source": "11",
        "target": "0"
      },
      {
        "source": "11",
        "target": "2"
      },
      {
        "source": "11",
        "target": "3"
      },
      {
        "source": "11",
        "target": "10"
      },
      {
        "source": "12",
        "target": "11"
      },
      {
        "source": "13",
        "target": "11"
      },
      {
        "source": "14",
        "target": "11"
      },
      {
        "source": "15",
        "target": "11"
      },
      {
        "source": "17",
        "target": "16"
      },
      {
        "source": "18",
        "target": "16"
      },
      {
        "source": "18",
        "target": "17"
      },
      {
        "source": "19",
        "target": "16"
      },
      {
        "source": "19",
        "target": "17"
      },
      {
        "source": "19",
        "target": "18"
      },
      {
        "source": "20",
        "target": "16"
      },
      {
        "source": "20",
        "target": "17"
      },
      {
        "source": "20",
        "target": "18"
      },
      {
        "source": "20",
        "target": "19"
      },
      {
        "source": "21",
        "target": "16"
      },
      {
        "source": "21",
        "target": "17"
      },
      {
        "source": "21",
        "target": "18"
      },
      {
        "source": "21",
        "target": "19"
      },
      {
        "source": "21",
        "target": "20"
      },
      {
        "source": "22",
        "target": "16"
      },
      {
        "source": "22",
        "target": "17"
      },
      {
        "source": "22",
        "target": "18"
      },
      {
        "source": "22",
        "target": "19"
      },
      {
        "source": "22",
        "target": "20"
      },
      {
        "source": "22",
        "target": "21"
      },
      {
        "source": "23",
        "target": "11"
      },
      {
        "source": "23",
        "target": "12"
      },
      {
        "source": "23",
        "target": "16"
      },
      {
        "source": "23",
        "target": "17"
      },
      {
        "source": "23",
        "target": "18"
      },
      {
        "source": "23",
        "target": "19"
      },
      {
        "source": "23",
        "target": "20"
      },
      {
        "source": "23",
        "target": "21"
      },
      {
        "source": "23",
        "target": "22"
      },
      {
        "source": "24",
        "target": "11"
      },
      {
        "source": "24",
        "target": "23"
      },
      {
        "source": "25",
        "target": "11"
      },
      {
        "source": "25",
        "target": "23"
      },
      {
        "source": "25",
        "target": "24"
      },
      {
        "source": "26",
        "target": "11"
      },
      {
        "source": "26",
        "target": "16"
      },
      {
        "source": "26",
        "target": "24"
      },
      {
        "source": "26",
        "target": "25"
      },
      {
        "source": "27",
        "target": "11"
      },
      {
        "source": "27",
        "target": "23"
      },
      {
        "source": "27",
        "target": "24"
      },
      {
        "source": "27",
        "target": "25"
      },
      {
        "source": "27",
        "target": "26"
      },
      {
        "source": "28",
        "target": "11"
      },
      {
        "source": "28",
        "target": "27"
      },
      {
        "source": "29",
        "target": "11"
      },
      {
        "source": "29",
        "target": "23"
      },
      {
        "source": "29",
        "target": "27"
      },
      {
        "source": "30",
        "target": "23"
      },
      {
        "source": "31",
        "target": "11"
      },
      {
        "source": "31",
        "target": "23"
      },
      {
        "source": "31",
        "target": "27"
      },
      {
        "source": "31",
        "target": "30"
      },
      {
        "source": "32",
        "target": "11"
      },
      {
        "source": "33",
        "target": "11"
      },
      {
        "source": "33",
        "target": "27"
      },
      {
        "source": "34",
        "target": "11"
      },
      {
        "source": "34",
        "target": "29"
      },
      {
        "source": "35",
        "target": "11"
      },
      {
        "source": "35",
        "target": "29"
      },
      {
        "source": "35",
        "target": "34"
      },
      {
        "source": "36",
        "target": "11"
      },
      {
        "source": "36",
        "target": "29"
      },
      {
        "source": "36",
        "target": "34"
      },
      {
        "source": "36",
        "target": "35"
      },
      {
        "source": "37",
        "target": "11"
      },
      {
        "source": "37",
        "target": "29"
      },
      {
        "source": "37",
        "target": "34"
      },
      {
        "source": "37",
        "target": "35"
      },
      {
        "source": "37",
        "target": "36"
      },
      {
        "source": "38",
        "target": "11"
      },
      {
        "source": "38",
        "target": "29"
      },
      {
        "source": "38",
        "target": "34"
      },
      {
        "source": "38",
        "target": "35"
      },
      {
        "source": "38",
        "target": "36"
      },
      {
        "source": "38",
        "target": "37"
      },
      {
        "source": "39",
        "target": "25"
      },
      {
        "source": "40",
        "target": "25"
      },
      {
        "source": "41",
        "target": "24"
      },
      {
        "source": "41",
        "target": "25"
      },
      {
        "source": "42",
        "target": "24"
      },
      {
        "source": "42",
        "target": "25"
      },
      {
        "source": "42",
        "target": "41"
      },
      {
        "source": "43",
        "target": "11"
      },
      {
        "source": "43",
        "target": "26"
      },
      {
        "source": "43",
        "target": "27"
      },
      {
        "source": "44",
        "target": "11"
      },
      {
        "source": "44",
        "target": "28"
      },
      {
        "source": "45",
        "target": "28"
      },
      {
        "source": "47",
        "target": "46"
      },
      {
        "source": "48",
        "target": "11"
      },
      {
        "source": "48",
        "target": "25"
      },
      {
        "source": "48",
        "target": "27"
      },
      {
        "source": "48",
        "target": "47"
      },
      {
        "source": "49",
        "target": "11"
      },
      {
        "source": "49",
        "target": "26"
      },
      {
        "source": "50",
        "target": "24"
      },
      {
        "source": "50",
        "target": "49"
      },
      {
        "source": "51",
        "target": "11"
      },
      {
        "source": "51",
        "target": "26"
      },
      {
        "source": "51",
        "target": "49"
      },
      {
        "source": "52",
        "target": "39"
      },
      {
        "source": "52",
        "target": "51"
      },
      {
        "source": "53",
        "target": "51"
      },
      {
        "source": "54",
        "target": "26"
      },
      {
        "source": "54",
        "target": "49"
      },
      {
        "source": "54",
        "target": "51"
      },
      {
        "source": "55",
        "target": "11"
      },
      {
        "source": "55",
        "target": "16"
      },
      {
        "source": "55",
        "target": "25"
      },
      {
        "source": "55",
        "target": "26"
      },
      {
        "source": "55",
        "target": "39"
      },
      {
        "source": "55",
        "target": "41"
      },
      {
        "source": "55",
        "target": "48"
      },
      {
        "source": "55",
        "target": "49"
      },
      {
        "source": "55",
        "target": "51"
      },
      {
        "source": "55",
        "target": "54"
      },
      {
        "source": "56",
        "target": "49"
      },
      {
        "source": "56",
        "target": "55"
      },
      {
        "source": "57",
        "target": "41"
      },
      {
        "source": "57",
        "target": "48"
      },
      {
        "source": "57",
        "target": "55"
      },
      {
        "source": "58",
        "target": "11"
      },
      {
        "source": "58",
        "target": "27"
      },
      {
        "source": "58",
        "target": "48"
      },
      {
        "source": "58",
        "target": "55"
      },
      {
        "source": "58",
        "target": "57"
      },
      {
        "source": "59",
        "target": "48"
      },
      {
        "source": "59",
        "target": "55"
      },
      {
        "source": "59",
        "target": "57"
      },
      {
        "source": "59",
        "target": "58"
      },
      {
        "source": "60",
        "target": "48"
      },
      {
        "source": "60",
        "target": "58"
      },
      {
        "source": "60",
        "target": "59"
      },
      {
        "source": "61",
        "target": "48"
      },
      {
        "source": "61",
        "target": "55"
      },
      {
        "source": "61",
        "target": "57"
      },
      {
        "source": "61",
        "target": "58"
      },
      {
        "source": "61",
        "target": "59"
      },
      {
        "source": "61",
        "target": "60"
      },
      {
        "source": "62",
        "target": "41"
      },
      {
        "source": "62",
        "target": "48"
      },
      {
        "source": "62",
        "target": "55"
      },
      {
        "source": "62",
        "target": "57"
      },
      {
        "source": "62",
        "target": "58"
      },
      {
        "source": "62",
        "target": "59"
      },
      {
        "source": "62",
        "target": "60"
      },
      {
        "source": "62",
        "target": "61"
      },
      {
        "source": "63",
        "target": "48"
      },
      {
        "source": "63",
        "target": "55"
      },
      {
        "source": "63",
        "target": "57"
      },
      {
        "source": "63",
        "target": "58"
      },
      {
        "source": "63",
        "target": "59"
      },
      {
        "source": "63",
        "target": "60"
      },
      {
        "source": "63",
        "target": "61"
      },
      {
        "source": "63",
        "target": "62"
      },
      {
        "source": "64",
        "target": "11"
      },
      {
        "source": "64",
        "target": "48"
      },
      {
        "source": "64",
        "target": "55"
      },
      {
        "source": "64",
        "target": "57"
      },
      {
        "source": "64",
        "target": "58"
      },
      {
        "source": "64",
        "target": "59"
      },
      {
        "source": "64",
        "target": "60"
      },
      {
        "source": "64",
        "target": "61"
      },
      {
        "source": "64",
        "target": "62"
      },
      {
        "source": "64",
        "target": "63"
      },
      {
        "source": "65",
        "target": "48"
      },
      {
        "source": "65",
        "target": "55"
      },
      {
        "source": "65",
        "target": "57"
      },
      {
        "source": "65",
        "target": "58"
      },
      {
        "source": "65",
        "target": "59"
      },
      {
        "source": "65",
        "target": "60"
      },
      {
        "source": "65",
        "target": "61"
      },
      {
        "source": "65",
        "target": "62"
      },
      {
        "source": "65",
        "target": "63"
      },
      {
        "source": "65",
        "target": "64"
      },
      {
        "source": "66",
        "target": "48"
      },
      {
        "source": "66",
        "target": "58"
      },
      {
        "source": "66",
        "target": "59"
      },
      {
        "source": "66",
        "target": "60"
      },
      {
        "source": "66",
        "target": "61"
      },
      {
        "source": "66",
        "target": "62"
      },
      {
        "source": "66",
        "target": "63"
      },
      {
        "source": "66",
        "target": "64"
      },
      {
        "source": "66",
        "target": "65"
      },
      {
        "source": "67",
        "target": "57"
      },
      {
        "source": "68",
        "target": "11"
      },
      {
        "source": "68",
        "target": "24"
      },
      {
        "source": "68",
        "target": "25"
      },
      {
        "source": "68",
        "target": "27"
      },
      {
        "source": "68",
        "target": "41"
      },
      {
        "source": "68",
        "target": "48"
      },
      {
        "source": "69",
        "target": "11"
      },
      {
        "source": "69",
        "target": "24"
      },
      {
        "source": "69",
        "target": "25"
      },
      {
        "source": "69",
        "target": "27"
      },
      {
        "source": "69",
        "target": "41"
      },
      {
        "source": "69",
        "target": "48"
      },
      {
        "source": "69",
        "target": "68"
      },
      {
        "source": "70",
        "target": "11"
      },
      {
        "source": "70",
        "target": "24"
      },
      {
        "source": "70",
        "target": "25"
      },
      {
        "source": "70",
        "target": "27"
      },
      {
        "source": "70",
        "target": "41"
      },
      {
        "source": "70",
        "target": "58"
      },
      {
        "source": "70",
        "target": "68"
      },
      {
        "source": "70",
        "target": "69"
      },
      {
        "source": "71",
        "target": "11"
      },
      {
        "source": "71",
        "target": "25"
      },
      {
        "source": "71",
        "target": "27"
      },
      {
        "source": "71",
        "target": "41"
      },
      {
        "source": "71",
        "target": "48"
      },
      {
        "source": "71",
        "target": "68"
      },
      {
        "source": "71",
        "target": "69"
      },
      {
        "source": "71",
        "target": "70"
      },
      {
        "source": "72",
        "target": "11"
      },
      {
        "source": "72",
        "target": "26"
      },
      {
        "source": "72",
        "target": "27"
      },
      {
        "source": "73",
        "target": "48"
      },
      {
        "source": "74",
        "target": "48"
      },
      {
        "source": "74",
        "target": "73"
      },
      {
        "source": "75",
        "target": "25"
      },
      {
        "source": "75",
        "target": "41"
      },
      {
        "source": "75",
        "target": "48"
      },
      {
        "source": "75",
        "target": "68"
      },
      {
        "source": "75",
        "target": "69"
      },
      {
        "source": "75",
        "target": "70"
      },
      {
        "source": "75",
        "target": "71"
      },
      {
        "source": "76",
        "target": "48"
      },
      {
        "source": "76",
        "target": "58"
      },
      {
        "source": "76",
        "target": "62"
      },
      {
        "source": "76",
        "target": "63"
      },
      {
        "source": "76",
        "target": "64"
      },
      {
        "source": "76",
        "target": "65"
      },
      {
        "source": "76",
        "target": "66"
      }
    ],
            categories: [
      {
        "name": "A"
      },
      {
        "name": "B"
      },
      {
        "name": "C"
      },],
            roam: true,
            label: {
              position: 'right',
              formatter: '{b}'
            },
            lineStyle: {
              color: 'source',
              curveness: 0.3
            },
            emphasis: {
              focus: 'adjacency',
              lineStyle: {
                width: 10
              }
            }
          }
        ]
      }
    }
  },
  filters: {
    nullAndOtherFilter(oldVal) {
      if (!oldVal) {
        return null
      } else if (oldVal == 'other') {
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
    levelFilter(sha1) { // todo(tanrenxuan): replace with our field
      let level = sha1.length % 2 // 0: 安全 1：危险
      const levelToDescription = {
        0: "安全",
        1: "危险",
      }
      return levelToDescription[level]
    },
    levelClassFilter(sha1) { // todo(tanrenxuan): replace with our field
      let level = sha1.length % 2 // 0: 安全 1：危险
      const levelToClass = {
        0: "safe",
        1: "danger"
      }
      return [levelToClass[level], 'value']
    },
    confidenceFilter(sha1) { // todo(tanrenxuan): replace with our field
      let confidence = sha1.length % 3 // 0: 低 1:中 2:高
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
    }
  },
  mounted() {
    // this.fetchData()
  },
  methods: {
    fetchData(val) {
      if (val != null && val !== '') {
        this.page.page = val
      }
      this.listLoading = true
      getVirusInfo(this.page.param.sha1).then(response => {
        this.dataList = [response.Data]
        this.page.total = 1
        this.listLoading = false
      }).catch(err => {
        this.dataList = [],
          this.page.total = 0,
          this.listLoading = false
      })
    },
    handleFilter() {
      this.page.param.sha1 = this.page.temp_query
      this.fetchData(1)
      console.log(Array.isArray(this.dataList))
      console.log(this.dataList)
    },
    indexMethod(index) {
      return (this.page.page - 1) * this.page.limit + index + 1;
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
    detailClick(sha1) {
      // judge if this tab already showed in tabs
      if (this.tabs.detailTabs.some(ele => {
        return ele.name === sha1
      })) {
        this.tabs.activeName = sha1
        return
      }
      // fetch virus details
      this.tabs.detailTabs.push({
        title: sha1 + '详情',
        name: sha1,
        activeName: 'first',
        firstPage: {
          page: 1,  // 默认是第一页
          limit: 5,  // 每一页多少条记录
          total: 0,  // 总共有多少条记录
          dataList: []
        },
        content: {
          VirusInfo: {
            sha1: '',
            file_name: '',
            file_type: '',
            id: '',
            md5: '',
            multi_engines: '',
            multiengines_results: '',
            sandbox_behaviors: '',
            sandbox_type_list: '',
            submit_time: '',
            threat_level: '', 
            threat_score: ''
          }
        } // loading time is too long, just show the tab first and then fetch data
      })
      this.tabs.activeName = sha1
      this.$nextTick(function () {
        let loading = this.startLoading(document.getElementById(sha1))
        getNetGraph(sha1).then(response => {
          this.option.series.data = response.Data.nodes;
          this.option.series.links = response.Data.links;
          console.log("response.nodes")
          console.log(response.Data.nodes)
          console.log(this.option.series.data)
          console.log("response.links")
          console.log(response.Data.links)
          console.log(this.option.series.links)
        })
        getVirusInfo(sha1).then(response => {
          let currTab = this.tabs.detailTabs[this.tabs.detailTabs.length - 1]
          currTab.content = {VirusInfo: response.Data}
          currTab.firstPage.total = currTab.content.length
          currTab.firstPage.dataList = [currTab.content]
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
      let startNumber = (curr_page - 1) * page_size
      let endNumber = (startNumber + page_size > items.length) ? items.length : startNumber + page_size
      return items.slice(startNumber, endNumber)
    },

    fetchFirstData(val, currTab) {
      currTab.firstPage.page = val
      currTab.firstPage.dataList = this.fetchDataFromTab(currTab.firstPage, currTab.content.Alarms.subject_alarms)
    },

    removeTab(targetName) {
      let tabList = this.tabs.detailTabs
      // re-calculator the activeName
      let currActiveName = this.tabs.activeName
      if (currActiveName === targetName) {
        tabList.forEach((tab, index) => {
          if (tab.name === targetName) {
            let nextTab = tabList[index + 1] || tabList[index - 1]
            if (nextTab) {
              currActiveName = nextTab.name
            } else {
              currActiveName = 'virusListPage'
            }
          }
        })
      }
      this.tabs.activeName = currActiveName
      this.tabs.detailTabs = tabList.filter(tab => tab.name !== targetName)
    },

    onCopySuccess() {
      this.$message.success("复制成功");
    },
    onCopyError() {
      this.$message.error("复制失败");
    },

    tagFilter(sha1) {
      const originLst = ['蜜罐', '日志易-waf', '日志易-云澈', '外生']
      let index = sha1.length % 4
      return [originLst[index], originLst[(index + 2) % 4]]
    }
  },
  activated() {
    if (this.$route.query.ip) {
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
  height: 750px;
}


.logo {
  text-align: center;
}

.logo .logo-content {
  margin-top: 20px;
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

#relativeGraphEchart{
  top: 0px;
  left: 0px;
  overflow: hidden;
  outline: none;
  user-select: none;
  width: 1039.2px;
  height: 600px;
}

</style>
