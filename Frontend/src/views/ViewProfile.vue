<template>
    <div v-cloak>
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
                <div class="detail-wrapper">
                    <div class="name-username">
                        <p class="name">{{ name }}</p>
                        <p class="username">@{{ username }}</p>
                    </div>
                    <div class="profile-actions">
                        <div @click="onFollow" v-if="follow" class="action-btn">
                            <a >Following</a>
                        </div>
                        <div @click="onFollow" v-else class="action-btn">
                            <a class="follow">Follow</a>
                        </div>
                </div>
                </div>
                <p v-show="bio" class="bio">{{ this.bio }}</p>
            </div>
            <div class="post-stat">
                <div class="post-count-wrapper">
                    <p style="font-size: 0.9rem">Blogs</p>
                    <p class="post-count"><strong>{{ posts.length }}</strong></p>
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
            profileView: false,
            follow: false,
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
        onFollow() {
            const options = {
            method: "GET",
            headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': "application/json",
            },
            credentials: 'include',
            }
            fetch(`${this.$store.state.api_url}/user/${this.$route.params.username}?follow=true`, options).then(res=>{
                if (res.status != 200)
                        throw new Error(res.status)
                this.follow = !this.follow
                return res.json()
            }).catch(err=>console.log(err))
            
        }
    },
    components: {
    FeedPost,
    ProfileIcon,
    UserModal,
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
        fetch(`${this.$store.state.api_url}/user/${this.$route.params.username}`, options).then(res=>{
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
            this.follow = res.follow
            if (res.pic=='')
                this.pic = this.$store.state.defaultProfileImg
            else
                this.pic = res.pic
        }).catch(err=>{
            if (err.message == '401') {
                this.$store.dispatch('unauthorized_error')
            }
            if (err.message == '404') {
                this.$router.replace({name: 'profile'})
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

.detail-wrapper {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.follow {
    background-color: var(--secondary-color) !important;
    color: var(--app-background) !important;
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

.action-btn {
    cursor: pointer;
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
