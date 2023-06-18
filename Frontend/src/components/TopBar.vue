<template>
    <header>
        <p>{{ title }}</p>
    </header>
</template>

<script>
export default({
    name: 'TopBar',
    computed: {
        title() {
            return this.$store.state.title
        }
    }
})
</script>

<style scoped>
p {
    margin-left: 6rem;
    font-weight: 600;
    color: var(--primary-text-color);
}

header {
    width: 100%;
    height: 2.5rem;
    border-bottom: 2px solid rgb(221, 221, 221);
    display: flex;
    align-items: center;
    position: sticky;
    top: 0;
    background-color: var(--app-background);
    z-index: 1;
}
</style>