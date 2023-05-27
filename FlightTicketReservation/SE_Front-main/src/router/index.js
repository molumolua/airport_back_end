import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/findPassword',
    name: 'findPassword',
    component: () => import('../views/FindPasswordView.vue')
  },
  {
    path: '/flight',
    name: 'flight',
    component: () => import('../views/FlightView.vue')
  },
  {
    path: '/flightInfo',
    name: 'flightInfo',
    component: () => import('../views/FlightInfoView.vue')
  },
  {
    path: '/order',
    name: 'order',
    component: () => import('../views/OrderView.vue')
  },
  {
    path: '/userInfo',
    name: 'userInfo',
    component: () => import('../views/UserInfoView.vue')
  },
  {
    path: '/changePassword',
    name: 'changePassword',
    component: () => import('../views/ChangePasswordView.vue')
  },
  {
    path: '/ticketInfo',
    name: 'ticketInfo',
    component: () => import('../views/TicketInfoView.vue')
  },
  {
    path: '/manager',
    name: 'manager',
    component: () => import('../views/ManagerView.vue')
  },
  {
    path: '/addFlight',
    name: 'addFlight',
    component: () => import('../views/AddFlightView.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue')
      
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
