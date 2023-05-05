import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from "@/views/HomePage"
import LoginPage from "@/views/LoginPage"

const BasicInfo = () => import('@/components/BasicInfo')
const OptimizationPage = () => import('@/components/OptimizationPage')
const ResourceMangae = () => import('@/components/ResourceManage')

Vue.use(VueRouter)

const routes = [
    {
      path: '/',
      name: '/',
      component: HomePage
    },
    {
        path: '/home',
        name: 'home',
        component: HomePage,
        children: [
            {
                path: '/home/basic-info',
                name: 'query',
                component: BasicInfo
            },
            {
                path: '/home/optimization',
                name: 'optimization',
                component: OptimizationPage
            },{
                path: '/home/resource',
                name: 'resourceManage',
                component: ResourceMangae
            }
        ]
    },
    {
        path: '/login',
        name: 'login',
        component: LoginPage,
    }
]

const router = new VueRouter({
    routes
})

export default router
