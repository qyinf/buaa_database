import VueRouter from "vue-router";
import SearchFood from "@/pages/SearchFood";
import MainPage from "@/pages/MainPage";
import MyDiet from "@/pages/MyDiet";
import MyDiet2 from "@/pages/MyDiet2";
import MyDiet3 from "@/pages/MyDiet3";
import UserCenter from "@/pages/UserCenter";
import LoginPage from "@/pages/LoginPage";
import AddPage from "@/pages/AddPage";
import Add_Canteen from "@/pages/Add_Canteen"

const router = new VueRouter({
    // mode: 'hash', //hash||history
    routes: [
        {
            name: 'FoodListBack',
            path: '/FoodListBack'
        },
        {
            name: 'login',
            path: '/',
            component:LoginPage
        },
        {
            name: "searchFood",
            path: '/searchFood',
            component: SearchFood
        },
        {
            name: "mainpage",
            path: '/mainpage',
            component: MainPage
        },
        {
            name: "mydiet",
            path: '/mydiet1/:name',
            component: MyDiet

        },
        {
            name: "mydiet",
            path: '/mydiet2/:name',
            component: MyDiet2

        },
        {
            name: "mydiet",
            path: '/mydiet3/:name',
            component: MyDiet3

        },
        {
            name: "usercenter",
            path: '/usercenter/:id/:name',
            component: UserCenter,
        },
        {
            name: "addpage",
            path: '/addpage',
            component: AddPage,
        },
        {
            name: "AddCanteen",
            path: '/AddCanteen',
            component: Add_Canteen,
        }
    ]
})
export default router