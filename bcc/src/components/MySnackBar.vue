<template>
  <v-snackbar
      timeout="1000"
      center
      top
      v-model="snackbar.show"
  >
    {{ snackbar.text }}
    <template v-slot:action="{ attrs }">
      <v-btn
          color="pink"
          text
          v-bind="attrs"
          @click="snackbar.show = false"
      >
        关闭
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  name: "MySnackBar",
  data() {
    return {
      snackbar: {
        show: false,
        text: ""
      },
    }
  },
  methods: {
    //点击
    handleClick(title) {
      this.snackbar.text = title;
      this.snackbar.show = true
    }
  },
  mounted() {
    this.$bus.$on('showSnackBar', this.handleClick)
  },
  beforeDestroy() {
    this.$bus.$off('showSnackBar')
  }
}
</script>

<style scoped>

</style>