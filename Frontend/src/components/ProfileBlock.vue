<template>
    <div class='search-result'>
        <RouterLink :to="profilePath" class="profile">
            <ProfileIcon :src="ProfileImg" :path="profilePath"></ProfileIcon>
            <div class="profile-details">
                <p class="name">{{ name }}</p>                        
                <p class="username">{{ username }}</p>
            </div>
        </RouterLink>
        <div class="action-btn">
            <RouterLink :to="profilePath">View Profile</RouterLink>
        </div>
    </div>
</template>

<script>
import ProfileIcon from './ProfileIcon.vue';
import { RouterLink } from 'vue-router';

export default ({
    name: 'ProfileBlock',
    props: {
        name: String, username: String, profile_img: String
    },
    data: function() {
        return {
        }
    },
    computed: {
        profilePath() {
            return `/profile/${this.username}`
        },
        ProfileImg() {
            if (this.profile_img == '' || this.profile_img == null)
                return this.$store.state.defaultProfileImg
            else
                return this.profile_img
        }
    },
    components: {
        ProfileIcon,
        RouterLink
    }
})
</script>

<style scoped>

a {
    text-decoration: none;
}
.search-result {
    padding: 1.5rem 1.625rem;
    display: flex;
    width: 30rem;
    justify-content: space-between;
    align-items: center;
    background-color: var(--app-background);
    border-radius: 2rem;
}

.profile {
    display: flex;
    gap: 0.8rem;
    align-items: center;
    color: var(--primary-text-color)
}

.username {
    font-size: 0.7rem;
    color: var(--secondary-color);
    font-weight: 600;
    margin-top: 0.2rem;
}


.action-btn > a{
    display: inline-block;
    text-decoration: none;
    background-color: #f1f1f1;
    color: var(--secondary-color);
    padding: 0.5rem 0.8125rem;
    font-size: 0.8rem;
    font-weight: 600;
    border-radius: 0.8rem;
}
</style>