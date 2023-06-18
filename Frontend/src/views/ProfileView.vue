<template>
    <div v-cloak :class="{'prevent-scroll': (showFollowers || showFollowing)}">
    <div class="profile-header">
                <UserModal @away="away" :visible="showFollowers" v-if="followers.length>0" :UsersData="followers"></UserModal>
                <UserModal @away="away" :visible="showFollowing" v-if="following.length>0" :UsersData="following"></UserModal>
                <ProfileIcon :src="pic" path="#"></ProfileIcon>
                <div class="profile-header-details">
                    <div class="follow-details">
                        <a href="#" @click="toggleFollowersList">
                            <p class="count">{{ followers.length }}</p>
                            <p class="tag">Followers</p>
                        </a>
                    </div>
                    <div class="follow-details">
                        <a href="#" @click="toggleFollowingList">
                            <p class="count">{{ following.length }}</p>
                            <p class="tag">Following</p>
                        </a>
                    </div>
                </div>
            </div>
            <div class="user-details">
                <div class="name-username">
                    <p class="name">{{ name }}</p>
                    <p class="username">@{{ username }}</p>
                </div>
                <!-- {% if user.bio %} -->
                <p v-show="bio" class="bio">{{bio}}</p>
                <!-- {% endif %} -->
            </div>
            <div class="post-stat">
                <div class="post-count-wrapper">
                    <p style="font-size: 0.9rem">Blogs</p>
                    <p class="post-count"><strong>{{ posts.length }}</strong></p>
                </div>
                <div class="profile-actions">
                    <div v-if="posts.length" @click="exportCSV" class="action-btn">
                        <a>Export CSV</a>
                    </div>
                    <div class="action-btn">
                        <RouterLink to="/profile/edit">Edit Profile</RouterLink>
                    </div>
                </div>
            </div>
            <TransitionGroup class="feed" name="bounce">
                <FeedPost @postDeleted="reload" v-for="(post,key) in posts" :key="key" :postData="post" :profileView="profileView"></FeedPost>
            </TransitionGroup>
    </div>
</template>

<script>

import FeedPost from '@/components/FeedPost.vue'
import ProfileIcon from '@/components/ProfileIcon.vue'
import UserModal from '@/components/UserModal.vue'
import { RouterLink } from 'vue-router'
export default({
    name: 'ProfileView',
    data: function() {
        return {
            name: '',
            username: '',
            followers: [],
            following: [],
            bio: '',
            posts: [],
            pic: '',
            showFollowers: false,
            showFollowing: false,
            profileView: true,
        }
    },
    methods: {
        reload() {
            window.location.reload(true)
        },
        away() {
            if (this.showFollowers)
            {
                this.showFollowers = false
            }
            else {
                this.showFollowing = false
            }
        },
        toggleFollowersList() {
            this.away()
            this.showFollowers = !this.showFollowers
        },
        toggleFollowingList() {
            this.away()
            this.showFollowing = !this.showFollowing
        },
        exportCSV() {
            const options = {
            method: "GET",
            headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': "application/json",
            },
            credentials: 'include',
            }
            fetch("http://127.0.0.1:5000/api/exportcsv", options).then(res=>{
                if (res.status != 200)
                    throw new Error(res.status)
            this.$emit('toast','Processing request...')
            return res.json()
            }
            ).then(res=>{
                console.log(res)
            }).catch(err=>{
            if (err.message == '401') {
                this.$store.dispatch('unauthorized_error')
            }
        })
        }
    },
    components: {
    FeedPost,
    ProfileIcon,
    UserModal,
    RouterLink
}
    ,
    beforeMount() {
        this.$store.commit('changePageTitle', 'Your Profile')
        const options = {
          method: "GET",
          headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': "application/json",
          },
          credentials: 'include',
          }
        fetch("http://127.0.0.1:5000/api/user", options).then(res=>{
                if (res.status != 200)
                    throw new Error(res.status)
            return res.json()
            }
        ).then(res=>{
            this.username = res.username
            this.name = res.name
            this.followers = res.followers
            this.following = res.following
            this.bio = res.bio
            this.posts = res.posts
            if (res.pic=='')
                this.pic = this.$store.state.defaultProfileImg
            else
                this.pic = res.pic
        }).catch(err=>{
            if (err.message == '401') {
                this.$store.dispatch('unauthorized_error')
            }
        })
    },
})

</script>

<style scoped>
.profile-header {
    padding: 1.65rem 1.75rem;
    display: flex;
    justify-content: flex-start;
    gap: 1rem;
    align-items: center;
}

.profile-img {
    width: 8rem;
    height: 8rem;
    background-color: var(--app-background);
    border-radius: 100%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid rgb(190, 190, 190);
}


.profile-header-details {
    display: flex;
    padding: 0.8rem 1.8rem;
    gap: 2.3rem;
}

.follow-details > a {
    display: flex;
    gap: 0.375rem;
    justify-content: center;
    align-items: center;
    text-decoration: none;
    color: #000000;
}

.count {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--secondary-color);
}

.tag {
    font-size: 0.875rem;
    color: var(---primary-text-color);
}

.user-details {
    padding: 1rem 1.625rem;
}

.name {
    font-size: 2rem;
    font-weight: 700;
}

.username {
    font-size: 1rem;
    color: var(--secondary-color);
    font-weight: 600;
}

.bio {
    margin-top: 1.1rem;
}

.post-stat {
    display: flex;
    justify-content: space-between;
}

.post-count-wrapper {
    display: flex;
    align-items: center;
    padding: 0.7rem 0.8rem;
    gap: 10px;
}

.profile-actions {
    display: flex;
    gap: 0.8rem;
}

.action-btn > a{
    display: inline-block;
    text-decoration: none;
    background-color: #ffff;
    color: var(--secondary-color);
    padding: 0.5rem 0.8125rem;
    font-size: 0.8rem;
    font-weight: 600;
    border-radius: 0.8rem;
}

.feed {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.prevent-scroll {
    overflow-y: hidden !important;
    /* position: fixed; */
}
</style>
