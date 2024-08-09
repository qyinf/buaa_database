<template>
  <div class="body-box">
    <div id="topBar-login">
      <div class="webLogo-box">
        <img class="webLogo" src="../assets/png/BCC.png" alt=""/>
      </div>
      <div class="logo-font-box">
        <div style="padding-top: 10px;">bcc</div>
      </div>
    </div>
    <div class="main-box">
      <div :class="['container', 'container-register',
          { 'is-txl': isLogin }]">

        <el-form :rules="registerRules" :model="createUserForm">
          <h2 class="title">注册</h2>

          <el-form-item prop="studentID">
            <el-input v-model="createUserForm.studentID"
              class="form__input" type="text" placeholder="学号"/>
          </el-form-item>

          <el-form-item prop="name">
            <el-input v-model="createUserForm.name"
              class="form__input" type="text" placeholder="姓名"/>
          </el-form-item>

          <el-form-item prop="password1">
            <el-input v-model="createUserForm.password1"
              class="form__input" type="password" placeholder="密码" show-password/>
          </el-form-item>

          <el-form-item prop="password2">
            <el-input v-model="createUserForm.password2"
              class="form__input" type="password" placeholder="再次输入密码" show-password/>
          </el-form-item>

          <el-form-item prop="sex">
            <el-input v-model="createUserForm.sex" class="form__input" type="text" placeholder="性别"/>
          </el-form-item>

          <el-form-item prop="institute">
            <el-input v-model="createUserForm.institute" class="form__input" type="text" placeholder="学院"/>
          </el-form-item>

          <el-form-item prop="height">
            <el-input v-model="createUserForm.height" class="form__input" type="text" placeholder="身高(单位:cm)"/>
          </el-form-item>

          <el-form-item prop="weight">
            <el-input v-model="createUserForm.weight" class="form__input" type="text" placeholder="体重(单位:kg)"/>
          </el-form-item>

          <el-form-item>
            <div class="primary-btn" @click="register">立即注册</div>
          </el-form-item>
        </el-form>
      </div>

      <div :class="['container', 'container-login', { 'is-txl is-z200': isLogin }]">
        <el-form :rules="loginRules" :model="loginForm">
          <h2 class="title">登录</h2>
          <el-form-item prop="studentID">
            <el-input v-model="loginForm.studentID" class="form__input" type="text" placeholder="学号"  />
          </el-form-item>
          <el-form-item prop="password">
            <el-input v-model="loginForm.password" class="form__input" type="password" placeholder="密码" show-password/>
          </el-form-item>
          <el-form-item>
            <div class="primary-btn" @click="login">立即登录</div>
          </el-form-item>
        </el-form>
      </div>

      <div :class="['switch', { login: isLogin }]">
        <div class="switch__circle"></div>
        <div class="switch__circle switch__circle_top"></div>
        <div class="switch__container">
          <h2>{{ isLogin ? '期待您的加入' : '欢迎回来' }}</h2>
          <p>
            {{
              isLogin
                  ? '还没有账号？点击下方按钮前往注册'
                  : '已创建过账号？点击下方按钮立即登录'
            }}
          </p>
          <div class="primary-btn" @click="isLogin = !isLogin">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Qs from "qs";

export default {
  name: "LoginPage",
  data() {
    let checkStudentID = (rule, value, callback) => {
      let studentID = /[0-9]{8}/;
      if (studentID.test(value)) {
        callback();
      }
      callback(new Error("学号格式：8位数字"));
    }
    let checkNewPwd = (rule, value, callback) => {
      let pwdReg = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,18}$/;
      if (!pwdReg.test(value)) {
        callback(new Error("密码长度8-18位，且需同时包含英文和数字"));
      }
      callback();
    }
    let checkNewPwd2 = (rule, value, callback) => {
      if (value !== this.createUserForm.password1) {
        callback(new Error("两次输入密码不一致！"));
      }
      callback();
    }
    return {
      isLogin: true,
      loginForm: {
        studentID: '',
        password: '',
      },
      createUserForm: {
        studentID: '',
        name: '',
        password1: '',
        password2: '',
        sex:'',
        institute:'',
        weight:'',
        height:''
      },
      loginRules: {
        studentID: [{required: true, message: '请输入学号', trigger: 'blur'}, {validator: checkStudentID, trigger: 'blur'}],
        password: [{required: true, message: '请输入密码', trigger: 'blur'}, {validator: checkNewPwd, trigger: 'blur'}],
      },
      registerRules: {
        studentID: [{required: true, message: '请输入学号', trigger: 'blur'}, {validator: checkStudentID, trigger: 'blur'}],
        password1: [{required: true, message: '请输入密码', trigger: 'blur'}, {validator: checkNewPwd, trigger: 'blur'}],
        password2: [{required: true, message: '请确认密码', trigger: 'blur'}, {validator: checkNewPwd2, trigger: 'blur'}],
        sex: [{required: true, message: '请输入性别', trigger: 'blur'}],
        institute: [{required: true, message: '请输入学院', trigger: 'blur'}]
      },
    }
  },
  methods:{
    login: function () {
      let con = {};
      con['user_id'] = this.loginForm.studentID;
      con['password'] = this.loginForm.password;
      this.$axios({
        url: 'http://127.0.0.1:8000/api/login_user',
        method: 'post',
        data: Qs.stringify(con),
      }).then((ret) => {
        if (ret.data.code === 0) {
          localStorage.clear();
          localStorage.setItem('user_id',ret.data.jwt.user_id);
          localStorage.setItem('code',ret.data.jwt.code);
          localStorage.setItem('time',ret.data.jwt.time);
          this.$message.success("登录成功");
          this.$router.push('/mainpage');
        } else this.$notify.error(ret.data.message+"，登录失败");
      })
    },
    register: function () {
      let con = {};
      con['user_id'] = this.createUserForm.studentID;
      con['name'] = this.createUserForm.name;
      con['password'] = this.createUserForm.password1;
      con['sex'] = this.createUserForm.sex;
      con['institute'] = this.createUserForm.institute;
      con['height'] = this.createUserForm.height;
      con['weight'] = this.createUserForm.weight;
      this.$axios({
        url: 'http://127.0.0.1:8000/api/register_user',
        method: 'post',
        data: Qs.stringify(con),
      }).then((ret) => {
        if (ret.data.code === 0) {
          this.$message.success("注册成功");
          this.isLogin = !this.isLogin;
          this.createUserForm = {
            name: '',
            studentID: '',
            password1: '',
            password2: '',
            verifyCode: '',
            sex: '',
            institute: '',
            height: '',
            weight: ''
          };
        } else this.$notify.error(ret.data.message+"，注册失败");
      })
    },
  }
}
</script>

<style lang="scss" scoped>
.main-box {
  margin-left: 17%;
  position: relative;
  width: 66%;
  min-width: 1000px;
  min-height: 600px;
  height: 650px;
  padding: 25px;
  background-color: #ecf0f3;
  box-shadow: 10px 10px 10px #d1d9e6, -10px -10px 10px #f9f9f9;
  border-radius: 12px;
  overflow: hidden;
  .container {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    width: 600px;
    height: 100%;
    padding: 25px;
    background-color: #ecf0f3;
    transition: all 1.25s;
    form {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      width: 100%;
      height: 100%;
      color: #a0a5a8;
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
        width: 350px;
        height: 35px;
        margin: 0px 0;
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
  .container-register {
    z-index: 100;
    left: calc(100% - 600px);
  }
  .container-login {
    left: calc(100% - 600px);
    z-index: 0;
  }
  .is-txl {
    left: 0;
    transition: 1.25s;
    transform-origin: right;
  }
  .is-z200 {
    z-index: 200;
    transition: 1.25s;
  }
  .switch {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 400px;
    padding: 50px;
    z-index: 200;
    transition: 1.25s;
    background-color: #ecf0f3;
    overflow: hidden;
    box-shadow: 4px 4px 10px #d1d9e6, -4px -4px 10px #f9f9f9;
    color: #a0a5a8;
    .switch__circle {
      position: absolute;
      width: 500px;
      height: 500px;
      border-radius: 50%;
      background-color: #ecf0f3;
      box-shadow: inset 8px 8px 12px #d1d9e6, inset -8px -8px 12px #f9f9f9;
      bottom: -37%;
      left: -60%;
      transition: 1.25s;
    }
    .switch__circle_top {
      top: -30%;
      left: 60%;
      width: 300px;
      height: 300px;
    }
    .switch__container {
      display: flex;
      justify-content: center !important;
      align-items: center;
      flex-direction: column;
      position: absolute;
      width: 400px;
      padding: 50px 55px;
      transition: 1.25s;
      h2 {
        font-size: 34px;
        font-weight: 700;
        line-height: 3;
        color: #181818;
      }
      p {
        font-size: 14px;
        letter-spacing: 0.25px;
        text-align: center;
        line-height: 1.6;
      }
    }
  }
  .login {
    left: calc(100% - 400px);
    .switch__circle {
      left: 0;
    }
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
}
.verify-btn{
  cursor: pointer;
  width: 80px;
  padding: 0 5px 0 5px;
  margin-top: 4px;
  margin-left: 10px;
  height: 40px;
  line-height: 40px;
  font-size: 13px;
  border-radius: 8px;
  background-color: #ecf0f3;
  box-shadow: 2px 2px 4px #d1d9e6, -2px -2px 4px #f9f9f9;
}
.verify-btn:hover{
  box-shadow: inset 2px 2px 4px #d1d9e6, inset -2px -2px 4px #f9f9f9;
}
.verify-btn:active{
  font-weight: bold;
  background-color: ghostwhite;
}
::v-deep .el-input__inner{
  background-color: #ecf0f3 !important;
  border: none 0 !important;
  padding-left: 0 !important;
  height: 30px !important;
  line-height: 30px !important;
}
.body-box{
  height: calc(100vh);
}
#topBar-login{
  position: relative;
  display: flex;
  height: 70px;
  padding: 0;
}
.webLogo-box{
  margin-left: 5px;
  float: left;
  height: 70px;
  width: 70px;
}
.webLogo{
  padding-top: 5px;
  height: 60px;
  width: 60px;
}
.logo-font-box{
  padding-top: 5px;
  font-family:华文行楷,serif;
  display: table-cell;
  width: 70px;
  font-size: 35px;
}
</style>
