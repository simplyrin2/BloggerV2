<template>
    <div>
        <p :key="-1" class="msg" v-if="posts.length==0">{{msg}}</p>
        <TransitionGroup name="bounce" id="feed">
            <FeedPost v-for="(item, key) in posts" :key="key" :postData="item"></FeedPost>
        </TransitionGroup>
    </div>
</template>

<script>
import FeedPost from '@/components/FeedPost.vue';

export default({
    name: "FeedView",
    data: function() {
        return {
            posts: [],
            msg: ''
        }
    },
    components: { FeedPost },
    beforeMount() {
        this.$store.commit('changePageTitle', 'Feed')
        const options = {
          method: "GET",
          headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': "application/json",
          },
          credentials: 'include',
          }
        fetch("http://127.0.0.1:5000/api/feed", options).then(res=>{
            if (res.status != 200)
                throw new Error(res.status)
            return res.json()
            }
        ).then(res=>{
            console.log(res)
            this.posts = res
            if (res.length == 0)
                this.msg = 'Nothing to show!'
        }).catch(err=>{
            if (err.message == '401') {
                this.$store.dispatch('unauthorized_error')
            }
        })
    },
})

</script>

<style scoped>

#feed {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
}

.msg {
    text-align: center;
    padding: 1rem;
    color: var(--secondary-text-color);
    font-weight: 600;
    margin-top: 3rem;
}

.list-enter-active,
.list-leave-active {
  transition: all 500ms ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>
