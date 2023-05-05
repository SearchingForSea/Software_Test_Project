<template>
  <div class="el-table--home">
    <el-table
        :data="tableData"
        class="el-table--fit"
        height="750"
        stripe
    >
      <el-table-column
          label="ID"
          width="50"
          class="table-column--item"
          type="index"
      />
      <el-table-column
          prop="index"
          label="集群名"
          width="240"
          class="table-column--item"
          :filters="valueSelect('index')"
          :filter-method="es_name_filter"
      />
      <el-table-column
          prop="shard"
          label="分片编号"
          width="120"
          class="table-column--item"
          :filters="valueSelect('shard')"
          :filter-method="es_shard_filter"
      />
      <el-table-column
          prop="prirep"
          label="主副分片"
          width="120"
          class="table-column--item"
      />
      <el-table-column
          prop="state"
          label="分片状态"
          width="150"
          class="table-column--item"
      />
      <el-table-column
          prop="docs"
          label="存储文档数"
          width="150"
          class="table-column--item"
      />
      <el-table-column
          prop="store"
          label="文档大小"
          width="100"
          class="table-column--item"
      />
      <el-table-column
          prop="ip"
          label="分片所在服务器 IP"
          width="180"
          class="table-column--item"
      />
      <el-table-column
          prop="node"
          label="节点名称"
          width="180"
          class="table-column--item"
      />
    </el-table>
  </div>
</template>

<script>
export default {
  name: "BasicInfo",
  data() {
    return {
      tableData: [],
      es_data: [],
      dataLength: 0
    }
  },
  computed: {
    valueSelect() {
      return function (arg) {
        let value_select = []
        let value_select_obj = []
        this.es_data.forEach((value) => {
          if (value_select.indexOf(value[arg]) === -1) {
            value_select.push(value[arg])
            value_select_obj.push({
              text: value[arg],
              value: value[arg]
            })
          }
        })
        return value_select_obj.sort((a, b) => {
          if (a.text < b.text) return -1
          else if (a.text === b.text) return 0
          else return 1
        })
      }
    }
  },
  created() {
    this.$https.get('http://127.0.0.1:8000/api/basic_info').then((response) => {
      response.data.forEach((value) => {
        this.es_data.push(value.fields)
      })
      this.tableData = this.es_data
    })
  },
  mounted() {
  },
  methods: {
    es_name_filter(value, row) {
      return row.index === value
    },
    es_shard_filter(value, row) {
      return row.shard === value
    },
    // onWheel(event) {
    //   if (event.deltaY < 0) {
    //     // 向上滑动
    //     this.scrollToElement('el-table--fit')
    //   } else {
    //     // 向下滑动
    //     this.scrollToElement('graph-chart')
    //   }
    // },
    // scrollToElement(className) {
    //   // 获取目标元素
    //   const toElement = document.getElementsByClassName(className)[0]
    //   const rightPage = document.getElementsByClassName('el-table--home')[0]
    //   // 计算目标元素的位置
    //   rightPage.scrollTop = toElement.offsetTop
    // },
    // 初始化 echarts
    // initChart() {
    //   let myChart = echarts.init(this.$refs.echarts_dom)
    //   myChart.setOption(this.setOption())
    //   myChart.resize() // 自适应大小
    // },
    // 设置 echarts 参数
    /*setOption() {*/
    /*  return {*/
    /*    title: {*/
    /*      text: '索引均衡分布移动示意图'*/
    /*    },*/
    /*    tooltip: {*/
    /*      trigger: 'item',*/
    /*      formatter: function(params) {*/
    /*        if (params.dataType === 'node') {*/
    /*          return '节点名称：' + params.name*/
    /*        } else if (params.dataType === 'edge') {*/
    /*          let index, p, s*/
    /*          [index, p, s] = [...params.data.text.split(' ')]*/
    /*          let is_p = (p === 'p') ? '是' : '否'*/
    /*          return '边起点：' + params.data.source + '<br/>边终点：' + params.data.target + '<br/>索引名：' + index + '<br/>是否为主分片：' + is_p + '<br/>分片编号：' + s // 自定义边提示信息*/
    /*        }*/
    /*      },*/
    /*    }, // 提示框*/
    /*    animationDurationUpdate: 1500,*/
    /*    animationEasingUpdate: "quinticInOut",*/
    /*    series: [*/
    /*      {*/
    /*        type: 'graph',*/
    /*        // layout: 'circular',*/
    /*        layout: 'circular',*/
    /*        symbol: 'rect',*/
    /*        symbolSize: [180, 80],*/
    /*        roam: true, //鼠标缩放功能*/
    /*        label: {*/
    /*          show: true, //是否显示标签*/
    /*          fontWeight: 'bold',*/
    /*          fontSize: 20*/
    /*        },*/
    /*        itemStyle: {*/
    /*          color: '#409EFF'*/
    /*        },*/
    /*        symbolOffset: [-40, -20],*/
    /*        focusNodeAdjacency: true, //鼠标移到节点上时突出显示结点以及邻节点和边*/
    /*        edgeSymbol: ["none", "arrow"], //关系两边的展现形式，也即图中线两端的展现形式。arrow为箭头*/
    /*        edgeSymbolSize: [4, 10],*/
    /*        draggable: false,*/
    /*        edgeLabel: {*/
    /*          normal: {*/
    /*            fontSize: 15,*/
    /*            show: true,*/
    /*            //通过回调函数设置连线上的标签*/
    //             formatter: function (x) {
    //               return x.data.text
    //             }
    //           }
    //         },
    //         data: this.node_data,
    //         links: this.link_data
    //       }
    //     ]
    //   }
    // }
  }
}
</script>

<style scoped>
.el-table--home {
  padding: 30px 50px;
  height: 100vh;
  box-sizing: border-box;
}
.el-table--fit {
  font-size: 16px;
}
</style>
