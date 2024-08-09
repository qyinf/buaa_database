<template>
  <div style="height: 800px;">
    <div class="tools">
      <div class="search-box">
        <el-input v-model="searchCanteenName"
        placeholder="输入食堂名称(新北食堂,合一食堂或者学二食堂)"
        clearable size="mini"/>
      </div>


      <div class="search-box">
        <el-input v-model="floor"
        placeholder="请输入食物所在的食堂楼层(1-4)"
        clearable size="mini"/>
      </div>




      <el-button slot="append"  
        icon="el-icon-search"
        id="search"
        @click="search">
      </el-button>
      

    <div class="dropdownSort-box">
        <el-dropdown placement="bottom"
          trigger="click"
          @command="handleSort">
          <span style="
          cursor: pointer;
          color: dodgerblue">
            {{ sortType }}
          <i class="el-icon-arrow-down el-icon--right"/></span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="priceDown">按价格降序</el-dropdown-item>
            <el-dropdown-item command="priceUp">按价格升序</el-dropdown-item>
            <el-dropdown-item command="priceNot">-</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <!-- 这个组件的使用不一定是对的
        <v-btn @click="getPdf('#'+'mychart', '食堂饭菜')"
                  v-show="charts"
                  color="blue lighten-3"
                     style="margin-left: 10px">导出食堂饭菜PDF
        </v-btn> -->
        <button @click="getPdf('#'+'mychart', '食堂饭菜')"
         style="margin-left: 10px; color:darkorange;">
          导出为pdf
        </button>
      </div>
    </div>
    <v-app id="mychart">
        <FoodList :foods ="selectedList" text="查看饭菜"></FoodList>
    </v-app>
  </div>
</template>

<script>

import Qs from "qs";
import FoodList from "@/components/FoodList";

export default {
  name: "FindFood-1",
  // todo
  components: {FoodList},
  // components: {foodList},
  data(){
    return{
      searchCanteenName: '',
      sortType:'按价格排序',
      floor: '',
      //foodList: [],
      realList: [],
      selectedList: [],
    }
  },
  methods:{
    initdata(){
      this.$axios.post(
          "http://127.0.0.1:8000/api/find_food",
          Qs.stringify({
            user_id: localStorage.getItem('user_id'),
          })
      ).then((res)=>{
        if(res.data.code===0){
          console.log(res.data.food_list)
          this.selectedList = res.data.food_list;
          this.realList = res.data.food_list;
          //然后挑选对应的层数
        }
        else this.$notify.error(res.data.message)
      }).catch((error)=>{
        console.log(error)
      })
    },
    search() {
      this.selectedList = this.realList;
      this.selectCanteen();
      this.selectFloor();
    },
    handleSort(command){
      switch (command){
        case 'priceDown':
          this.sortType = '按价格降序';
          break;
        case 'priceUp':
          this.sortType = '按价格升序';
          break;
        case 'priceNot':
          this.sortType = '按价格排序';
      }
      this.sortFood()
    },
    sortCmp(itemA, itemB){
      switch (this.sortType){
        case '按价格降序':
          return itemA.price < itemB.price;
        case '按价格升序':
          return itemA.price > itemB.price;
      }
    },
    sortFood(){
      let sortList = []
      for (let i = 0;i < this.selectedList.length;i++){
        sortList[i] = this.selectedList[i]
      }
      for(let i = 0; i < sortList.length; i++){
        for(let j = i+1; j < sortList.length; j++){
          if(this.sortCmp(sortList[i],sortList[j])){
            let tmp = sortList[j];
            sortList[j] = sortList[i];
            sortList[i] = tmp;
          }
        }
      }
      this.selectedList = sortList;
    },
    selectCanteen() {
      let tmpList = [];
      if (this.searchCanteenName == '') {
          tmpList = this.selectedList;
      }
      else {
          let j = 0;
          for(let i = 0; i < this.selectedList.length; i++){
            if (this.selectedList[i].place === this.searchCanteenName){
              tmpList[j++] = this.selectedList[i];
            }
          }
        }
      this.selectedList = tmpList;
    },
    selectFloor(){
      let tmpList = [];
      if (this.floor == '') {
          tmpList = this.selectedList;
      }
      else {
          let j = 0;
          for(let i = 0; i < this.selectedList.length; i++){
            if (this.selectedList[i].floor === parseInt(this.floor)){
              tmpList[j++] = this.selectedList[i];
            }
          }
        }
      this.selectedList = tmpList;
    },
  },
  mounted() {
    this.initdata();
  }
}
</script>

<style scoped>
.tools{
  height: 30px;
  width: 1200px;
  display: flex;
}
.search-box{
  width: 420px;
  margin-right: 20px;
}
.dropdownSort-box{
  width: 250px;
}
.dropdownType-box{
  width: 90px;
  margin-right: 30px;
}
.dropdownLevel-box{
 width: 90px;
 margin-right: 30px;
}
.clubBar{
  width: 650px;
  float: left;
  height: 200px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  margin-right: 20px;
  margin-bottom: 20px;
}
.club_picture{
  margin-left: 10px;
  width: 200px;
  height: 200px;
  float: left;
  margin-right: 30px;
}
.club_name{
  font-size: 50px;
  width: 410px;
  float: left;
  margin-top: 10px;
  margin-bottom: 10px;
}
.club_info{
  float: left;
  width: 410px;
  margin-bottom: 10px;
}
.club_dis{
  word-wrap: break-word;
  display: inline;
}
</style>
