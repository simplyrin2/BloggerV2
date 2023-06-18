<template>
    <nav id="sidebar">
        <div class="group">
            <i class="bi bi-send-fill" id="logo"></i>
            <RouterLink to="/"><NavBtn type="bi bi-layers" title="Feed"></NavBtn></RouterLink>
            <RouterLink to="/create"><NavBtn type="bi bi-plus-lg" title="Create"></NavBtn></RouterLink>
            <RouterLink to="/search"><NavBtn type="bi bi-search" title="Search"></NavBtn></RouterLink>
            <RouterLink to="/notifications" id="notification"><NavBtn type="bi bi-bell" title="Notifications"></NavBtn></RouterLink>
            <RouterLink to="/profile"><NavBtn type="bi bi-person" title="Profile"></NavBtn></RouterLink>
        </div>
        <NavBtn v-if="this.$store.state.isloggedin" @logout="logout" type="bi bi-box-arrow-right" title="Logout"></NavBtn>
    </nav>
</template>

<script>
import { RouterLink } from 'vue-router';
import NavBtn from './NavBtn.vue';

export default {
    name: 'SideBar',
    methods: {
        logout() {
            this.$store.dispatch('logout')
        }
    },
    data: function() {
        return {
        }
    },
    components: {
    NavBtn,
    RouterLink
    },
}
</script>

<style scoped>
#sidebar {
    position: fixed;
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 0.75rem;
    background-color: var(--primary-gray);
    box-shadow: 1px 0 10px rgba(0,0,0,0.4);
    z-index: 2;
    justify-content: space-between;
}

.group {
    display: flex;
    flex-direction: column;
    justify-items: center;
    align-items: center;
    gap: 0.8rem;
}

#logo {
    color: var(--primary-color);
    -webkit-text-stroke: 0.5px;
    font-size: 2rem;
    margin-bottom: 0.8rem;
    transition: transform 200ms ease-in;
}

#logo:hover {
    transform: rotate(20deg);
}

#notification {
    position: relative;
}

.dot {
    position: absolute;
    height: 0.6rem;
    width: 0.6rem;
    background-color: var(--primary-color);
    top: 2px;
    right: 4px;
    border-radius: 1rem;
}
</style>