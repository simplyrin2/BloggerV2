<template>
    <!-- <div id="wrapper"> -->
        <!-- <div @click="$emit('backdrop_clicked')" id="backdrop"></div> -->
        <Transition name="bounce">
        <div v-on-clickaway="away" v-if="visible" id="container">
            <span id="close-icon" @click="$emit('away')">
            <i class="bi bi-x-lg"></i></span>    
            <ProfileBlock v-for="(item,key) in UsersData" :key="key" :name="item.name" :username="item.username" :profile_img="item.pic"></ProfileBlock>
        </div>
        </Transition>
    <!-- </div> -->
</template>

<script>
import { directive as onClickaway } from 'vue-clickaway';

import ProfileBlock from './ProfileBlock.vue';

export default({
    name: 'UserModal',
    directives: {
        onClickaway: onClickaway
    },
    props: {
        UsersData: Array, visible: Boolean,
    },
    data: function() {
        return {
        }
    },
    components: {
    ProfileBlock,
    },
    methods: {
        away() {
            this.$emit('away')
        }
    },
})

</script>

<style scoped>
#container {
    top: 4rem;
    left: 50%;
    translate: -50%;
    background-color: rgb(247, 247, 247);
    border: 2px solid rgb(202, 202, 202);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 3rem 1rem;
    border-radius: 0.8rem;
    max-height: 40rem;
    overflow-y: auto;
    position: absolute;
}

#close-icon {
    position: absolute;
    top: 1rem;
    right: 1rem;
    cursor: pointer;
}

#close-icon > i {
    color: var(---primary-text-color);
    -webkit-text-stroke: 0.2px;
}

.bounce-enter-active {
    animation: bounce-in 200ms;
  }
  .bounce-leave-active {
    animation: bounce-in 100ms reverse;
  }
  @keyframes bounce-in {
    0% {
      transform: translateY(-10%);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }

</style>