<template>
 <div>
   <div id="chart" style="width: 100%; height:50rem" ></div>
 </div>
</template>
<script>
/* eslint-disable */
import * as  echarts from "echarts";
export default {
  props: {
    records:{
      type:Array,
      default(){
        return [];
      }
    }
  },
 data() {
   return {
   };
 },
 mounted() {
   this.initChart()
 },
 methods: {
   initChart() {
     //初始化echarts
     let myChart = echarts.init(document.getElementById('chart'))
     myChart.resize();  //自适应大小
     myChart.setOption(this.setOption());
   },
   //初始化echarts
   setOption() {
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
           data: [
             {
               name: "工作重点",
               category: 0,
             },
             {
               name: "1",
               category: 1,
             },
             {
               name: "2",
               category: 1,
             },
             {
               name: "3",
               category: 1,
             }
           ],
           links: [
             {
               source: "工作重点",
               target: "1",
             },
             {
               source: "工作重点",
               target: "2",
             },
             {
               source: "工作重点",
               target: "3",
             }
           ],
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
 },
};
</script>

<style lang="scss" scoped>
</style>
