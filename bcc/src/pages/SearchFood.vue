<template>
  <el-container>
    <div class="side-bar">
      <SideBar></SideBar>
    </div>
    <el-container>
      <el-header>
        <MyHeader></MyHeader>
      </el-header>
      <el-main>
        <el-tabs v-model="activeName">
          <el-tab-pane label="食堂检索" name="first">
            <find-food1></find-food1>
          </el-tab-pane>
          <el-tab-pane label="数据导出" name="third">
            <ExportData></ExportData>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import FindFood1 from "@/components/FindFood1";
import ExportData from "@/components/ExportData.vue";
import MyHeader from "@/components/MyHeader";
import SideBar from "@/components/SideBar";

export default {
  name: "FindFood",
  components: {FindFood1, MyHeader, SideBar,ExportData},
  data() {
    return {
      activeName: "first"
    }
  }
}
</script>

<style scoped>
.side-bar {
  width: 65px;
  transition: width 0.5s;
  -moz-transition: width 0.5s;
  -webkit-transition: width 0.5s;
  -o-transition: width 0.5s;
}

.side-bar:hover {
  width: 150px;
}
</style>