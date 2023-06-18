<template>
    <div class="profile-img">
        <RouterLink :to="path"><img :src="src" :style="{height: height, width: width}" /></RouterLink>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';


export default({
    props: {
        src: String,
        path: String,
    },
    data: function() {
        return {
            height: null,
            width: null,
        }
    },
    components: {
        RouterLink
    },
})


</script>

<style scoped>
.profile-img {
    width: 3.5rem;
    height: 3.5rem;
    border-radius: 100%;
    overflow: hidden;
    background-color: var(--app-background);
    display: flex;
    align-items: center;
    justify-content: center;
}

img {
    width: 100%;
}

</style>