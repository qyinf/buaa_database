<template>
  <div>
  <v-list>
    <v-row style="margin-left: 10px">
      <v-icon color="blue">mdi-bulletin-board</v-icon>
      <h1 style="margin-left: 10px;margin-top: 10px">
        {{ text }}</h1>
    </v-row>

    <div v-for="(food, index) in foods" :key="food.food_id">
    <v-list-item
    v-if="isVisible(index)"
        :key="food.food_id"
        style="margin-top: 20px; width: 400px; margin-left:20px; float: left"
    >
      <v-card
          class="mx-auto"
          style="min-width: 400px"
      >
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="headline">
                {{ food.name }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
         
        <v-img
            :src="food.picture"
            height="194"
        ></v-img>

        <div class="desBlock">
          价位：{{ food.price }}
        </div>
        <div>
          位置：{{ food.place}} / {{ food.floor }}
        </div>
        
        <v-card-actions>
          <v-btn
              text
              color="deep-purple accent-4"
              @click="food.show = true"
          >
          查看详情
          </v-btn>
          <v-spacer></v-spacer>

          <v-btn
              text
              color="deep-purple accent-4"
              @click.native="fooddelete(food)"
              v-show=isAdmin
          >
          删除
          </v-btn>
          <v-spacer></v-spacer>

          <v-btn icon :color="get_likecolor(food.userlike)" 
             @click="likeDish(food)" >
            <v-icon>mdi-thumb-up</v-icon>
          </v-btn>
          <div>{{ food.like }}</div>

          <v-btn icon :color="get_dislikecolor(food.userlike)"
          @click="dislikeDish(food)">
            <v-icon>mdi-thumb-down</v-icon>
          </v-btn>
          <div>
            {{ food.dislike }}
          </div>
        </v-card-actions>

        <v-dialog v-model="food.show">
          <v-card>
            <v-card-title>
              <span class="headline">
                {{ food.name }}
              </span>
            </v-card-title>
            <v-card-text style="margin-top: 20px">
              <pre>{{ food.intro }}</pre>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="green darken-1" text @click="food.show = false">关闭</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

      </v-card>
    </v-list-item>
  </div>
  </v-list>
  <div style="clear: both;"></div>
    <div style="align-items: center;">
      <button class="page_button" @click="prevPage">上一页</button>
      <button class="page_button" @click="nextPage">下一页</button>
    </div>
  </div>
</template>

<script>
import Qs from "qs";


export default {
  name: "FoodList",
  props: ['foods', 'text'],
  data:function() {
    return {
      isAdmin:false,
      rank: 1,
      num: 2
    }
  },
  mounted() {
    console.log(this.foods)
    this.getUserInformation();
  },
  methods:{
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
          if (res.data.user.level === 1) {
            this.isAdmin = true;
          } else this.isAdmin = false;
        } else this.$notify.error(res.data.message)
      }).catch((error)=>{
        console.log(error)
      })
    },
    nextPage() {
      let max = Math.ceil(this.foods.length / this.num); 
      if (this.rank + 1 <= max) {
        this.rank++;
        this.$forceUpdate();
      }
    },
    prevPage() {
      if (this.rank - 1 >= 1) {
        this.rank--;
        this.$forceUpdate();
      }
    },
    isVisible(idx) {
      let l = (this.rank - 1) * this.num + 1;
      let r = (this.rank) * this.num;
      idx = idx + 1;
      return l <= idx && idx <= r;
    },
    get_likecolor(status) {
      switch(status){
        case 0:
        case -1:  
          return '#838383';  // 灰色
        case 1:
          return '#e04189';  // 粉色
        default:
          break;  
      }
    },
    get_dislikecolor(status) {
      switch(status){
        case 0:
        case 1:  
          return '#838383';  // 灰色
        case -1:
          return '#4b5ca5';  // 浅蓝色
        default:
          break;  
      }
    },
    fooddelete(food){
      this.$axios.post(
      "http://127.0.0.1:8000/api/delete_food",
       Qs.stringify({
          food_id: food.food_id
       })
       ).then((res) => {
        if (res.code === 0) {  
          //
        } else this.$notify.error(res.message)
      }).catch((error) => {
        console.log(error)
      })
      this.$router.go(0);  
    },
    likeDish(food) {
      this.$axios.post(
          "http://127.0.0.1:8000/api/like_dish",
          Qs.stringify({
            user_id: localStorage.getItem('user_id'),
            food_id:food.food_id
          })
      ).then((res) => {
        if (res.data.code === 0) {  
          this.$refs.upload.clearFiles();
          
        } else this.$notify.error(res.data.message)
      }).catch((error) => {
        console.log(error)
      })
      this.$router.go(0)  
      //this.$router.replace({
      //          path: '/FoodListBack',
      //          name: 'FoodListBack'
      //})
      
    },
    dislikeDish(food) {
      this.$axios.post(
          "http://127.0.0.1:8000/api/dislike_dish ",
          Qs.stringify({
            user_id: localStorage.getItem('user_id'),
            food_id: food.food_id,
          })
      ).then((res) => {
        if (res.data.code === 0) {
          //food.like = res.data.like;
          //food.dislike = res.data.dislike;
          this.$refs.upload.clearFiles();
        } else this.$notify.error(res.data.message)
      }).catch((error) => {
        console.log(error)
      })
      this.$router.go(0)
    }
  },
}
</script>

<style scoped>
pre {
  tab-size: 2;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.desBlock {
  margin-top: 30px;
}

.page_button {
  background-color: aqua;
  border-radius: 4px;
  margin-top: 10px;
  margin-left: 10px;
}
</style>
