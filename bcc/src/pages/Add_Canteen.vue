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
          <AddCanteen onCreate = true></AddCanteen>
        </el-main>
      </el-container>
    </el-container>
  </template>
  
  <script>
  import AddCanteen from "@/components/AddCanteen";
  import MyHeader from "@/components/MyHeader";
  import SideBar from "@/components/SideBar";
  
  export default {
    name: "Add_Canteen",
    components: {AddCanteen, MyHeader, SideBar},
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