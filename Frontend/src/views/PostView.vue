<template>
<div class="wrapper">
    <div class="feed-post">
            <div class="post-details">
                <RouterLink :to="profilePath" class="author">{{author}}</RouterLink>
                <p class="timestamp">{{timestamp}}</p>
            </div>
            <div class="post-content">
                <p class="title">{{title}}</p>
                <p class="content">{{content}}</p>
            </div>
            <div v-if="img" class="post-image">
                <div class="overlay-back">
                </div>
                <img class="image" :src="img" />
            </div>
            <div class="post-engagement">
                <a @click="onLike" class="like eng">
                    <svg :class="{'fill': liked}" width="16" height="14" viewBox="0 0 16 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M2.2385 1.7385C1.9251 2.0519 1.67649 2.42396 1.50688 2.83343C1.33727 3.24291 1.24997 3.68178 1.24997 4.125C1.24997 4.56821 1.33727 5.00709 1.50688 5.41656C1.67649 5.82604 1.9251 6.1981 2.2385 6.5115L8 12.273L13.7615 6.5115C14.3944 5.87856 14.75 5.02011 14.75 4.125C14.75 3.22989 14.3944 2.37144 13.7615 1.7385C13.1286 1.10556 12.2701 0.749978 11.375 0.749978C10.4799 0.749978 9.62144 1.10556 8.9885 1.7385L8 2.727L7.0115 1.7385C6.6981 1.4251 6.32604 1.17649 5.91657 1.00688C5.50709 0.837268 5.06822 0.749969 4.625 0.749969C4.18179 0.749969 3.74291 0.837268 3.33343 1.00688C2.92396 1.17649 2.5519 1.4251 2.2385 1.7385V1.7385Z" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>        
                </a>                    
                <a @click="showLikesToggle" class="eng like-count">
                    <p>{{likes.length}} Likes</p>
                </a>
                <UserModal @away="showLikes=false" :UsersData="likes" :visible="showLikes"></UserModal>   
            </div>
            <div class="comment-count">
                {{comments.length}} Comments
            </div>
            <div class="comment-bar">
                <form @submit.prevent="formSubmit" action="/comment" method="POST" class="post-form">
                    <div class="create-content">
                        <textarea v-model="yourcomment" type="text" name="comment" id="comment" placeholder="comment" rows="2" cols="35" maxlength="200" required></textarea>
                      </div>
                    <div class="search-submit">
                      <button type="submit">Comment</button>
                    </div>
                  </form>
            </div>
            <div class="comments" id="comments-section">
                <div v-for="(comment, key) in comments" :key="key" class="comment-block">
                    <div class="comment-header">
                        <RouterLink :to="{name: 'profile', params: {username: comment.username}}" href="/profile/" class="comment-user">
                            <p class="comment-name">{{ comment.name }}</p>
                            <p class="comment-username">@{{comment.username}}</p>
                        </RouterLink>
                        <a v-if="current_user(comment.username)" @click="removeComment(key, comment.comment_id)" class="remove-btn">Remove</a>
                    </div>
                    <p class="comment-content">
                        {{comment.comment}}
                    </p>
                </div>
            </div>
    </div>
</div>
</template>

<script>
import UserModal from '@/components/UserModal.vue';
import { RouterLink } from 'vue-router';

export default({
    name: "NotificationsView",
    data: function (){
        return {
            author: "",
            username: '',
            title: "",
            content: "",
            img: null,
            comments: [],
            likes: [],
            timestamp: '',
            post_id: '',
            yourcomment: '',
            liked: false,
            showLikes: false,
        };
    },
    computed: {
        profilePath() {
            return '/profile/'+this.username
        }
    },
    beforeMount() {
        this.$store.commit("changePageTitle", "Post");
        const options = {
          method: "GET",
          headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': "application/json",
          },
          credentials: 'include',
          }
        fetch(`${this.$store.state.api_url}/post/${this.$route.params.id}`, options).then(res=>{
                if (res.status != 200)
                    throw new Error(res.status)
            return res.json()
            }
        ).then(res=>{
            this.post_id = res.post_id
            this.title = res.title
            this.content = res.content
            this.author = res.author_name
            this.username = res.username
            this.timestamp = res.timestamp
            this.comments = res.comments
            this.likes = res.likes
            this.timestamp = res.timestamp
            this.img = res.image
            this.liked = res.liked
        }).catch(err=>{
            if (err.message == '401') {
                this.$store.dispatch('unauthorized_error')
            }
        })
    },
    methods: {
        async makeRequestWithJWT(url, options) {
            const response = await fetch(url, options);
            try {
                if (response.status == 200) {
                    const res = await response.json();
                    this.$emit('toast', 'Comment deleted')
                    return res;
                }
                if (response.status != 201)
                    throw new Error(response)
                    this.$emit('toast', 'Commented successfully!')
                    const res = await response.json();
                    this.comments.push({username: res.username, name: res.name, comment: res.comment, comment_id: res.comment_id})
                    return res;
            }
            catch(err) {
                this.$emit('toast', 'Something went wrong!')
            }
        },
        async formSubmit() {
            const url = `${this.$store.state.api_url}/post/${this.post_id}/comments?comment=${this.yourcomment}`
            const options = {
                method: 'POST',
                headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`
                },
                cache: 'default',
                mode: 'cors',
                body: {},
                credentials: 'include',
            }
            await this.makeRequestWithJWT(url, options)
        }, 
        current_user(username){
            return this.$store.state.username == username || this.$store.state.username == this.username
        },
        async removeComment(key, comment_id) {
            const url = `${this.$store.state.api_url}/comment/${comment_id}`
            const options = {
                method: 'DELETE',
                headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`
                },
                cache: 'default',
                mode: 'cors',
                body: {},
                credentials: 'include',
            }
            await this.makeRequestWithJWT(url, options)
            this.comments.splice(key, 1)
        },
        showLikesToggle() {
            if (!this.likes.length)
                return
            this.showLikes = true
        },
        async onLike() {
            this.liked = !this.liked
            const url = `${this.$store.state.api_url}/post/${this.post_id}/like`
            const options = {
                method: 'POST',
                headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`
                },
                cache: 'default',
                mode: 'cors',
                credentials: 'include',
            }
            fetch(url, options).then(res=> {
                if (res.status != 200)
                    throw new Error('Something went wrong')
                return res.json()
            }).then(res=>{
                console.log(res)
                if (res.like_status=='Liked' && this.liked) {return}
                else if(res.like_status=='Not Liked' && !this.liked) {return}
                else {this.liked = !this.liked}
            }).catch(err=>this.$emit('toast', err))
        }
    },
    components: { RouterLink, UserModal },
})

</script>

<style scoped>
.wrapper {
    display: flex;
    justify-content: center;
    gap: 1rem;
}
.feed-post {
    padding: 20px;
    text-decoration: none;
    background-color: var(--app-background);
    min-width: 20rem;
    width: 50rem;
    border-radius: 1rem;
}


.post-details {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 1rem;
}

.author {
    font-size: 0.9rem;
    font-weight: 600;
    color: #000080a1;
}

.timestamp {
    font-size: 0.75rem;
    color: #6C6C6C;
}

.title {
    display: inline-block;
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    transition: border-bottom 200ms ease-in;
}

.content {
    font-size: 1rem;
    color: #4B4B4B;
    line-height: 1.5rem;
}

.post-image {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 25rem;
    overflow: hidden;
    margin-top: 1rem;
    border-radius: 1.2rem;
}

.post-image > img {
    width: 100%;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.overlay > .overlay-back {
    position: fixed;
    top: 0;
    left: 0;
    background-color: #00003ae0;
    opacity: 0.8;
    width: 100%;
    height: 100%;
    z-index: -1;
}

.overlay > img {
    max-height: 80%;
    max-width: 90%;
    width: auto;
    height: auto;
}

.post-engagement {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 2rem;
    margin-top: 0.7rem;
}

.post-engagement > a {
    text-decoration: none;
    color: var(--secondary-color);
}

.eng {
    display: flex;
    align-items: center;
    gap: 8px;
    transition: transform 300ms;
    font-weight: 600;
    cursor: pointer;
}

.eng:hover {
    transform: scale(1.04);
}

.eng > p {
    font-size: 0.7rem;
}

.eng > svg {
    width: 18px;
    height: 20px;
    stroke: #555555;
}

.fill {
    fill: var(--secondary-color);
    stroke:var(--secondary-color) !important;
}

.comment-count {
    font-size: 0.8rem;
    padding: 1rem 1rem;
    color: var(--secondary-color);
}

form {
    padding: 0 0 0.875rem 1rem;
    display: flex;
    justify-content: flex-start;
    gap: 2rem;
    align-items: center;
}


#comment {
    font-size: 0.9rem;
    resize: none;
    background-color: var(--app-background);
    border: 2px solid rgb(212, 212, 212);   
    padding: 1rem;
    width: 100%;
    border-radius: 1rem;
    color: var(--primary-text-color);
}

#comment::placeholder {
    color: var(--secondary-text-color);
}

#comment:focus{
    outline: none;
    border: 2px solid var(--secondary-color);   
}

.search-submit > button {
    padding: 0.375rem 0.8rem;
    border: none;
    background-color: #f1f1f1; 
    color: var(--secondary-color);
    font-weight: 600;
    font-size: 0.8rem;
    border-radius: 0.5rem;
}

.comment-block {
    padding: 1rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}


.comment-user {
    display: flex;
    gap: 5px;
    font-size: 0.8rem;
}

.comment-name {
    font-weight: 700;
    color: #505050;
}

.comment-username {
    color: #7b7b7b;
}

.remove-btn {
    font-size: 0.8rem;
    color:rgb(158, 86, 86);
    cursor: pointer;
}

.comment-content {
    font-size: 0.9rem;
}
</style>