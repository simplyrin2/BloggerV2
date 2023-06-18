<template>
    <form @submit.prevent="formSubmit" action="" method="POST" class="post-form" enctype="multipart/form-data">
                <div class="input title-block">
                  <textarea v-model="title" type="text" name="title" id="title" placeholder="Title" maxlength="50" rows="1" required></textarea>
                  <span class="tooltip">{{ title.length }}/50</span>
                </div>
                <div class="input content-block">
                  <textarea v-model="content" type="text" name="content" id="content" placeholder="Content" maxlength="500"></textarea>
                  <span class="tooltip">{{ content.length }}/500</span>
                </div>
                <div class="create-img">
                    <input @change="displayImg" ref="fileInput" type="file" name="image" id="fileInput"  accept=".png, .jpg, .jpeg" hidden="hidden" class="upload-input">
                    <div class="img-input">
                        <div v-show="!img" @click="uploadImg" class="imgInput-placeholder">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 9V12M12 12V15M12 12H15M12 12H9M21 12C21 13.1819 20.7672 14.3522 20.3149 15.4442C19.8626 16.5361 19.1997 17.5282 18.364 18.364C17.5282 19.1997 16.5361 19.8626 15.4442 20.3149C14.3522 20.7672 13.1819 21 12 21C10.8181 21 9.64778 20.7672 8.55585 20.3149C7.46392 19.8626 6.47177 19.1997 5.63604 18.364C4.80031 17.5282 4.13738 16.5361 3.68508 15.4442C3.23279 14.3522 3 13.1819 3 12C3 9.61305 3.94821 7.32387 5.63604 5.63604C7.32387 3.94821 9.61305 3 12 3C14.3869 3 16.6761 3.94821 18.364 5.63604C20.0518 7.32387 21 9.61305 21 12Z" stroke="#0000ca8e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>   
                            <p id="img-placeholder-text">Image</p>
                        </div>
                        <img src="" id="img-preview" ref="imgPreview">  
                    </div>
                    <div v-show="img" @click="removeImg" id="cancel">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="#4B4B4B" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>   
                    </div>
                  </div>
                <div class="create-submit">
                  <button type="submit">
                    <span v-show="!submitting">Post</span>
                    <div v-show="submitting" class="lds-dual-ring"></div>
                  </button>
                </div>
              </form>
</template>

<script>
export default({
    name: 'CreateView',
    data: function() {
        return {
            title: '',
            content: '',
            img: false,
            submitting: false,
        }
    },
    computed: {
        len_title() {
            return this.title.length
        }
    },
    methods: {
        uploadImg() {
            this.$refs.fileInput.click()
        },
        displayImg() {
            console.log(this.$refs.fileInput.files[0])
            const file = this.$refs.fileInput.files[0]
            if (!file) return
            const fileReader = new FileReader();
            fileReader.addEventListener('load', (e) => {
            this.$refs.imgPreview.src = e.target.result;
            this.$refs.imgPreview.style.width='100%';
            });
            fileReader.readAsDataURL(file);
            this.img = true
        },
        removeImg() {
            this.$refs.fileInput.value = null
            this.$refs.imgPreview.src = ''
            this.img = false
        },
        async makeRequestWithJWT(url, options) {
            const response = await fetch(url, options).catch(()=>{
                this.submitting = false
                this.$emit('toast', 'Something went wrong!')
                return;
            });
            if (response.status === 201){
                this.$router.replace({name: 'profile'})
                this.$emit('toast', 'Post created successfully!')
            }
            else {
                this.submitting = false
                this.$emit('toast', 'Something went wrong!')
            }
            const result = await response.json();
            return result;
        },
        async formSubmit(e) {
            this.submitting = true
            const data = new FormData(e.target)
            for (const [name,value] of data) {
                console.log(name, ":", value)
                console.log(name, value)
            }
            const url = `http://127.0.0.1:5000/api/post`
            const options = {
                method: 'POST',
                headers: {
                "Authorization": `Bearer ${localStorage.getItem('token')}`
                },
                cache: 'default',
                mode: 'cors',
                body: data,
                credentials: 'include',
            }
            await this.makeRequestWithJWT(url, options)
            this.submitting = false
        }
    },
    beforeMount() {
        this.$store.commit('changePageTitle', 'Create Post')
    }
})

</script>

<style scoped>
form {
    padding: 0 1.75rem;
}

.input {
    position: relative;
}

.title-block {
    margin-bottom: 0.5rem;
}

#title {
    font-size: 1.5rem;
    font-weight: 600;
    resize: none;
    background-color: var(--app-background);
    border: 2px solid rgb(212, 212, 212);   
    padding: 1rem;
    width: 100%;
    border-radius: 0.5rem;
    color: var(--primary-text-color);
}

#title::placeholder {
    color: var(--secondary-text-color);
}

#title:focus, #content:focus {
    outline: none;
    border: 2px solid var(--secondary-color);   
}


#content {
    font-size: 1.2rem;
    color: var(--primary-text-color);
    line-height: 1.3rem;
    border: none;
    resize: none;
    border: 2px solid rgb(212, 212, 212);   
    padding: 1rem;
    width: 100%;
    height: 15rem;
    border-radius: 0.5rem;
}


#content::placeholder {
    color: var(--secondary-text-color-color)
}

.post-image {
    width: 100%;
    height: 13.5rem;
    overflow: hidden;
    margin-top: 1rem;
}

.post-image > img {
    width: 100%;
}

.create-img {
    position: relative;
    width: 50%;
}

.img-input  {
    width: 100%;
    height: 16rem;
    overflow: hidden;
    margin-top: 1rem;
    background-color: #ffff;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    border: 2px solid rgb(212,212,212);
    border-radius: 1.2rem;
}

.imgInput-placeholder {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    position: absolute;
    color: var(--primary-text-color);
    cursor: pointer;
}

#cancel {
    width: 24px;
    height: 24px;
    border-radius: 50px;
    background-color: #ffff;

    position: absolute;
    right: -10px;
    top: -10px;
    opacity: 0.8;
}

#image-preview {
    width: 100%;
}


.create-submit {
    display: flex;
    justify-content: flex-end;
    margin-top: 1.31rem;
}

.create-submit > button {
    padding: 0.5rem 1.7rem;
    border: none;
    background-color: var(--primary-gray);
    color: #eeeeee;
    font-size: 1rem;
    border-radius: 0.8rem;
}

.tooltip {
    position: absolute;
    right: 0.5rem;
    bottom: 0.5rem;
    color: var(--secondary-text-color);
    font-size: 0.8rem;
}

</style>