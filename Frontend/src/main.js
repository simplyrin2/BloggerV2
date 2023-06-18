import Vue from 'vue'
import VueRouter from 'vue-router'
import Vuex from 'vuex'
import VueCookies from 'vue-cookies'

import App from './App.vue'
import Feed from './views/FeedView.vue'
import Create from './views/CreateView.vue'
import Search from './views/SearchView.vue'
import Notifications from './views/NotificationsView.vue'
import Profile from './views/ProfileView.vue'
import viewProfile from './views/ViewProfile.vue'
import Login from './views/LoginView.vue'
import Signup from './views/SignupView.vue'
import Post from './views/PostView.vue'
import EditPost from './views/EditPostView.vue'
import EditProfile from './views/EditProfile.vue'
import Error from './views/ErrorView.vue'

Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(VueCookies, {secure: true,})
Vue.config.productionTip = false

const store = new Vuex.Store({
  state: {
    api_url: 'http://127.0.0.1:5000/api',
    title: '',
    isloggedin: false,
    username: '',
    token: localStorage.getItem('token'),
    defaultProfileImg: 'https://bloggerv2.s3.ap-south-1.amazonaws.com/defaultprofile.jpg'
  },
  mutations: {
    changePageTitle(state, title) {
      state.title = title
    },
    login(state, val) {
      state.isloggedin = val
    },
    changeUsername(state, val) {
      state.username = val
    }
  },
  actions: {
    logout(state) {
        console.log('LOGOUT')
        state.commit('login', false)
        localStorage.removeItem('token')
        router.push({name: 'login'})
    },
    unauthorized_error(state) {
      state.commit('login', false)
      router.replace({name: 'login'})
    }
  }
})

const routes = [
  {path: '/', component: Feed, alias: ['/home', '/index', '/main', '/feed'], name: 'feed',meta: {requiresAuth: true}},
  {path: '/create', component: Create, name: 'create', meta: {requiresAuth: true}},
  {path: '/post/:id', component: Post, name: 'post', meta: {requiresAuth: true}},
  {path: '/post/edit/:id', component: EditPost, name: 'editpost', meta: {requiresAuth: true}},
  {path: '/search', component: Search, name: 'search', meta: {requiresAuth: true}},
  {path: '/notifications', component: Notifications, name: 'notifications', meta: {requiresAuth: true}},
  {path: '/profile', component: Profile, name: 'profile', meta: {requiresAuth: true}},
  {path: '/profile/edit', component: EditProfile, name: 'editprofile', meta: {requiresAuth: true}},
  {path: '/profile/:username', component: viewProfile, name: 'view_profile', meta: {requiresAuth: true},},
  {path: '/login', component: Login, name: 'login', meta: {requiresAuth: false}},
  {path: '/signup', component: Signup, name: 'signup', meta: {requiresAuth: false}},
  {path: '/error', component: Error, name: 'error', meta: {requiresAuth: false}},
]

const router = new VueRouter({
  routes,
  mode: 'history',
  render: true
})

router.beforeEach(async (to, from, next) => {
  if (!localStorage.getItem('token')){
    store.commit('login', false)
    if(to.meta.requiresAuth && !store.state.isloggedin) {
      next({name: 'login', query: {redirect: `${to.path}`}})
    }
    else {
      next()
    }
  }
  else {
    if (to.meta.requiresAuth) {
      if (!store.state.isloggedin) {
        await fetch('http://127.0.0.1:5000/api/verify',
          {
          method: "GET",
          headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': "application/json",
          },
          credentials: 'include',
          }
          ).then((res) => {
              if (res.status == 401) {
                next({name: 'login', query: {redirect: `${to.path}`}})
              }
              else if (res.status == 200) {
                  store.commit('login', true)
                  next()
              }
              return res.json()
          }).then((res) => {
              store.commit('changeUsername', res.username)
              console.log(res.username)
          }).catch(err => {
            console.log(err)
            next({name: 'error'})
          })
      } else
          next()
    }
    else {
      next()
    }
  }
})

new Vue({
  render: h => h(App),
  router,
  store,
}).$mount('#app')

