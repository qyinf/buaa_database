<template>
    <div class="main-box">
      <div class="container">
        <el-form :rules="createFoodRules" :model="createFoodForm">
          <h2 class="title">食物基本信息</h2>
          <h3 style="margin-bottom: 20px;color: #4b70e2;float: left">请上传食物图片</h3>
          <el-form-item>
            <el-upload
                :auto-upload="true"
                :before-upload="beforeAvatarUpload"
                :on-success="handleAvatarSuccess"
                :limit=1
                multiple
                accept=".png,.jpg,.jepg"
                action="http://127.0.0.1:8000/upload/img"
                list-type="picture-card"
                ref="upload"
                style="margin-bottom: 20px">
              <i slot="default" class="el-icon-plus"></i>
              <div slot="file" slot-scope="{file}">
                <img
                    class="el-upload-list__item-thumbnail"
                    :src="file.url" alt=""
                >
                <span class="el-upload-list__item-actions">
                      <span
                          class="el-upload-list__item-preview"
                          @click="handlePictureCardPreview(file)"
                      >
                        <i class="el-icon-zoom-in"></i>
                      </span>
                      <span
                          v-if="!disabled"
                          class="el-upload-list__item-delete"
                          @click="handleRemove(file)"
                      >
                        <i class="el-icon-delete"></i>
                        </span>
                    </span>
              </div>
            </el-upload>
            <el-dialog :visible.sync="dialogVisible">
              <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog>
          </el-form-item>
          
          <el-form-item prop="foodName">
            <el-input v-model="createFoodForm.foodName"
              class="form__input"
              type="text"
              placeholder="食物名称"/>
          </el-form-item>

          <el-form-item prop="foodCalorie">
            <el-input v-model="createFoodForm.foodCalorie"
              class="form__input"
              type="text"
              placeholder="食物卡路里"/>
          </el-form-item>

          <el-form-item prop="foodPrice">
            <el-input v-model="createFoodForm.foodPrice"
            class="form__input"
            type="text"
            placeholder="食物价格"/>
          </el-form-item>

          <el-form-item prop="foodPlace">
            <el-select v-model="createFoodForm.foodPlace"
            class="form__input"
            placeholder="请选择食物地点"  @change="$forceUpdate()"
                        style="display: block;">
              
              <el-option v-for="item in canteen" :key="item.id" :label="item.name" :value="item.name"></el-option>
              
            </el-select>
          </el-form-item>

          <el-form-item prop="foodFloor">
            <el-input v-model="createFoodForm.foodFloor"
            class="form__input"
            type = "text"
            placeholder="食堂层数"/>
          </el-form-item>


          <el-form-item prop="isSpicy">
            <el-select v-model="createFoodForm.isSpicy"
            class="form__input"
            placeholder="请选择食物口味"
                       style="display: block;">
              <el-option label="辣" value="1"></el-option>
              <el-option label="不辣" value="2"></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item prop="introduction">
            <el-input v-model="createFoodForm.introduction"
              class="form__input"
              type="text"
              placeholder="食物简介"/>
          </el-form-item>
          <el-form-item>
            <div class="primary-btn" @click="create" v-show="onCreate">立即添加</div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </template>
  
  <script>
  
  import Qs from "qs";
  
  export default {
    
    name: "AddFood",
    props: ['onCreate'],
    data() {
      return {
        canteen:[],
        dialogImageUrl: '',
        dialogVisible: false,
        disabled: false,
        user_id: localStorage.getItem('user_id'),
        createFoodForm: {
          imageUrl: '',
          welcomeImage: '',
          foodName: '',
          foodCalorie: '',
          foodPlace: '',
          foodFloor: '',
          foodPrice:'',
          introduction: '',
          isSpicy:''
        },
        createFoodRules: {
          foodName: [{required: true, message: '请输入食物名称', trigger: 'blur'}],
          foodCalorie: [{required: true, message: '请输入食物卡路里', trigger: 'blur'}],
          foodPlace: [{required: true, message: '请选择食物地点', trigger: 'blur'}],
          foodFloor: [{required: true, message: '请输入食物层数', trigger: 'blur'}],
          foodPrice: [{required: true, message: '请输入食物价格', trigger: 'blur'}],
          introduction: [{required: true, message: '请输入食物简介', trigger: 'blur'}],
          isSpicy: [{required: true, message: '请选择食物口味', trigger: 'blur'}],
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
      create: function () {
        let con = {};
        con['image_url'] = this.createFoodForm.imageUrl;
        con['name'] = this.createFoodForm.foodName;
        con['calorie'] = this.createFoodForm.foodCalorie;
        con['floor'] = this.createFoodForm.foodFloor;
        con['place'] = this.createFoodForm.foodPlace;
        con['price'] = this.createFoodForm.foodPrice;
        con['intro'] = this.createFoodForm.introduction;
        con['taste'] = this.createFoodForm.isSpicy;
        this.$axios({
          url: 'http://127.0.0.1:8000/api/add_dish',
          method: 'post',
          data: Qs.stringify(con),
        }).then((ret) => {
          if (ret.data.code === 0) {
            this.$message.success("食品信息添加成功");
            //this.$refs.upload.clearFiles();
            this.createFoodForm.imageUrl = '';
            this.createFoodForm.foodName = '';
            this.createFoodForm.foodPlace = '';
            this.createFoodForm.foodFloor = '';
            this.createFoodForm.introduction = '';
            this.createFoodForm.foodPrice = '';
            this.createFoodForm.foodCalorie = '';
            this.createFoodForm.isSpicy = '';
            this.$refs.upload.clearFiles();
          }
            else this.$notify.error(ret.data.message + "，添加失败");
        })
      },
      beforeAvatarUpload(file) {
        console.log(file);
        return true;
      },
      //清除图片缓存
      handleRemove(file) {
        console.log(file)
        this.$refs.upload.clearFiles();
      },
      //展示图片预览图
      handlePictureCardPreview(file) {
        this.dialogImageUrl = file.url;
        this.dialogVisible = true;
      },
      handleAvatarSuccess(res) {
        if (res.code !== 0) {
          this.$message.error(res.message)
          return false
        }
        if (this.createFoodForm.imageUrl === '')
            this.createFoodForm.imageUrl = res.image_path
        this.$message.success('上传成功')
      },
      
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
    min-height: 500px;
    height: 1000px;
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
  </style>
  