<template>
    <div class="main-box">
      <div class="container">
        <el-form :rules="createFoodRules" :model="createFoodForm">
          <h2 class="title">食堂基本信息</h2>
          
          <el-form-item prop="Name">
            <el-input v-model="createFoodForm.Name"
              class="form__input"
              type="text"
              placeholder="食堂名称"/>
          </el-form-item>

          <el-form-item prop="Floor">
            <el-input v-model="createFoodForm.Floor"
            class="form__input"
            type = "text"
            placeholder="食堂层数"/>
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
    
    name: "AddCanteen",
    props: ['onCreate'],
    data() {
      return {
        dialogImageUrl: '',
        dialogVisible: false,
        disabled: false,
        user_id: localStorage.getItem('user_id'),
        createFoodForm: {
          welcomeImage: '',
          Name: '',
          Floor: ''
        },
        createFoodRules: {
          Name: [{required: true, message: '请输入食堂名称', trigger: 'blur'}],
          Floor: [{required: true, message: '请输入食堂层数', trigger: 'blur'}],
        }
      }
    },
    methods: {
      create: function () {
        let con = {};
        con['name'] = this.createFoodForm.Name;
        con['floor'] = this.createFoodForm.Floor;
        this.$axios({
          url: 'http://127.0.0.1:8000/api/add_canteen',
          method: 'post',
          data: Qs.stringify(con),
        }).then((ret) => {
          if (ret.data.code === 0) {
            this.$message.success("食堂信息添加成功");
            //this.$refs.upload.clearFiles();
            this.createFoodForm.Name = '';
            this.createFoodForm.Floor = '';
            this.$refs.upload.clearFiles();
          }
            else this.$notify.error(ret.data.message + "，添加失败");
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
  