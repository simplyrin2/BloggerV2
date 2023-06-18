<template>
  <div id="app">
    <SideBar></SideBar>
    <TopBar></TopBar>
    <div id="main-wrapper">
      <div v-cloak id="main-container">
        <Transition name="scale" mode="out-in">
          <RouterView :key="this.$route.params.username" @toast="triggerToast"></RouterView>
        </Transition>
      </div>
    <Toast :msg="toastmsg" v-show="toastVisible" class="toast"></Toast>
  </div>
  </div>
</template>

<script>
import { RouterView } from 'vue-router';
import SideBar from './components/SideBar.vue';
import TopBar from './components/TopBar.vue';
import Toast from './components/Toast.vue';

export default {
  name: 'App',
  data: function() {
    return {
      toastVisible: false,
      toastmsg: '',
    }
  },
  methods: {
    triggerToast(msg) {
      this.toastmsg = msg
      this.toastVisible = true
      setTimeout(()=>{
        this.toastVisible = false
      }, 3000)
    },
  },
  async mounted() {
    const s1 = new EventSource('http://127.0.0.1:5000/stream')
    s1.addEventListener('exportcsv', e => {
      let data = JSON.parse(e.data)
      this.triggerToast(data.message)
      console.log(data.message)
    }, false)
    s1.addEventListener(this.$store.state.username, e => {
      let data = JSON.parse(e.data)
      this.triggerToast(data.message)
    }, false)
  },
  components: {
    SideBar,
    RouterView,
    TopBar,
    Toast
}, 
}

</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', sans-serif;
}

:root {
    --primary-color: rgb(122, 200, 255);
    --secondary-color: rgb(60, 77, 112);
    --tertiary-color: rgb(108, 131, 177);
    --primary-gray: rgb(33, 33, 33);
    --secondary-gray: rgb(54, 52, 52);
    --app-background: rgb(255, 255, 255);
    --app-background-color: rgb(234, 246, 255);
    /* --app-background-color: rgb(238, 238, 238); */
    --primary-text-color: rgb(77, 77, 77);
    --secondary-text-color: rgb(112, 112, 112);
    --error-color: rgb(137, 0, 0);
    /* --app-background: rgb(31, 31, 31);
    --primary-text-color: rgb(211, 211, 211);
    --secondary-text-color: rgb(203, 203, 203); */
}

body {
    background-color: var(--app-background-color);
}

a {
  text-decoration: none;
  cursor: pointer;
}

#main-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

#main-container {
  margin-top: 1rem;
  margin-left: 5.5rem;
  width: 80%;
}

.scale-enter-active, .scale-leave-active {
  transition: all 100ms ease;
}

.scale-leave-to {
  opacity: 0;
}

.bounce-enter-active {
    animation: bounce-in 200ms;
  }
  .bounce-leave-active {
    animation: bounce-in 100ms reverse;
  }
  @keyframes bounce-in {
    0% {
      transform: translateY(-5%);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }

.lds-dual-ring {
  display: inline-block;
  width: 20px;
  height: 20px;
}

.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 3px solid #fff;
  border-color: #fff transparent #fff transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}
@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
