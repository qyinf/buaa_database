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
        <el-row :gutter="20" type="flex" class="row-bg" justify="center" align="middle">
          <el-col :span="12">
              <el-carousel trigger="click">
                <el-carousel-item>
                  <img src="../assets/png/loop-1.jpg" class="img-object1">
                </el-carousel-item>
                <el-carousel-item>
                  <img src="../assets/png/loop-2.jpg" class="img-object1">
                </el-carousel-item>
                <el-carousel-item>
                  <img src="../assets/png/loop-3.jpg" class="img-object1">
                </el-carousel-item>
              </el-carousel>
          </el-col>
          <el-col :span="6">
              <img src="../assets/png/user-1.jpg" class="img-object1">
          </el-col>
        </el-row>
        <el-row :gutter="20" type="flex" class="row-bg" justify="center" align="middle">
          <el-col :span="6">
            <img src="../assets/png/team-1.jpg" class="img-object2">
          </el-col>
          <el-col :span="6">
            <img src="../assets/png/moun-3.jpg" class="img-object2">
          </el-col>
          <el-col :span="6">
            <img src="../assets/png/mem-1.jpg" class="img-object2">
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import SideBar from "@/components/SideBar";
import MyHeader from "@/components/MyHeader";

export default {
  name: 'MainPage',
  components: {MyHeader, SideBar},
}
</script>

<style scoped>
.img-object1 {
  height: 100%;
  min-height: 300px;
  width: 100%;
  object-fit: cover;
  /*object-position: 50% 20%;*/
}

.img-object2 {
  height: 100%;
  min-height: 200px;
  width: 100%;
  object-fit: cover;
  /*object-position: 50% 20%;*/
}

.el-col {
  border-radius: 4px;
}

.bg-purple-dark {
  background: #99a9bf;
}

.bg-purple {
  background: #d3dce6;
}

.bg-purple-light {
  background: #e5e9f2;
}

.grid-content1 {
  border-radius: 4px;
  min-height: 250px;
}

.grid-content2 {
  border-radius: 4px;
  min-height: 200px;
}

.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}

.side-bar {
  width: 65px;
  transition:width 1s;
  -moz-transition:width 1s;
  -webkit-transition:width 1s;
  -o-transition:width 1s;
}

.side-bar:hover{
  width: 150px;
}
</style>