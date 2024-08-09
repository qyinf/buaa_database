<template>
  <div>
    <v-app style="height: 100%;overflow-y: hidden;overflow-x: hidden">
      <v-row style="max-height: 50px;margin-top: 10px;margin-left: 10px" v-show="id === curId">
        <v-col cols="1">
          <v-icon color="blue">mdi-file-document-edit</v-icon>
        </v-col>
        <v-col cols="9">
          <h1>管理您的账号</h1>
        </v-col>
      </v-row>
      <v-row style="margin-left: 10px;max-height:50px;min-width: 300px">
        
        <v-btn color="deep-purple accent-1"
               elevation="5"
               @click="dialogFormVisible = true">
          修改密码
        </v-btn>
        
        <v-btn color="deep-purple accent-1"
               elevation="5"
               style="margin-left: 10px"
               @click="pickPhoto">
          上传头像
        </v-btn>

        <div>
          <el-dialog :visible.sync="dialogVisible">
            <el-upload
                :auto-upload="true"
                :before-upload="beforeAvatarUpload"
                :on-success="handleAvatarSuccess"
                :limit=1
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
            <el-button type="primary" @click="updateAvatar">提交</el-button>
            <el-dialog :visible.sync="dialogPictVisible" append-to-body>
              <img width="100%" :src="dialogImageUrl" alt="">
            </el-dialog>

          </el-dialog>
        </div>
        
        <div>

          <el-dialog :visible.sync="dialogFormVisible">
            <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px"
                     class="demo-ruleForm">
              <el-form-item label="原始密码" prop="oldPass">
                <el-input type="password" v-model="ruleForm.oldPass" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="pass">
                <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item label="确认密码" prop="checkPass">
                <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                <el-button @click="resetForm('ruleForm')">重置</el-button>
              </el-form-item>
            </el-form>
          </el-dialog>
          
        </div>
      </v-row>


      <v-row style="margin-left: 10px;max-height:50px;min-width: 300px" v-show="id !== curId">
      </v-row>
      <v-row align-self="center"
        style="margin-left: 10px;
        max-height:300px;
        margin-top: 30px">
        <v-card width="70%" shaped>
          <v-row style="margin-left: 0;margin-top: 0;margin-right: 0;">
            <v-avatar tile width="100%" height="300px">
              <img :src="avatar" alt="头像" v-if="!modified">
              <img :src="imageUrl" alt="头像" v-if="modified">
            </v-avatar>
            <v-col cols="8" style="float: left">
              <v-card-title>用户名：{{ real_name }}</v-card-title>
            </v-col>
            <v-col cols="8" style="float: left">
              <v-card-title>BMI指数： {{ BMI }}</v-card-title>
            </v-col>
          </v-row>
        </v-card>
      </v-row>
      <MySnackBar></MySnackBar>
    </v-app>
  </div>
</template>

<script>
import MySnackBar from "@/components/MySnackBar";
import Qs from "qs";

export default {
  name: "MyUserCenterHeader",
  components: {MySnackBar},
  props: ["real_name","avatar","curId","BMI"],
  data() {
    let validatePass = (value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'));
      } else {
        if (this.ruleForm.checkPass !== '') {
          this.$refs.ruleForm.validateField('checkPass');
        }
        callback();
      }
    };
    let validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    let validatePass3 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入原始密码'));
      } else {
        callback();
      }
    };
    return {
      id:localStorage.getItem('user_id'),
      imageUrl:'',
      tmpUrl:'',
      modified:false,
      dialogImageUrl: '',
      disabled:false,
      dialogFormVisible: false,
      dialogVisible:false,
      dialogPictVisible:false,
      ruleForm: {
        oldPass: '',
        pass: '',
        checkPass: '',
      },
      rules: {
        pass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        checkPass: [
          {validator: validatePass2, trigger: 'blur'}
        ],
        oldPass: [
          {validator: validatePass3, trigger: 'blur'}
        ]
      }
    }
  },
  methods: {
    submitForm(formName) {
      console.log("验证密码正确性")
      console.log(formName)
      this.$refs[formName].validate((valid) => {
        console.log(valid)
        if (valid) {
          this.$axios.post(
              "http://127.0.0.1:8000/api/modify_password",
              Qs.stringify({
                jwt: {'code':localStorage.getItem('code'),'user_id':localStorage.getItem('user_id'),'time':localStorage.getItem('time')},
                old_password:this.ruleForm.oldPass,
                new_password:this.ruleForm.pass
              })
          ).then((res)=>{
            if(res.data.code===0){
              this.dialogFormVisible = false
              this.$bus.$emit("showSnackBar", "修改密码成功！")
            } else if (res.data.code===3){
              this.$bus.$emit("showSnackBar", "初始密码错误！")
            } else this.$notify.error(res.data.message)
          }).catch((error)=>{
            console.log(error)
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    beforeAvatarUpload(file) {
      console.log(file);
      return true;
    },
    handleRemove(file) {
      console.log(file)
      this.$refs.upload.clearFiles();
    },

    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogPictVisible = true;
    },

    handleAvatarSuccess (res) {
      if (res.code !== 0) {
        this.$message.error(res.message)
        return false
      }
      this.tmpUrl = res.image_path
      // console.log(this.imageUrl)
    },
    /*
    DO: 上传头像接口，可以复用社团上传图片的接口
     */
    pickPhoto() {
      this.dialogVisible = true;
    },
    updateAvatar() {
      this.$axios({
        url: 'http://127.0.0.1:8000/api/update_avatar',
        method: 'post',
        data: Qs.stringify({
          user_id:localStorage.getItem('user_id'),
          avatar:this.tmpUrl
        }),
      }).then((ret) => {
        if (ret.data.code === 0) {
          this.dialogVisible = false;
          this.$message.success('上传成功')
          this.imageUrl = this.tmpUrl
          this.modified = true
          this.$refs.upload.clearFiles();
        } else this.$notify.error(ret.data.message + "，申请失败");
      })
    }
  },
  created() {
    this.modified = false
  }
}
</script>

<style scoped>
.flexs {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
