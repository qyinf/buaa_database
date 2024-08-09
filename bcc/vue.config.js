const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],
  devServer: {
    proxy: {
      '/api/login/': {//业务类的接口请求地址，这里的api可以是后端的工程名
        changeOrigin: true,
        target: 'http://127.0.0.1:8000/api/login/'
      },
    }
  }
})
