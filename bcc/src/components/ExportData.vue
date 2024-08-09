<template>
    <div style="height: 800px;">
        <v-app>
            <v-list>
                <v-row style="margin-left: 10px">
                <v-icon color="blue">mdi-bulletin-board</v-icon>
                <h1 style="margin-left: 10px;margin-top: 1px">
                {{ text }}</h1>
                </v-row>
            </v-list>
            <div style="height: 20px;"></div>
            <v-tabs>
              <v-btn @click="showCharts" color="blue lighten-3" style="margin-left: 10px">查看各食堂好评数</v-btn>
              <v-btn @click="showDish"
                  v-show="true"
                  color="blue lighten-3"
                     style="margin-left: 10px">查看菜单
              </v-btn>
              <v-btn @click="getPdf('#'+'pdf', '菜单')"
                  v-show="!this.show1"
                  color="blue lighten-3"
                     style="margin-left: 10px">导出菜单
              </v-btn>
            </v-tabs>

          <v-row style="margin-top: 20px;margin-left: 20px">
            <div style="width:500px;height:500px" v-show="!show1" id = "pdf">
            <table align="center" width="100%" class="table xunw_table_form" border="0">
                <tbody>
                <tr><th colspan="10" class="zxstyle ly">食堂菜单</th>
                </tr>
                <tr>
                    <th  class="zxstyle">名称</th>
                    <th  class="zxstyle">卡路里</th>
                    <th  class="zxstyle">位置</th>
                    <th  class="zxstyle">价格</th>
                    <th  class="zxstyle">好评数</th>
                    <th  class="zxstyle">差评数</th>
                    <th  class="zxstyle">简介</th>
                </tr>
                <tr v-for="item in foodList" :key="item.food_id">
                    <td>{{item.name}}</td>
                    <td>{{item.calorie}}</td>
                    <td>{{item.place}}</td>
                    <td>{{item.price}}</td>
                    <td>{{item.like}}</td>
                    <td>{{item.dislike}}</td>
                    <td>{{item.intro}}</td>
                </tr>
                </tbody>
            </table>
        </div>
            <div v-show="chartsBar" style="width:500px;height:500px;float:right;" id="mychart2">
            </div>
          </v-row>
    </v-app>
    
    </div>
  </template>
  
  <script>
  
  import Qs from "qs";
  import * as echarts from "echarts";
  
  export default {
    name: "FindFood-1",
    // todo
    components: {},
    // components: {FoodList},
    data(){
      return {
        text:"导出数据",
        show1:"false",
        foodList: [],
        list: [],
        canteen_num:'',
        firstClickBar:true,
        chartsBar:false,
      }
    },
    methods:{
      getScore(){
      this.$axios.post(
          "http://127.0.0.1:8000/api/get_Score",
      ).then((res)=>{
        if(res.data.code===0){
          console.log(res.data.list)
          this.list = res.data.list;
          this.canteen_num = res.data.canteen_num;
          //this.dataAxis = res.data.canteen_name;
          //然后挑选对应的层数
        }
          else this.$notify.error(res.data.message)
      }).catch((error)=>{
        console.log(error)
      })
      },
     getTotalFood(){
      this.$axios.post(
          "http://127.0.0.1:8000/api/find_food",
          Qs.stringify({
            user_id: localStorage.getItem('user_id'),
            key_word: ""
          })
      ).then((res)=>{
        if(res.data.code===0){
          console.log(res.data.food_list)
          this.foodList = res.data.food_list;
        }
        else this.$notify.error(res.data.message)
      }).catch((error)=>{
        console.log(error)
      })
    },
    showCharts() {
        if (this.firstClickBar) {
          
          this.initEchartsBar();
          this.firstClickBar = false;
        }
        this.chartsBar = !this.chartsBar;
      },
    initEchartsBar() {
        const chartDom = document.getElementById('mychart2');
        const myChart = echarts.init(chartDom);
        let dataAxis = [];
        let data = [];
        for (var i = 0; i < this.list.length; i++){
          dataAxis.push(this.list[i].place);
          data.push(this.list[i].score);
        }
        let yMax = 500;
        let dataShadow = [];
        for (let i = 0; i < data.length; i++) {
          dataShadow.push(yMax);
        }
        const option = {
          title: {
            text: '各食堂点赞总数分布',
        },
        xAxis: {
          type: 'category',
          splitLine: {show: false},
          data: dataAxis,
          axisTick: {
            show: false
          },
          axisLine: {
            show: false
          },
          z: 10
        },
        yAxis: {
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            color: '#999'
          }
        },
        dataZoom: [
          {
            type: 'inside'
          }
        ],
        series: [
          {
            name: "总点赞数",
            type: 'bar',
            showBackground: true,
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {offset: 0, color: '#83bff6'},
                {offset: 0.5, color: '#188df0'},
                {offset: 1, color: '#188df0'}
              ])
            },
            emphasis: {
              itemStyle: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                  {offset: 0, color: '#2378f7'},
                  {offset: 0.7, color: '#2378f7'},
                  {offset: 1, color: '#83bff6'}
                ])
              }
            },
            data: data,
            label: {
              show: true,
              position: 'inside'
            }
          }
        ]
      };
      const zoomSize = 6;
      myChart.on('click', function (params) {
        console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
        myChart.dispatchAction({
          type: 'dataZoom',
          startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
          endValue:
          dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
        });
      });
      option && myChart.setOption(option);
    },
    showDish() {
      this.show1 = !this.show1;
    },
  },
    mounted() {
      this.getTotalFood();
      this.getScore();
    }
  }
  </script>
  
  <style scoped>
  .tools{
    height: 30px;
    width: 1200px;
    display: flex;
  }
  .search-box{
    width: 420px;
    margin-right: 20px;
  }
  .dropdownSort-box{
    width: 250px;
  }
  .dropdownType-box{
    width: 90px;
    margin-right: 30px;
  }
  .dropdownLevel-box{
   width: 90px;
   margin-right: 30px;
  }
  .clubBar{
    width: 650px;
    float: left;
    height: 200px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    margin-right: 20px;
    margin-bottom: 20px;
  }
  .club_picture{
    margin-left: 10px;
    width: 200px;
    height: 200px;
    float: left;
    margin-right: 30px;
  }
  .club_name{
    font-size: 50px;
    width: 410px;
    float: left;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .club_info{
    float: left;
    width: 410px;
    margin-bottom: 10px;
  }
  .club_dis{
    word-wrap: break-word;
    display: inline;
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
  </style>
  