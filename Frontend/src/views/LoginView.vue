<template>
    <div>
        <div class="container">
        <div class="col nav">
            <div class="col-1">
                <div class="header">
                    <h2>Blogger</h2>
                    <form @submit="login" action="/login" method="POST" class="post-form" autocomplete="off">
                        <div class="input-block">
                            <input v-model="username" class="input" type="text" name="username" id="username" placeholder="username" maxlength="20" required>
                        </div>
                        <div class="input-block">
                            <input v-model="password" class="input" type="password" name="password" id="password" placeholder="password" maxlength="20" required>
                        </div>
                        <div class="search-submit">
                            <button type="submit" class="button">Login</button>
                        </div>
                      </form>
                      <RouterLink to="/signup">Don't have an account? <strong>Signup</strong></RouterLink>
                </div>
            </div>
        </div>
    </div>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';

export default({
    name: 'LoginView',
    // beforeCreate() {
    //     this.$store.commit('hideSidebar', true)
    // },
    data: function() {
        return {
            username: '',
            password: ''
        }
    },
    beforeMount() {
        this.$store.commit('changePageTitle', 'Login')
    },
    components: {
        RouterLink
    },
    methods: {
        async login(e) {
            e.preventDefault()
            console.log(this.username)
            console.log(this.password)
            await fetch('http://127.0.0.1:5000/api/access_token',
            {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify({username: this.username, password: this.password}),
            credentials: 'include',
            }
            ).then((res) => {
                if (res.status != 200)
                    throw new Error(res.status)
                return res.json()
            }).then((res) => {
                localStorage.setItem('token', res.token)
                this.$store.commit('login', true)
                this.$store.commit('changeUsername', res.username)
                this.$emit('toast', 'Logged in successfully!')
                if (!this.$route.query.redirect)
                    this.$router.replace({name: 'feed'})
                else
                    this.$router.replace(this.$route.query.redirect)
            }).catch(err => { console.log(err)
                this.$emit('toast', 'Something went wrong!')
             })
        }
    }
})

</script>

<style scoped>

.container {
    display: flex;
    gap: 15px;
    width: 100%;
    justify-content: center;
}

.col {
    display: inline-block;
}


.col-1 {
    padding: 5.7rem;
    position: sticky;
    top:0;
}

.header {
    display: flex; 
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    height: 50vh;
    justify-content: center;
} 

.g1 {
    display: flex;
    flex-direction: column; 
    gap: 3.875rem;
    align-items: center;
}

.header-links {
    display: block;
    padding: 0.5rem;
    text-decoration: none;
    color: #1E1E1E;
}

.col-2 {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin-top: 5rem;
    width: 29.125rem;
    overflow-y: auto;
}

h2 {
    margin-bottom: 2rem;
    color: var(--primary-gray);
}

form {
    padding: 0 0 0.875rem 1.625rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

a {
    text-decoration: none;
    color: var(--secondary-text-color)
}

.input {
    font-size: 1.2rem;
    color: var(--primary-text-color);
    resize: none;
    background-color: var(--app-background);
    border: 2px solid rgb(190, 190, 190);
    padding: 1rem;
    width: 100%;
    border-radius: 0.8rem;
    transition: all 200ms ease;
}

.input::placeholder {
    color: #CCCCCC;
}

input {
    width: 100%;
}

input:focus {
    outline: none;
    border: 2px solid rgb(117, 117, 117);
}

.search-submit {
    width: 100%;
}

.search-submit > .button {
    padding: 0.8rem 1.25rem;
    font-size: 1.2rem;
    background-color: var(--primary-gray);
    color: #fafafa;
    width: 100%;
    transition: background-color 200ms;
    font-weight: 700;
    border: 2px solid var(--primary-gray);
    border-radius: 0.5rem;
}

.search-submit > .button:hover {
    cursor: pointer;
    background-color: #ffff;
    color: var(--primary-gray);
}

.action-btn > a{
    display: inline-block;
    text-decoration: none;
    background-color: #F1F1F1;
    color: #4D4D4D;
    padding: 0.5rem 0.8125rem;
    font-size: 0.7rem;
    font-weight: 700;
}

.action {
    text-decoration: none;
    color: #a3a3a3;
}

.error-message {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: rgb(200, 0, 0);
    margin-top: 5px;
    font-size: 0.8rem;
}

#close-icon:hover {
    cursor: pointer;
}

</style>