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
          <AddFood onCreate = true></AddFood>
        </el-main>
      </el-container>
    </el-container>
  </template>
  
  <script>
  import AddFood from "@/components/AddFood";
  import MyHeader from "@/components/MyHeader";
  import SideBar from "@/components/SideBar";
  
  export default {
    name: "AddPage",
    components: {AddFood, MyHeader, SideBar},
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