<template>
  <div class="graph-chart">
    <div
        ref="echarts_dom"
        class="main-chart"
    />
    <el-card class="box-card">
      <div
          slot="header"
          class="clearfix"
      >
        <span>{{ bm_data.name }}</span>
      </div>
      <div>
        <span class="message-title">存储信息:  </span>
        <span class="card-message"> {{ 12516 - this.bm_data.store}}G </span>已使用 (剩余<span class="card-message"> {{ this.bm_data.store }}G </span>); 占单机总量的 <span class="card-message">{{ (100 - this.bm_data.store_rate * 100).toFixed(2) }}% </span>
      </div>
      <div>
        <span class="message-title">CPU信息:  </span>
        <span class="card-message"> {{ 120 - this.bm_data.cpu_num}}个 </span>已使用 (剩余<span class="card-message"> {{ this.bm_data.cpu_num }}个 </span>); 占单机总量的 <span class="card-message">{{ (100 - this.bm_data.cpu_rate * 100).toFixed(2) }}% </span>
      </div>
      <div>
        <span class="message-title">内存信息:  </span>
        <span class="card-message"> {{ 512*1024 - this.bm_data.memory}}M </span>已使用 (剩余<span class="card-message"> {{ this.bm_data.memory }}M </span>); 占单机总量的 <span class="card-message">{{ (100 - this.bm_data.memory_rate * 100).toFixed(2) }}% </span>
      </div>
      <div>
        <span class="message-title">平均使用率:  </span>
        <span class="card-message"> {{ (bm_data.avg_rate * 100).toFixed(2) }}% </span>
      </div>
      <div>
        <span class="message-title">包含的虚拟机:  </span>
        <span class="card-message"> {{ get_vm }} </span>
      </div>
    </el-card>
  </div>
</template>

<script>
import echarts from "echarts";
export default {
  name: "DataPanel",
  props: {
    bm_data: Object,
  },
  computed: {
    get_vm() {
      let return_vm_text = ''
      let len = this.bm_data.stored_vm.length
      this.bm_data.stored_vm.forEach((item, index) => {
        return_vm_text += item
        if(index !== len-1) return_vm_text += ', '
      })
      return return_vm_text
    }
  },
  watch: {
    bm_data: {
      handler(newValue) {
        this.chart_pie_data.length = 0
        this.chart_pie_data.push([{
          name: '已使用', value: (1 - newValue.store_rate)
        },{
          name: '未使用', value: newValue.store_rate
        }])
        this.chart_pie_data.push([{
          name: '已使用', value: (1 - newValue.cpu_rate)
        },{
          name: '未使用', value: newValue.cpu_rate
        }])
        this.chart_pie_data.push([{
          name: '已使用', value: (1 - newValue.memory_rate)
        },{
          name: '未使用', value: newValue.memory_rate
        }])
        this.initChart()
      }
    }
  },
  data() {
    return {
      chart_pie_data: []
    }
  },
  created() {
    this.chart_pie_data.push([{
      name: '已使用', value: (1 - this.bm_data.store_rate)
    },{
      name: '未使用', value: this.bm_data.store_rate
    }])
    this.chart_pie_data.push([{
      name: '已使用', value: (1 - this.bm_data.cpu_rate)
    },{
      name: '未使用', value: this.bm_data.cpu_rate
    }])
    this.chart_pie_data.push([{
      name: '已使用', value: (1 - this.bm_data.memory_rate)
    },{
      name: '未使用', value: this.bm_data.memory_rate
    }])
  },
  mounted() {
    this.initChart()
  },
  methods: {
    initChart() {
      let myChart = echarts.init(this.$refs.echarts_dom)
      myChart.setOption(this.setOption())
      myChart.resize() // 自适应大小
    },
    setOption() {
      return {
        title: {
          // 设置饼图标题，位置设为顶部居中
          text: `${this.bm_data.name} 资源使用情况`,
          top: "2%",
          left: "center"
        },
        label: {
          show: false,
          position: 'center',
          formatter: '{a}: {b}'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        avoidLabelOverlap: false,
        series: [
          {
            type: 'pie', // 第一个饼图的 type 属性
            data: this.chart_pie_data[0],
            center: ['22%', '70%'],
            radius: ['20%', '40%'],
            name: '存储情况'
          },
          {
            type: 'pie', // 第二个饼图的 type 属性
            data: this.chart_pie_data[1],
            center: ['47%', '38%'],
            radius: ['20%', '40%'],
            name: 'CPU 情况'
          },
          {
            type: 'pie', // 第二个饼图的 type 属性
            data: this.chart_pie_data[2],
            center: ['80%', '70%'],
            radius: ['20%', '40%'],
            name: '内存情况'
          }
        ]
      }
    }
  }
}
</script>

<style scoped>
.main-chart {
  height: 45vh;
  width: 100%;
  border-radius: 30px;
  background-color: rgba(0, 0, 0, 0.03);
}
.box-card {
  width: 100%;
  margin-top: 5vh;
  height: 40vh;
  border-radius: 30px;
}
.box-card div {
  margin-bottom: 10px;
}
.clearfix span {
  font-weight: bold;
  font-size: 20px;
}
.card-message {
  font-weight: bolder;
  font-size: 16px;
}
.message-title {
  font-weight: normal;
  font-size: 18px;
  margin-right: 5px;
}
</style>
