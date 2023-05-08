<template>
  <div class="resource_manage">
    <div class="el-table--home">
      <h3>平均利用率: {{ (100 * avg_index).toFixed(2) }}%</h3>
      <el-table
          :data="bm_data"
          class="el-table--fit"
          stripe
          :default-sort = "{prop: 'name', order: 'ascending'}"
          :cell-style="styleBack"
          @sort-change="onNameSortChange"
          @row-click="handleRowClick"
      >
        <el-table-column
            label="ID"
            width="40"
            type="index"
            class="table-column--item"
        />
        <el-table-column
            prop="name"
            label="物理机名"
            width="108"
            sortable="custom"
            align="center"
            class="table-column--item"
        />
        <el-table-column
            prop="store"
            label="存储(G)"
            width="108"
            sortable
            align="center"
            class="table-column--item"
        />
        <el-table-column
            prop="cpu_num"
            label="cpu数量(个)"
            width="135"
            sortable
            align="center"
            class="table-column--item"
        />
        <el-table-column
            prop="memory"
            label="内存(M)"
            width="110"
            sortable
            align="center"
            class="table-column--item"
        />
        <el-table-column
            prop="avg_rate"
            label="利用率(%)"
            width="120"
            sortable
            align="center"
            class="table-column--item"
        />
      </el-table>
    </div>
    <div class="display-page">
      <el-empty
          v-if="!displayData"
          description="暂未选中某物理机"
          class="empty-data"
      />
      <data-panel
          v-else
          :bm_data="displayData"
      />
    </div>
  </div>
</template>

<script>
import DataPanel from "@/components/DataPanel";
export default {
  name: "ResourceManage",
  components: {
    DataPanel
  },
  computed: {
  },
  created() {
    this.$https.get('http://127.0.0.1:8000/api/manage_resource').then((response) => {
      this.avg_index = response.data.avg_rate
      this.bm_data = response.data.return_bm_data
      if (typeof this.bm_data === 'object') {
        this.bm_data.forEach((item, index, arr) => {
          arr[index].avg_rate = parseFloat((100 - arr[index].avg_rate * 100).toFixed(2))
        })
        this.bm_data.sort((a, b) => parseInt(a.name.slice(3)) - parseInt(b.name.slice(3)))
      } else {
        alert(this.bm_data)
      }
    })
  },
  data() {
    return {
      bm_data: null,
      displayData: null,
      avg_index: 0
    }
  },
  methods: {
    handleRowClick(row) {
      this.displayData = row
    },
    onNameSortChange({ prop, order }) {
      if (prop === 'name') {
        if (order === 'ascending') {
          this.bm_data.sort((a, b) => parseInt(a.name.slice(3)) - parseInt(b.name.slice(3)))
        } else {
          this.bm_data.sort((a, b) => parseInt(b.name.slice(3)) - parseInt(a.name.slice(3)))
        }
      }
    },
    styleBack({ row }) {
      if (row.avg_rate === 0) {
        return { backgroundColor: "rgba(33,236,65,0.61)" }
      } else if (row.avg_rate > 90) {
        return {
          backgroundColor: "rgba(234,7,7,0.69)",
          color: 'white'
        }
      } else {
        return {
          backgroundColor: "rgba(243,191,22,0.69)",
          color: 'white'
        }
      }
    }
  }
}
</script>

<style scoped>
.resource_manage {
  display: flex;
  width: 100vw;
}
.el-table--home {
  height: 100vh;
  width: 40vw;
  box-sizing: border-box;
  overflow-y: scroll;
  padding: 20px 20px;
}
.el-table--fit {
  font-size: 16px;
}
.el-table--fit:hover {
  cursor: pointer;
}
.display-page {
  height: 96vh;
  width: 41vw;
  margin: 0 2vw;
  /*background-color: lightgray;*/
  border-radius: 20px;
  padding: 30px 0;
  box-sizing: border-box;
}
.empty-data {
  margin-top: 200px;
}
</style>
