<template>
  <div>
    <div class="flexs">
      <h1>你好!{{ userName }}</h1>
      <el-badge >
        <el-button circle @click="quit" icon="el-icon-switch-button"></el-button>
      </el-badge>
      
    </div>
    
    <hr/>
  </div>
</template>

<script>
import Qs from "qs";

export default {
  name: "MyHeader",
  data() {
    return {
      userName: '柒羽',
      hidden: false,
      messageCount: 12,
      drawer: false,
      messages: [{
       }]
    }
  },
  methods: {
    quit() {
      let path = "/";
      this.$router.push({
        path
      });
      localStorage.clear()
    },
    getUserInformation() {
      this.$axios.post(
          "http://127.0.0.1:8000/api/get_user_information",
          Qs.stringify({
            'user_id': localStorage.getItem('user_id'),
          })
      ).then((res) => {
        if (res.data.code === 0) {
          // console.log(res.data)
          this.userName = res.data.user.real_name
        } else this.$notify.error(res.data.message)
      }).catch((error) => {
        console.log(error)
      })
    }
  },
  mounted() {
    this.getUserInformation();
  }
}
</script>

<style scoped>
.flexs {
  height: 75px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
