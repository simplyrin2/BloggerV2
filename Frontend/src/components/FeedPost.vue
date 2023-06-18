<template>
<div class="feed-post">
    <div class="post-details">
        <RouterLink :to="path" class="author">{{ author }}</RouterLink>
        <p class="timestamp">{{ timestamp }}</p>
    </div>
    <RouterLink class="wrapper" :to="postPath" >
        <div class="post-content">
            <p class="title">{{ title }}</p>
            <p class="content">{{ content }}</p>    
        </div>
        <div v-if="isImage" class="post-image">
            <img :src="pimg" />
        </div>
    </RouterLink>
    <div class="post-engagement">
        <a @click="onLike" class="like eng">
            <svg width="16" class="like-icon" :class="{'fill': liked}" height="14" viewBox="0 0 16 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M2.2385 1.7385C1.9251 2.0519 1.67649 2.42396 1.50688 2.83343C1.33727 3.24291 1.24997 3.68178 1.24997 4.125C1.24997 4.56821 1.33727 5.00709 1.50688 5.41656C1.67649 5.82604 1.9251 6.1981 2.2385 6.5115L8 12.273L13.7615 6.5115C14.3944 5.87856 14.75 5.02011 14.75 4.125C14.75 3.22989 14.3944 2.37144 13.7615 1.7385C13.1286 1.10556 12.2701 0.749978 11.375 0.749978C10.4799 0.749978 9.62144 1.10556 8.9885 1.7385L8 2.727L7.0115 1.7385C6.6981 1.4251 6.32604 1.17649 5.91657 1.00688C5.50709 0.837268 5.06822 0.749969 4.625 0.749969C4.18179 0.749969 3.74291 0.837268 3.33343 1.00688C2.92396 1.17649 2.5519 1.4251 2.2385 1.7385V1.7385Z" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <p class="like-count">{{likes}}</p>    
        </a>                    
        <a class="comment eng">
            <svg width="16" height="15" viewBox="0 0 16 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 5.5H5.0075M8 5.5H8.0075M11 5.5H11.0075M5.75 10H2.75C2.35218 10 1.97064 9.84196 1.68934 9.56066C1.40804 9.27936 1.25 8.89782 1.25 8.5V2.5C1.25 2.10218 1.40804 1.72064 1.68934 1.43934C1.97064 1.15804 2.35218 1 2.75 1H13.25C13.6478 1 14.0294 1.15804 14.3107 1.43934C14.592 1.72064 14.75 2.10218 14.75 2.5V8.5C14.75 8.89782 14.592 9.27936 14.3107 9.56066C14.0294 9.84196 13.6478 10 13.25 10H9.5L5.75 13.75V10Z" stroke="" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>                            
            <p class="comment-count">{{comments}}</p>    
        </a>
        <RouterLink :to="editPath" v-show="profileView" class="delete-btn comment eng">
            <i class="bi bi-pencil-square"></i>                           
            <p class="comment-count">Edit</p>    
        </RouterLink>
        <a @click="deletePost" v-show="profileView" class="delete-btn comment eng">
            <i class="bi bi-trash3-fill"></i>                            
            <p class="comment-count">Delete</p>    
        </a>
    </div>
</div>
</template>

<script>
import { RouterLink } from 'vue-router';
// import ProfileIcon from './ProfileIcon.vue';



export default ({
    name: "FeedPost",
    data: function () {
        return {
            title: this.postData.title,
            content: this.postData.content,
            pimg: this.postData.img,
            timestamp: this.postData.timestamp,
            author: this.postData.author_name,
            username: this.postData.author_username,
            postID: this.postData.post_id,
            likes: this.postData.likes,
            comments: this.postData.comments,
            deleteModal: true,
            liked: this.postData.liked
        }
    },
    computed: {
        path: function() {
            return '/profile/'+this.username
        },
        postPath: function() {
            return '/post/'+this.postID
        },
        isImage() {
            if (this.pimg === "" || this.pimg === null)
                return false
            return true
        },
        editPath() {
            return '/post/edit/'+this.postID
        }
    },
    methods: {
        async deletePost() {
            const options = {
            method: "DELETE",
            headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': "application/json",
            },
            credentials: 'include',
            }
            await fetch(`${this.$store.state.api_url}/post/${this.postID}`, options).then(res=>{
                    if (res.status != 200)
                        throw new Error(res.status)
                return res.json()
                }
            ).then(res=>{
                console.log(res)
                this.$emit('postDeleted')
                this.$emit('toast', 'Post deleted successfully')
            }).catch(err=>{
                if (err.message == '401') {
                    this.$store.dispatch('unauthorized_error')
                    this.$emit('toast', 'Something went wrong')
                }
            })
        },
        async onLike() {
            this.liked = !this.liked
            if (this.liked)
                this.likes += 1
            else
                this.likes -= 1
            const url = `${this.$store.state.api_url}/post/${this.postID}/like`
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
    props: {
        postData: Object, profileView: {type: Boolean, default: false},
    },
    components: { RouterLink }
})

</script>

<style scoped>
.feed-post {
    border: 2px solid rgb(255, 255, 255);
    padding: 20px;
    text-decoration: none;
    border-radius: 0.5rem;
    background-color: #ffffff;
    transition: all 100ms ease-out;
    /* box-shadow: 0 0 10px rgba(0, 0, 0, 0.15); */
}

.feed-post:hover {
    border: 2px solid rgb(190, 190, 190);
}

.wrapper {
    display: flex;
    justify-content: space-between;
    text-decoration: none;
    color: #000000;
    gap: 1rem;
}


.post-details {
    display: flex;
    gap: 10px;
    align-items: center;
    margin-bottom: 1rem;
}

.author {
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--tertiary-color);
}

.timestamp {
    font-size: 0.75rem;
    color: var(--secondary-text-color);
}

.title {
    display: inline-block;
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    border-bottom: 1.5px solid transparent;
    transition: border-bottom 200ms ease-in;
    color: var(--primary-text-color);
}



.content {
    font-size: 1rem;
    color: var(--secondary-text-color);
    line-height: 1.3rem;
}

.post-image {
    min-width: 15rem;
    width: 15rem;
    background-color: #dadada;
    height: 8rem;
    overflow: hidden;
    margin-top: 1rem;
    border-radius: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.post-image > img {
    width: 100%;
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
    color: var(--tertiary-color);
}

.eng {
    display: flex;
    align-items: center;
    gap: 8px;
    transition: transform 300ms;
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
    stroke: var(--secondary-color) !important;
}

.delete-btn {
    cursor: pointer;
}

.delete-btn > i {
    font-size: 1rem;
    opacity: 0.5;
}

@media only screen and (max-width: 700px) {
    .wrapper {
        flex-direction: column;
    }
    .post-image {
        width: 100%;
        height: 16rem;
    }
}
</style>