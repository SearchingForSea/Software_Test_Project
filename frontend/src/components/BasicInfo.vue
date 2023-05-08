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
      console.log(response.data)
      response.data.forEach((value) => {
        this.es_data.push(value)
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
    }
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
