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
          <GenerateDiet on-create="true"></GenerateDiet>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import GenerateDiet from "@/components/GenerateDiet.vue";
import MyHeader from "@/components/MyHeader";
import SideBar from "@/components/SideBar";

export default {
  name: "FindClub",
  components: {GenerateDiet,MyHeader, SideBar},
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