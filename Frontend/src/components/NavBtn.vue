<template>
    <button @click="$emit('logout')" @mouseover="text=true" @mouseleave="text=false" class="navButton">
        <i :class=type></i>
        <transition name="fade">
        <span v-show="text">{{title}}</span>
        </transition>
    </button>
</template>

<script>
export default {
    props: {
        type: String,
        title: String,
    },
    data: function() {
        return {
            text: false
        }
    },
    
}
</script>

<style scoped>
.navButton {
    position: relative;
    border: none;
    border-radius: 3rem;
    width: 3.3rem;
    min-height: 3.3rem;
    background-color: var(--secondary-gray);
    transition: all 150ms;
    cursor: pointer;
}

.navButton:hover {
    border-radius: 1.3rem;
    background-color: rgb(60, 77, 112);
}

.navButton:hover > i {
    color: whitesmoke;
}

.navButton > span {
    background-color: rgb(255, 255, 255);
    padding: 0.2rem 0.6rem;
    border-radius: 0.2rem;
    font-weight: 600;
    position: absolute;
    left: 5rem;
    color: var(--primary-text-color);
    box-shadow: 0 2px 15px rgba(0,0,0,0.10);
    font-size: 0.95rem;
}

.navButton > i {
    font-size: 1.2rem;
    color: var(--primary-color);
    -webkit-text-stroke: 0.2px;
}

</style>