<template>
  <div class="main-box">
    <div class="container" v-show = true>
      <el-form :rules="rules" :model="createClubForm">
        <h2 class="title">请输入您的晚餐需求⌯'▾'⌯</h2>

        <el-form-item prop="dietCalorie">
          <el-input v-model="request.calorie"
            class="form__input"
            type="text"
            placeholder="目标卡路里(晚餐的建议在300大卡左右~)"/>
        </el-form-item>


        <el-form-item prop="type">
            <el-select v-model="request.place"
            class="form__input"
            placeholder="请选择食物地点"  @change="$forceUpdate()"
                        style="display: block;">
              
              <el-option v-for="item in canteen" :key="item.id" :label="item.name" :value="item.name"></el-option>
              
            </el-select>
          </el-form-item>

        <el-form-item prop="choice">
          <el-select v-model="request.taste"
                  class="form__input"
                  placeholder="口味选择!"
                  style="display: block;">
            <el-option label="无辣不欢!" value="1"></el-option>
            <el-option label="滴辣不沾!" value="2"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item prop="floor">
          <el-input v-model="request.floor"
              class="form__input"
              type="text"
              placeholder="楼层"/>
        </el-form-item>

        <el-form-item prop="budget">
          <el-input v-model="request.budget"
              class="form__input"
              type="text"
              placeholder="本餐预算"/>
        </el-form-item>

        <el-form-item>
          <div class="primary-btn"
            @click="create"
            v-show="onCreate">点击生成!
          </div>
        </el-form-item>
      </el-form>


      <el-main class="el-main-table">
        <el-descriptions class="margin-top" :column="1" border>
          <el-descriptions-item>
             <template slot="label">
                  <i class="el-icon-food"></i>
                  餐品1
                </template>
                {{ this.result.dish1 }}
                {{ this.result.price1 }}
                {{ this.result.calorie1 }}
              </el-descriptions-item>
        </el-descriptions>

        <el-descriptions class="margin-top" :column="1" border>
          <el-descriptions-item>
             <template slot="label">
                  <i class="el-icon-food"></i>
                  餐品2
                </template>
                {{ this.result.dish2 }}
                {{ this.result.price2 }}
                {{ this.result.calorie2 }}
              </el-descriptions-item>
        </el-descriptions>

        <el-descriptions class="margin-top" :column="1" border>
          <el-descriptions-item>
             <template slot="label">
                  <i class="el-icon-food"></i>
                  餐品3
                </template>
                {{ this.result.dish3 }}
                {{ this.result.price3 }}
                {{ this.result.calorie3 }}
              </el-descriptions-item>
        </el-descriptions>
      </el-main>
    </div>



      
  </div>
</template>
<script>

import Qs from "qs";

export default {
  name: "FindClub2",
  props: ['onCreate'],
  data() {
    return {
      user_id: localStorage.getItem('user_id'),
      canteen:[],
      createClubForm: {
        imageUrl: '',
        welcomeImage: '',
        clubName: '',
        clubType: '',
        introduction: '',
        welcome: '',
      },
      request: {
        calorie: '',
        place: '',
        taste: '',
        budget: '',
      },
      result :{
        dish1: '',
        price1: '',
        calorie1: '',
        dish2: '',
        price2: '',
        calorie2: '',
        dish3: '',
        price3: '',
        calorie3: '',
      },

      rules: {
        dietCalorie: [{required: true, message: '请输入目标卡路里', trigger: 'blur'}],
        type: [{required: true, message: '请选择用餐地点', trigger: 'blur'}],
        choice: [{required: true, message: '请选择你的口味', trigger: 'blur'}],
        budget: [{required: true, message: '请输入目标预算', trigger: 'blur'}],
        floor: [{required: true, message: '楼层', trigger: 'blur'}]
      }
    }
  },
  mounted() {
      this.getCanteen()
  },
  methods: {
    getCanteen:function() {
        //let con = {}
        this.$axios({
          url: 'http://127.0.0.1:8000/api/find_canteen_list',
          method: 'post',
          //data:Qs.stringify(con),
        }).then((ret) => {
          if(ret.data.code === 0) {
            this.canteen = ret.data.data;
            console.log(this.canteen);
          } 
          else this.$notify.error(ret.data.message + "，无法找到餐厅呱");
        })

      },
    create() {
      let con = {};
      con['calorie'] = this.request.calorie;
      con['place'] = this.request.place;
      con['taste'] = this.request.taste;
      con['budget'] = this.request.budget;
      con['floor'] = this.request.floor;
      con['jwt'] = {
        'code': localStorage.getItem('code'),
        'user_id': localStorage.getItem('user_id'),
        'time': localStorage.getItem('time')
      };
      this.$axios({
        url: 'http://127.0.0.1:8000/api/prepare_meal',
        method: 'post',
        key:'3', //代表是早餐
        data: Qs.stringify(con),
      }).then((ret) => {
        if (ret.data.code === 0) {
          this.result.dish1 = ret.data.dish1;
          this.result.dish2 = ret.data.dish2;
          this.result.dish3 = ret.data.dish3;
          this.result.price1 = ret.data.price1;
          this.result.price2 = ret.data.price2;
          this.result.price3 = ret.data.price3;
          this.result.calorie1 = ret.data.calorie1;
          this.result.calorie2 = ret.data.calorie2;
          this.result.calorie3 = ret.data.calorie3;
          this.$message.success("您的晚餐已经备好^v^");
          this.$refs.upload.clearFiles();
          this.request.calorie = '';
          this.request.budget = '';
          this.request.place = '';
          this.request.taste = '';
          
        }
        else this.$notify.error(ret.data.message + "，生成失败");
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.pic {
  float: left;
  min-width: 500px;
  max-height: 148px;

}

.el-form-item__content {
  max-height: 148px;
}

.main-box {
  position: center;
  width: 100%;
  min-width: 1000px;
  min-height: 300px;
  height: 700px;
  background-color: #ecf0f3;
  box-shadow: 10px 10px 10px #c3d5f3, -10px -10px 10px #f9f9f9;
  border-radius: 12px;
  overflow: hidden;

  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: center;
    width: 100%;
    height: 100%;
    background-color: #ecf0f3;

    form {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      width: 100%;
      height: 100%;
      color: #ecf0f3;

      .title {
        font-size: 34px;
        font-weight: 700;
        line-height: 3;
        color: #181818;
      }

      .text {
        margin-top: 30px;
        margin-bottom: 12px;
      }

      .form__input {
        width: 700px;
        height: 40px;
        margin: 4px 0;
        padding-left: 25px;
        font-size: 13px;
        letter-spacing: 0.15px;
        border: none;
        outline: none;
        // font-family: 'Montserrat', sans-serif;
        background-color: #ecf0f3;
        transition: 0.25s ease;
        border-radius: 8px;
        box-shadow: inset 2px 2px 4px #d1d9e6, inset -2px -2px 4px #f9f9f9;

        &::placeholder {
          color: #a0a5a8;
        }
      }
    }
  }
}

::v-deep .el-input__inner {
  background-color: #ecf0f3 !important;
  border: none 0 !important;
  padding-left: 0 !important;
  height: 30px !important;
  line-height: 30px !important;
}

.primary-btn {
  transition: all 0.3s;
  width: 180px;
  height: 50px;
  border-radius: 25px;
  margin-top: 25px;
  text-align: center;
  line-height: 50px;
  font-size: 14px;
  letter-spacing: 2px;
  background-color: #4b70e2;
  color: #f9f9f9;
  cursor: pointer;
  box-shadow: 8px 8px 16px #d1d9e6, -8px -8px 16px #f9f9f9;

  &:hover {
    box-shadow: 4px 4px 6px 0 rgb(255 255 255 / 50%),
    -4px -4px 6px 0 rgb(116 125 136 / 50%),
    inset -4px -4px 6px 0 rgb(255 255 255 / 20%),
    inset 4px 4px 6px 0 rgb(0 0 0 / 40%);
  }
}

.avatar {
  margin-top: 10px;
  height: 150px;
  width: 150px;
}

.el-upload-dragger {
  height: 250px;
  width: 250px;
}

.el-main-table {
  width: 50%;
  align-self: center;
}
</style>
