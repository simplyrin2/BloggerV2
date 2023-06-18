<template>
    <p>{{ error_msg }}</p>
</template>

<script>
export default({
    name: 'NotificationsView',
    data: function() {
        return {
            error_msg: 'Internal Server Error'
        }
    },
    beforeMount() {
        this.$store.commit('changePageTitle', '')
    }
})

</script>

<style scoped>
p {
    text-align: center;
    color: var(--secondary-text-color);
    font-weight: 600;
    font-size: 1.2rem;
}
</style>
