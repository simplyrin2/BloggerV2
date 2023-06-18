<template>
    <Transition class="toast" name="bounce" mode="out-in">
        <div class="toast-body">
            {{ msg }}
        </div>
    </Transition>
</template>

<script>
export default({
    name: 'toasterComponent',
    props: { msg: String}
})
</script>

<style scoped>
.toast {
    position: fixed;
    bottom: 2rem;
    background-color: var(--app-background);
    padding: 0.6rem 1rem;
    border-radius: 0.8rem;
    box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}
.toast-body {
    color: var(--secondary-color);
    font-size: 0.9rem;
    font-weight: 600;
}

.bounce-enter-active {
    animation: bounce-in 200ms;
  }
.bounce-leave-active {
    animation: bounce-in 200ms reverse;
}
@keyframes bounce-in {
    0% {
        transform: translateY(100%);
        opacity: 0;
    }
    100% {
        transform: translateY(0);
        opacity: 1;
    }
}
</style>