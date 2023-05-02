<template>
  <div class="el-table--home">
    <el-table
        :data="tableData"
        class="el-table--fit"
    >
      <el-table-column
          prop="id"
          label="ID"
          width="50"
          class="table-column--item"
      />
      <el-table-column
          prop="index"
          label="集群名"
          width="240"
          class="table-column--item"
          :filters="indexSelect"
          :filter-method="es_name_filter"
      />
      <el-table-column
          prop="shard"
          label="分片编号"
          width="120"
          class="table-column--item"
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
      pageNum: 0,
      curPage: 0,
      dataLength: 0,
    }
  },
  watch: {
  },
  computed: {
    indexSelect() {
      let index_select = []
      let index_select_obj = []
      this.es_data.forEach((value) => {
        if (index_select.indexOf(value.index) === -1) {
          index_select.push(value.index)
          index_select_obj.push({
            text: value.index,
            value: value.index
          })
        }
      })
      return index_select_obj
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
  methods: {
    es_name_filter(value, row) {
      console.log(value, row)
    }
  }
}
</script>

<style scoped>
.el-table--home {
  padding: 50px 50px;
}
.el-table--fit {
  font-size: 16px;
}
.el-pag {
  text-align: center;
  margin-top: 25px;
  position: relative;
  left: -30px;
}
</style>
