<template>
  <div class="graph-chart">
    <div
        ref="echarts_dom"
        class="main-chart"
    />
  </div>
</template>

<script>
import echarts from "echarts";

export default {
  name: "OptimizationPage",
  data() {
    return {
      node_data: [{
        name: 'master-data-01',
        value: 'master-data-01'
      }, {
        name: 'master-data-02',
        value: 'master-data-02'
      }, {
        name: 'master-data-03',
        value: 'master-data-03'
      }, {
        name: 'data-node-04',
        value: 'data-node-04'
      }, {
        name: 'data-node-05',
        value: 'data-node-05'
      }, {
        name: 'data-node-06',
        value: 'data-node-06'
      }, {
        name: 'data-node-07',
        value: 'data-node-07'
      }],
      link_data: []
    }
  },
  mounted() {
    this.$https.get('http://127.0.0.1:8000/api/balancing_node_steps').then((response) => {
      let cur = [1.5, 1, 0.5]
      let index = 0
      response.data.forEach((item) => {
        index = (index + 1) % 3
        this.link_data.push({
          source: item.source_node,
          target: item.dest_node,
          text: `${item.index} ${item.prirep} ${item.shard}`,
          lineStyle: {
            opacity: 0.9,
            width: 2,
            curveness: cur[index],
          }
        })
      })
      this.initChart()
    })
  },
  methods: {
    // 初始化 echarts
    initChart() {
      let myChart = echarts.init(this.$refs.echarts_dom)
      myChart.setOption(this.setOption())
      myChart.resize() // 自适应大小
    },
    // 设置 echarts 参数
    setOption() {
      return {
        title: {
          text: '索引均衡分布移动示意图'
        },
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            if (params.dataType === 'node') {
              return '节点名称：' + params.name
            } else if (params.dataType === 'edge') {
              let index, p, s
              [index, p, s] = [...params.data.text.split(' ')]
              let is_p = (p === 'p') ? '是' : '否'
              return '边起点：' + params.data.source + '<br/>边终点：' + params.data.target + '<br/>索引名：' + index + '<br/>是否为主分片：' + is_p + '<br/>分片编号：' + s // 自定义边提示信息
            }
          },
        }, // 提示框
        animationDurationUpdate: 1000,
        animationEasingUpdate: "quinticInOut",
        series: [
          {
            type: 'graph',
            // layout: 'circular',
            layout: 'circular',
            symbol: 'rect',
            symbolSize: [180, 80],
            roam: true, //鼠标缩放功能
            label: {
              show: true, //是否显示标签
              fontWeight: 'bold',
              fontSize: 20
            },
            itemStyle: {
              color: '#409EFF'
            },
            symbolOffset: [-40, -20],
            focusNodeAdjacency: true, //鼠标移到节点上时突出显示结点以及邻节点和边
            edgeSymbol: ["none", "arrow"], //关系两边的展现形式，也即图中线两端的展现形式。arrow为箭头
            edgeSymbolSize: [4, 10],
            draggable: false,
            edgeLabel: {
              normal: {
                fontSize: 15,
                show: true,
                //通过回调函数设置连线上的标签
                formatter: function (x) {
                  return x.data.text
                }
              }
            },
            data: this.node_data,
            links: this.link_data
          }
        ]
      }
    }
  }
}
</script>

<style scoped>
.graph-chart {
  width: 100%;
  padding: 30px 50px;
  height: 100vh;
  box-sizing: border-box;
}
.main-chart {
  height: 100%;
  width: 1280px;
  border-radius: 50px;
  background-color: rgba(0, 0, 0, 0.02);
}
</style>
