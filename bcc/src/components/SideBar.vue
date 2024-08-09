<template>
  <div @mouseover="mouseOver"
       @mouseleave="mouseLeave"
       class="showHide">
    <el-menu :default-active="this.$router.path"
             router
             class="el-menu-vertical-demo"
             :collapse="isCollapse"
             :collapse-transition="false"
    >
      <el-menu-item index="/mainpage" router>
        <i class="el-icon-video-camera"></i>
        <span slot="title">北航食堂概览</span>
      </el-menu-item>


      <el-menu-item index="/searchFood" router>
        <i class="el-icon-search"></i>
        <span slot="title">搜索食物</span>
      </el-menu-item>

      
      <el-submenu index="/mydiet">
        <template slot="title">
          <i class="el-icon-place"></i>
          <span slot="title">我的三餐</span>
        </template>
        <el-menu-item v-for="diet in myDiet"
        :key="diet.id"
        :index="`/mydiet${diet.id}/${diet.name}`" router>
          {{diet.name}}
        </el-menu-item>
      </el-submenu>

      <el-menu-item :index="`/usercenter/${this.user.user_id}/${this.user.real_name}`">
        <i class="el-icon-user-solid"></i>
        <span slot="title">个人中心</span>
      </el-menu-item>

      <el-menu-item index="/addpage" router v-show=isAdmin>
        <i class="el-icon-s-order"></i>
        <span slot="title">添加食物</span>
      </el-menu-item>

      <el-menu-item index="/AddCanteen" router v-show=isAdmin>
        <i class="el-icon-s-order"></i>
        <span slot="title">添加餐厅</span>
      </el-menu-item>

    </el-menu>
  </div>
</template>

<script>


import Qs from "qs";

export default {
  name: "SideBar",
  data() {
    return {
      isAdmin:false,
      hasClub: false,
      isCollapse: true,
      user: {},
      user_id: "21373090",
      user_name: "柒羽",
      myDiet: [{
        id: 1,
        name: "早饭"
      }, {
        id: 2,
        name: "午饭"
      }, {
        id: 3,
        name: "晚饭"
      }]
    };
  },
  methods: {
    getUserInformation(){
      console.log("local storage user id=", localStorage.getItem("user_id"));
      this.$axios.post(
          "http://127.0.0.1:8000/api/get_user_information",
          Qs.stringify({
            'user_id':localStorage.getItem('user_id')
          })
      ).then((res)=>{
        if(res.data.code===0){
          console.log(res.data)
          this.user = res.data.user
          if (parseInt(res.data.user.level) === 1) {
            this.isAdmin = true;
          } else this.isAdmin = false;
          
        } else this.$notify.error(res.data.message)
      }).catch((error)=>{
        console.log(error)
      })
    },
    mouseOver() {
      this.isCollapse = false
    },
    mouseLeave() {
      this.isCollapse = true
    }
  },
  created() {
    this.getUserInformation();
  }
}
</script>
<style>
.hid{
  display: none;
}
</style>
