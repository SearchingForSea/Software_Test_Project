<template>
  <el-row class="tac">
    <el-col :span="9">
      <el-menu
          default-active="/home/basic-info"
          class="el-menu-vertical"
          @select="handleSelect"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b">
        <el-menu-item
            index="/home/basic-info"
            class="el-menu-item"
        >
          <template slot="title">
            <i class="el-icon-location"></i>
            <span>集群信息</span>
          </template>
        </el-menu-item>
        <el-menu-item
            index="/home/optimization"
            class="el-menu-item"
        >
          <i class="el-icon-menu"></i>
          <span slot="title">集群操作</span>
        </el-menu-item>
        <el-menu-item
            index="/home/resource"
            class="el-menu-item"
        >
          <i class="el-icon-s-tools"></i>
          <span slot="title">集群负载</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<script>
export default {
  name: "NavHome",
  created() {
    if (this.$route.path !== '/home/basic-info') {
      this.$router.push('/home/basic-info')
    }
  },
  methods: {
    handleSelect(key) {
      this.$router.push(key)
    }
  }
}
</script>

<style scoped>
.tac {
  width: 15vw;
  display: inline-block;
}
.el-menu-vertical {
  height: 100vh;
  width: 15vw;
}
.el-menu-item {
  height: 20vh;
  padding: 0 35px !important;
}
.el-menu-item span {
  font-size: 20px;
  line-height: 165px;
}
</style>
