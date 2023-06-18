<template>
    <div>
        <TransitionGroup id="container" name="bounce">
            <div v-for="(item,key) in notifications" :key="key" class="notification">
                <RouterLink :to="path(item)" class="wrapper">
                    <div class="details">
                        <p class="content">{{ item.content }}</p>
                        <p class="timestamp" style="opacity: 0.8">{{ item.timestamp }}</p>                                 
                    </div>
                </RouterLink>
                <div class="action-btn">
                    <a @click="clear(item.not_id, key)"><i class="bi bi-x-circle-fill"></i></a>
                </div>
            </div>
        </TransitionGroup>
        <p class="msg" v-show="showmsg">No notifications!!</p>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router'

export default({
    name: "NotificationsView",
    data: function () {
        return {
            notifications: [],
            showmsg: false,
        };
    },
    methods: {
        fetchNotifications() {
            if (this.query === "")
                return;
            this.submitted = true;
            const options = {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("token")}`,
                    "Content-Type": "application/json",
                },
                credentials: "include",
            };
            fetch(`${this.$store.state.api_url}/notifications`, options).then(res => {
                if (res.status != 200)
                    throw new Error(res.status);
                return res.json();
            }).then(res => {
                this.notifications = [];
                this.notifications = res;
                if (this.notifications.length == 0)
                    this.showmsg = true
            }).catch(err => {
                if (err.message == "401") {
                    this.$store.dispatch("unauthorized_error");
                }
            });
        },
        path(n) {
            if (n.type==0)
                return `/profile/${n.username}`
            else
                return `/post/${n.id}`
        },
        clear(id, key) {
            const options = {
                method: "DELETE",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("token")}`,
                    "Content-Type": "application/json",
                },
                credentials: "include",
            };
            fetch(`${this.$store.state.api_url}/notifications/${id}`, options).then(res => {
                if (res.status != 200)
                    throw new Error(res.status);
                this.notifications.splice(key, 1)
                if (!this.notifications.length) this.showmsg=true
                return res.json();
            }).catch(err => {
                if (err.message == "401") {
                    this.$store.dispatch("unauthorized_error");
                }
                else {
                    this.$emit('toast', 'Something went wrong')
                }
            });
        }
    },
    beforeMount() {
        this.$store.commit("changePageTitle", "Notifications")
        this.fetchNotifications()
    },
    components: { RouterLink }
})

</script>

<style scoped>
#container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

.notification {
    background-color: var(--app-background);
    border: 2px solid rgb(218, 218, 218);
    padding: 1rem;
    width: 40rem;
    border-radius: 1.2rem;
    display: flex;
    justify-content: space-between;
}

.wrapper {
    text-decoration: none;
}

.details {
    display: flex;
    justify-content: flex-start;
    gap: 1rem;
    align-items: center;
    color: var(--primary-text-color);
}

.timestamp {
    font-size: 0.8rem;
}

.msg {
    text-align: center;
    padding: 1rem;
    color: var(--secondary-text-color);
    font-weight: 600;
    margin-top: 3rem;
}

.action-btn > a{
    opacity: 0.4;
}
</style>