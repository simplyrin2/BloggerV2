<template>
    <div>
        <form @submit.prevent="onSubmit" action="" method="POST" class="post-form" autocomplete="off">
                <div class="input title-block">
                  <input v-model="query" type="text" name="title" id="title" placeholder="Search" maxlength="50" rows="1"/>
                  <div class="create-submit">
                  <button type="submit"><i class="bi bi-search"></i></button>
                </div>
                </div>
        </form>
        <div id="search-results-container">
            <TransitionGroup class="results" name="bounce">
                <ProfileBlock v-for="(item,key) in results" :key="key" :name="item.name" :username="item.username" :profile_img="item.pic"></ProfileBlock>
            </TransitionGroup>
            <p v-show="!results.length && showmsg">{{ msg }}</p>
        </div>
    </div>
</template>

<script>
import ProfileBlock from '@/components/ProfileBlock.vue';

export default({
    name: "SearchView",
    data: function () {
        return {
            query: "",
            results: [],
            msg: "No users found",
            showmsg: false,
        };
    },
    methods: {
        onSubmit() {
            if (this.query == '') return
            this.showmsg = true;
                const options = {
            method: "GET",
            headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': "application/json",
            },
            credentials: 'include',
            }
            fetch(`${this.$store.state.api_url}/user?search=${this.query}`, options).then(res=>{
                    if (res.status != 200)
                        throw new Error(res.status)
                return res.json()
                }
            ).then(res=>{
                console.log(res)
                this.results=[]
                this.results = res
            }).catch(err=>{
                if (err.message == '401') {
                    this.$store.dispatch('unauthorized_error')
                }
            })
        }
    },
    beforeMount() {
        this.$store.commit("changePageTitle", "Search");
    },
    components: { ProfileBlock }
})

</script>

<style scoped>
form {
    padding: 0 1.75rem;
    text-align: center;
}

.input {
    position: relative;
}

.title-block {
    margin-bottom: 0.5rem;
    position: relative;
}

#title {
    font-size: 1rem;
    font-weight: 600;
    resize: none;
    background-color: var(--app-background);
    border: 2px solid rgb(190, 190, 190);   
    padding: 1rem;
    width: 22rem;
    height: 3.5rem;
    border-radius: 10rem 0 0 10rem;
    color: var(--primary-text-color);
}

#title::placeholder {
    color: var(--secondary-text-color);
}

#title:focus, #content:focus {
    outline: none;
}

.create-submit {
    display: inline-block;
}

.create-submit > button {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem 1rem;
    border: none;
    border-radius: 0 10rem 10rem 0;
    background-color: var(--app-background);
    color: #eeeeee;
    font-size: 1rem;
    width: 3.5rem;
    height: 3.5rem;
}

.create-submit > button > i {
    font-size: 1.2rem;
    color: var(--primary-gray);
    -webkit-text-stroke: 0.2px;
}

#search-results-container {
    margin-top: 2rem;
    text-align: center;
}

.results {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    text-align: left;
}

#search-results-container > p{
    font-weight: 600;
    font-size: 0.8rem;
    color: var(--secondary-text-color);
}

.bounce-enter-active {
    animation: bounce-in 200ms;
  }
  .bounce-leave-active {
    animation: bounce-in 100ms reverse;
  }
  @keyframes bounce-in {
    0% {
      transform: translateY(-5%);
      opacity: 0;
    }
    100% {
      transform: translateY(0);
      opacity: 1;
    }
  }
</style>