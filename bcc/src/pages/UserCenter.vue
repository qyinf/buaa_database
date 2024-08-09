<template>
  <el-container>
    <div class="side-bar">
      <SideBar></SideBar>
    </div>
    <v-app>
      <MySnackBar></MySnackBar>
    </v-app>
      <el-container>
        <el-header>
          <MyHeader></MyHeader>
        </el-header>
        <el-container>
          <el-main>
            <MyUserCenterHeader
                :real_name="user.real_name"
                :avatar="user.avatar"
                :BMI="bmi.toFixed(1)"
                :cur-id="this.$router.history.current.params.id">
            </MyUserCenterHeader>
          </el-main>
          <el-main class="el-main-table">
            <el-descriptions class="margin-top" :column="1" border>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-postcard"></i>
                  学号
                </template>
                {{ user.user_id }}
              </el-descriptions-item>

              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-postcard"></i>
                  姓名
                </template>
                {{ user.real_name }}
              </el-descriptions-item>


              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-time"></i>
                  注册时间
                </template>
                {{ user.time }}
              </el-descriptions-item>

              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-sex"></i>
                  性别
                </template>
                <label v-show="!isEdit">
                  {{ user.sex }}</label>
                <template>
                  <el-radio size="mini" v-model="user.sex" v-show="isEdit" label="男">男</el-radio>
                  <el-radio size="mini" v-model="user.sex" v-show="isEdit" label="女">女</el-radio>
                </template>
              </el-descriptions-item>

          

              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-email"></i>
                  学院
                </template>
                <label v-show="!isEdit">
                  {{ user.institute }}
                </label>
                <el-input size="mini" v-model="user.institute" v-show="isEdit"></el-input>
              </el-descriptions-item>


              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-mobile-phone"></i>
                  手机号
                </template>
                <label v-show="!isEdit">
                  {{ user.phone }}
                </label>
                <el-input size="mini" v-model="user.phone" v-show="isEdit"></el-input>
              </el-descriptions-item>


              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-email"></i>
                  身高
                </template>
                <label v-show="!isEdit">
                  {{ user.height }}
                </label>
                <el-input size="mini" v-model="user.height" v-show="isEdit"></el-input>
              </el-descriptions-item>

              
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-email"></i>
                  体重
                </template>
                <label v-show="!isEdit">
                  {{ user.weight }}
                </label>
                <el-input size="mini" v-model="user.weight" v-show="isEdit"></el-input>
              </el-descriptions-item>


            </el-descriptions>

            <div class="flexs">
              <el-button type="primary"
                  @click="submitChangeInfo">
                  {{ mode }}
              </el-button>

              <el-button type="primary"
                v-show="isEdit"
                @click="isEdit = !isEdit">
              取消
            </el-button>
            
          </div>

          </el-main>
        </el-container>
      </el-container>
  </el-container>
</template>

<script>
import MyHeader from "@/components/MyHeader";
import SideBar from "@/components/SideBar";
import MyUserCenterHeader from "@/components/MyUserCenterHeader";
import MySnackBar from "@/components/MySnackBar";
import Qs from "qs";

export default {
  name: "UserCenter",
  components: {MySnackBar, MyUserCenterHeader, MyHeader, SideBar},
  data() {
    return {
      id:localStorage.getItem('user_id'),
      bmi: '',
      user: {
        user_id: "21373090",
        password: "123456",
        avatar: "",
        time: "2023-11-25",
        real_name: "柒羽",
        sex: "女",
        institute: "计算机学院",
        phone: "18539100301",
        height: "",
        weight: "",
        //BMI:"1",
      },
      
      isEdit: false
    }
  },
  methods: {
    submitChangeInfo() {
      if (this.isEdit) {
        this.$axios.post(
            "http://127.0.0.1:8000/api/update_user_information",
            Qs.stringify(
                this.user
            )
        ).then((res) => {
          if (res.data.code === 0) {
            this.$bus.$emit('showSnackBar', "你已成功修改信息！")
             this.$router.go(0)
          } else this.$notify.error(res.data.message)
        }).catch((error) => {
          console.log(error)
        })
      }
      this.isEdit = !this.isEdit
     
    },
    getUserInformation() {
      this.$axios.post(
          "http://127.0.0.1:8000/api/get_user_information",
          Qs.stringify({
            'user_id': this.$router.history.current.params.id
          })
      ).then((res) => {
        if (res.data.code === 0) {
          this.user = res.data.user
          this.bmi = parseInt(this.user.weight) / (parseInt(this.user.height)*parseInt(this.user.height))*10000
        } else this.$notify.error(res.data.message)
      }).catch((error) => {
        console.log(error)
      })
    },
  },
  computed: {
    mode() {
      if (this.isEdit) {
        return "提交"
      } else {
        return "编辑"
      }
    }
  },
  mounted() {
    this.getUserInformation()
  },
}
</script>

<style scoped>
.el-main-table {
  width: 50%;
  align-self: center;
}

.flexs {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.el-icon {
  color: cornflowerblue;
}

.el-icon-real_name {
  background: url("../assets/real_name.png") no-repeat;
  font-size: 16px;
  background-size: contain;
}

.el-icon-real_name:before {
  content: "ccc";
  font-size: 1px;
  color: rgba(255, 255, 255, 0);
}

.el-icon-sex {
  background: url("../assets/sex.png") no-repeat;
  font-size: 16px;
  background-size: cover;
}

.el-icon-sex:before {
  content: "ccc";
  font-size: 1px;
  color: rgba(255, 255, 255, 0);
}

.el-icon-institute {
  background: url("../assets/institute.png") no-repeat;
  font-size: 16px;
  background-size: cover;
}

.el-icon-institute:before {
  content: "ccc";
  font-size: 1px;
  color: rgba(255, 255, 255, 0);
}

.el-icon-email {
  background: url("../assets/email.png") no-repeat;
  font-size: 16px;
  background-size: cover;
}

.el-icon-email:before {
  content: "ccc";
  font-size: 1px;
  color: rgba(255, 255, 255, 0);
}

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
