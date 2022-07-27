<template>
  <div class="kgWidget">
    <div class="kgHead">
      <div style="margin-left:30px;">
        <span>输入查询语句进行查询:</span>
        <input type="text" style="width:700px;" v-model="query" @keyup.enter="qqq"/>
      </div>
    </div>
    <div class="flexRow kgWidgetContainer">
      <div class="editBox flexColumn">
       <div>
   <div id="chart" style="width: 100%; height:50rem" ></div>
 </div>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from "../plugins/axios.min"
  //import LocalGraph from "./LocalGraph.vue";
  /* eslint-disable */
  import * as  echarts from "echarts";
  export default {
    components: {
    },
    data() {
      return {
        query: 'MATCH p=()-->() RETURN p LIMIT 5',
        records: [],
        clearAll: false
      }
    },
    methods: {
      qqq(){
        let mdata = this.executeQuery(this.query);
        console.log(mdata)
        mdata.then(res=>{
          this.initChart(res)
        })
      },
      executeQuery(query) {
        axios.defaults.baseURL = 'http://127.0.0.1:8000/q/';
        return new Promise((resolve, reject) => {
          axios({
            url: 'http://127.0.0.1:8000/q/' + query,
            method: 'get'
          }).then(response=>{
            resolve(response)
          }).catch(function (error) {
                reject(error);
              })
        });
      },
      initChart(tdata) {
     //初始化echarts
     let myChart = echarts.init(document.getElementById('chart'))
     myChart.resize();  //自适应大小
     myChart.setOption(this.setOption(tdata));
   },
   //初始化echarts
   setOption(tdata) {
     console.log(tdata.data.response)
     let node_data=[];
     let node_set=new Set();
     let link_data=[];
     let l1=tdata.data.response;
     let ll1=l1.length;
     for(var i=0;i<ll1;i++){
       let name0;
       if(l1[i].p[0].hasOwnProperty("name"))
        name0=l1[i].p[0].name;
       else
         name0=l1[i].p[0].title;

       let name1;
       if(l1[i].p[2].hasOwnProperty("name"))
        name1=l1[i].p[2].name;
       else
         name1=l1[i].p[2].title;
       node_set.add(name0);
       node_set.add(name1);

       let sedge={"source":name0,"target":name1,"name":l1[i].p[1]}
       link_data.push(sedge);
     }
     for(let a of node_set){
       let sn={"name":a,"category":1};
       node_data.push(sn);
     }
     console.log(node_data)
     console.log(link_data)
     let option = {
       tooltip: {}, //提示框
       animationDurationUpdate: 1500,
       animationEasingUpdate: "quinticInOut",
       series: [
         {
           type: "graph",
           layout: "force",
           symbolSize: 100, //倘若该属性不在link里，则其表示节点的大小；否则即为线两端标记的大小
           symbolSize: (value, params) => {
             console.log(params)
             switch (params.data.category) {
               case 0:
                 return 100;
                 // eslint-disable-next-line no-unreachable
                 break;
               case 1:
                 return 50;
                 // eslint-disable-next-line no-unreachable
                 break;
             }
           },
           roam: true, //鼠标缩放功能
           label: {
             show: true, //是否显示标签
           },
           focusNodeAdjacency: true, //鼠标移到节点上时突出显示结点以及邻节点和边
           edgeSymbol: ["circle","arrow"], //关系两边的展现形式，也即图中线两端的展现形式。arrow为箭头
           edgeSymbolSize: [4, 10],
           draggable: true,
           edgeLabel: {
             fontSize: 14, //关系（也即线）上的标签字体大小
           },
           force: {
             repulsion: 200,
             edgeLength: 120,
           },
           data:node_data,
           links:link_data,
           lineStyle: {
             opacity: 0.9,
             width: 2,
             curveness: 0,
           },
         },
       ],
     };
     return option;
   },
    }
  }

</script>
<style>
  .kgWidget {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0
  }

  .kgWidget div,
  .kgWidget li,
  .kgWidget spanï¼Œinput,
  .kgWidget ul {
    font-size: 13px
  }

  .kgWidget .fontIcon {
    color: #b0b0b0
  }

  .kgWidget .fontIcon:hover {
    color: #424242
  }

  .kgWidget .borderTop {
    border-top: 1px solid #ccc
  }

  .kgWidget .fullHeight {
    height: 100%
  }

  .kgWidget .bold {
    font-weight: 600
  }

  .kgWidget .canDragEl {
    cursor: -webkit-grab;
    cursor: grab
  }

  .kgWidget.cursorGrabbing,
  .kgWidget.cursorGrabbing * {
    cursor: -webkit-grabbing!important;
    cursor: grabbing!important
  }

  .kgWidget input[type=text],
  .kgWidget textarea {
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    resize: none;
    height: 32px;
    line-height: 32px
  }

  .kgWidget textarea {
    height: 30px;
    line-height: 30px
  }

  .kgWidget .confirmMsg {
    text-align: center;
    padding-bottom: 20px;
    padding-top: 20px;
    font-size: 14px;
    font-weight: 700
  }

  .kgWidget .kgWidget {
    height: 100%;
    width: 100%
  }

  .kgWidget .kgWidget:before {
    content: "";
    display: table
  }

  .kgWidget .kgHead {
    position: absolute;
    top: 0;
    left: 0;
    right: 0
  }

  .kgWidget .kgContent,
  .kgWidget .kgHead,
  .kgWidget .kgLeftMenu,
  .kgWidget .kgSettings {
    background: #fff
  }

  .kgWidget .kgLeftMenu {
    height: 100%
  }

  .kgWidget .kgContent,
  .kgWidget .kgContent input,
  .kgWidget .kgLeftMenu,
  .kgWidget .kgLeftMenu input {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none
  }

  .kgWidget .kgContent,
  .kgWidget .kgSettings {
    display: -webkit-box;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-direction: column
  }

  .kgWidget .kgContent {
    overflow: hidden
  }

  .kgWidget .kgHead {
    box-shadow: 0 2px 4px rgba(0, 0, 0, .15)
  }

  .kgWidget .kgLeftMenu,
  .kgWidget .handleArea {
    box-shadow: 0 0 6px 1px rgba(0, 0, 0, .15)
  }

  .kgWidget .kgHeadBox,
  .kgWidget .kgWidgetContainer {
    width: 100%;
    /*min-width: 1280px;*/
    margin: 0 auto;
    height: 100%
  }

  .kgWidget .kgHeadBox .goback {
    display: inline-block;
    font-size: 0;
    padding: 0 10px;
    color: #757575;
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none
  }

  .kgWidget .kgHeadBox .goback:hover {
    color: #333
  }

  .kgWidget .kgHeadBox .goback i.icon {
    font-size: 20px;
    line-height: 50px
  }

  .kgWidget .kgWidgetContainer {
    box-sizing: border-box;
    padding-top: 60px;
    font-size: 12px
  }

  .kgWidget .kgHead {
    height: 50px;
    line-height: 50px
  }

  .kgWidget .kgHead .kgCancel,
  .kgWidget .kgHead .kgSave {
    display: inline-block;
    margin-left: 10px;
    height: 34px;
    line-height: 34px;
    vertical-align: middle;
    margin-top: 8px;
    width: 88px;
    text-align: center
  }

  .kgWidget .kgHead .kgCancel:not(:hover) {
    color: #ccc!important
  }

  .kgWidget .kgHead .kgSave {
    color: #fff;
    border-radius: 3px
  }

  .kgWidget .kgLeftMenu {
    width: 180px
  }

  .kgWidget .kgContent {
    width: 640px;
    border-right: 1px solid #ccc
  }

  .kgWidget .kgSettings {
    width: 464px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none
  }

  .kgWidget .kgTitle {
    font-size: 14px;
    color: #333;
    height: 40px;
    line-height: 40px;
    box-sizing: border-box
  }

  .kgWidget .flexBox {
    display: -webkit-box;
    display: flex
  }

  .kgWidget .dragPreview {
    position: absolute;
    top: 8px;
    left: 16px
  }

  .limitTxt {
    display: inline-block;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    vertical-align: top;
    max-width: 86px
  }

  .confirmSave .noHeader {
    height: 0
  }

  .confirmSave .dialogContent {
    text-align: center;
    padding: 14px 0;
    padding-right: 20px;
    height: 36px
  }

  .confirmSave .savePrompt {
    display: inline-block;
    vertical-align: middle;
    margin-top: 5px;
    color: #9e9e9e
  }

  .confirmSave .saveLoader {
    display: inline-block;
    vertical-align: middle;
    margin-right: 22px
  }

  .pointerEvents {
    pointer-events: none
  }

  .kgWidget .widgetBox {
    color: #333;
    font-size: 12px;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    height: 100%;
    display: -webkit-box;
    display: flex;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-direction: column
  }

  .kgWidget .editBoxItem {
    padding: 12px 0;
    padding-left: 10px;
    box-sizing: border-box
  }

  .kgWidget .dragHint {
    opacity: .3;
    padding: 0 0 6px 10px
  }

  .kgWidget .dragTitle {
    font-weight: 700;
    padding: 6px 0 6px 10px
  }

  .kgWidget .widgetList {
    -webkit-box-flex: 1;
    flex: 1
  }

  .kgWidget .widgetListLi {
    width: 180px;
    list-style: none;
    position: relative;
    background: #f4f5f7
  }

  .kgWidget .widgetListLi:not(.active) {
    color: #333!important
  }

  .kgWidget .widgetListLi:not(:hover) {
    background: #fff!important
  }

  .kgWidget .widgetListLi:not(:hover) .addBottomWidget {
    display: none
  }

  .kgWidget .widgetListLi .addBottomWidget {
    position: absolute;
    top: 10px;
    right: 16px;
    cursor: pointer
  }

  .kgWidget .widgetListLi .addBottomWidget .iconMenu {
    color: #ddd;
    font-size: 22px
  }

  .kgWidget .widgetListLi .addBottomWidget .iconMenu:hover {
    color: #999
  }

  .kgWidget .widgetListItem {
    padding: 12px 0 12px 10px;
    box-sizing: border-box;
    width: 100%
  }

  .kgWidget .widgetListItem i {
    font-size: 16px;
    color: #9e9e9e;
    width: 25px;
    display: inline-block
  }

  .editBox {
    font-size: 12px;
    color: #333;
    width: 100%;
    -webkit-box-flex: 1;
    flex: 1;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none
  }

  .editBox .bottomLocation {
    -webkit-box-flex: 1;
    flex: 1;
    min-height: 40px
  }

  .editBox .editArea {
    min-height: 361px;
    display: -webkit-box;
    display: flex;
    width: 100%;
    position: relative;
    background: #fff;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
    flex-direction: column
  }

  .editBox .editWidgetContainer {
    width: 100%;
    padding: 0 14px;
    box-sizing: border-box;
    padding-top: 10px
  }

  .editBox .editWidgetList {
    width: 100%;
    display: -webkit-box;
    display: flex
  }

  .kgWidget .settingsBox {
    font-size: 13px;
    color: #333;
    -webkit-box-flex: 1;
    flex: 1;
  }

  .kgWidget .settingsBox .widgetSettingsBox {
    padding-top: 24px;
    padding-left: 20px
  }

  .kgWidget .settingsBox .widgetSettingsTitle {
    padding-bottom: 22px
  }

  .kgWidget .settingsBox .widgetSettingsTitle .wsLf>span {
    opacity: 1
  }

  .kgWidget .settingsBox .radioGroup {
    display: inline-block;
    vertical-align: middle
  }

  .kgWidget .extraSettings {
    width: 100%;
    border-bottom: 1px solid #ccc
  }

  .kgWidget .extraSettings .filterSettingsTip {
    color: #b0b0b0;
    vertical-align: middle;
    margin-top: -7px;
    font-weight: 400
  }

  .kgWidget .extraSettings .filterSettingsTip:after {
    white-space: normal;
    width: 299px
  }

  .kgWidget .extraSettings .defaultSettings {
    padding-top: 12px
  }

  .kgWidget .extraSettings .extraSettingsTitle {
    font-size: 14px;
    height: 40px;
    margin-left: 20px;
    line-height: 40px
  }

  .kgWidget .extraSettings .filterSettingsBox {
    max-height: 180px;
    min-height: 88px;
    padding-bottom: 7px
  }

  .kgWidget .extraSettings .filterSettingsItem {
    float: left;
    width: 50%;
    margin-bottom: 4px;
    padding-left: 24px;
    box-sizing: border-box
  }

  .kgWidget .icon-dialpad {
    font-size: 18px
  }

  .kgWidget input[type=text],
  .kgWidget textarea {
    padding: 0 10px;
    width: 320px;
    border-radius: 3px;
    border: 1px solid
  }

  .kgWidget input[type=text]:not(.active):not(:hover),
  .kgWidget textarea:not(.active):not(:hover) {
    border-color: #ccc!important
  }

  .kgWidget input[type=text].halfInput,
  .kgWidget textarea.halfInput {
    width: 90px
  }

  .kgWidget textarea.multipleLine {
    height: auto!important;
    padding: 5px 10px;
    line-height: 20px;
    vertical-align: middle
  }

  .kgWidget input[type=radio] {
    margin-right: 10px
  }

  .kgWidget .addOption {
    display: block;
    margin-left: 40px;
    margin-top: 14px;
    cursor: pointer
  }

  .kgWidget .defaultSettings {
    padding-top: 60px;
    text-align: center;
    color: #333;
    opacity: .3;
    font-size: 14px
  }

  .kgWidget .OAOptionsBox {
    padding-left: 20px;
    margin-top: 28px
  }

  .kgWidget .OAOptionsBox .checkboxLabel {
    margin-bottom: 16px;
    display: block
  }

  .kgWidget .iconDelete {
    margin-top: -12px;
    vertical-align: middle;
    font-size: 18px
  }
</style>
