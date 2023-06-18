<template>
    <div>
        <div class="col nav">
            <div class="col-1">
                <div class="header">
                    <h2>Edit Profile</h2>
                <form @submit.prevent="formSubmit" method="POST" class="post-form" enctype="multipart/form-data" autocomplete="off">
                    <div class="create-img">
                        <input @change="displayImg" ref="fileInput" type="file" name="image" id="fileInput"  accept=".png, .jpg, .jpeg" hidden="hidden" class="upload-input">
                        <div class="img-input">
                            <div v-show="!img" @click="uploadImg" class="imgInput-placeholder">
                                <i class="bi bi-plus"></i>
                                <p id="img-placeholder-text">Profile Image</p>
                            </div>
                            <img :src="imgPath" id="img-preview" ref="imgPreview">   
                        </div>
                        <div v-show="img" @click="removeImg" id="cancel">
                            <i class="bi bi-x-circle"></i> 
                        </div>
                    </div>
                    <div class="input-block username-input">
                        <input @input="checkUsername" v-model="username" class="input" type="text" name="username" id="username" placeholder="Username" maxlength="20" required>
                        <span class="tooltip" v-show="usernametooltip && !validUsername">Invalid username</span>
                    </div>
                    <div class="input-block name-input">
                        <input @input="checkName" v-model="name" class="input" type="text" name="name" id="name" placeholder="Name" maxlength="30" required>
                        <span class="tooltip" v-show="nametooltip && !validName">Invalid name</span>
                    </div>
                    <div class="input-block name-input">
                        <input @input="checkEmail" v-model="email" class="input" type="email" name="email" id="email" placeholder="Email" maxlength="40">
                        <span class="tooltip" v-show="emailtooltip && !validEmail">Invalid email</span>
                    </div>
                    <div class="input-block">
                        <textarea v-model="bio" type="text" name="bio" class="input" id="bio" placeholder="Bio" maxlength="80" rows="3"></textarea>
                    </div>
                    <div class="search-submit">
                        <button type="submit" class="button">
                            <span v-show="!submitting">Save</span>
                            <div v-show="submitting" class="lds-dual-ring"></div>
                        </button>
                    </div>
                    </form>
            </div>
        </div>
    </div>
</div>
</template>

<script>

export default({
    name: 'LoginView',
    data : function() {
        return {
            username: '',
            name: '',
            bio: '',
            img: false,
            email: '',
            imgPath: '', 
            imgChange: false,
            imgPresent: false,
            usernametooltip: false,
            nametooltip: false,
            emailtooltip: false,
            submitting: false,
        }
    },
    async beforeMount() {
        this.$store.commit('changePageTitle', 'Edit Profile')
        const options = {
            method: 'GET',
            headers: {
            "Authorization": `Bearer ${localStorage.getItem('token')}`
            },
            cache: 'default',
            mode: 'cors',
            credentials: 'include',
        }
        const url = `${this.$store.state.api_url}/user`
        const res = await this.makeRequestWithJWT(url, options)
        this.name = res.name
        this.username = res.username
        this.email = res.email
        if (res.pic != '') {
            this.imgPath = res.pic
            this.img = true
        }
    },
    computed: {
        validUsername() {
            const re = /^[a-zA-Z0-9]*$/
            return re.test(this.username)
        },
        validName() {
            const re = /^[a-zA-Z]+(\s?[a-zA-Z])*$/
            return re.test(this.name)
        },
        validEmail() {
            if (this.email == '' || this.email == null) return true
            const re = /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/
            return re.test(this.email)
        }
    },
    methods: {
        uploadImg() {
            this.$refs.fileInput.click()
        },
        displayImg() {
            this.imgChange = true
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
            this.imgChange = true
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
            if (response.status == 201) {
                this.$router.replace({name: 'profile'})
                this.$emit('toast', 'Changes saved successfully')
            }
            if (response.status/100 == 4) {
                this.submitting = false
                this.$emit('toast', 'Something went wrong')
            }
            const result = await response.json();
            return result;
        },
        async formSubmit(e) {
            if (!this.validName || !this.validUsername || !this.validEmail)
                return
            this.submitting = true
            const data = new FormData(e.target)
            data.append('imgChanged', this.imgChange)
            for (const [name,value] of data) {
                console.log(name, value)
            }
            console.log(data)
            const url = `${this.$store.state.api_url}/user`
            const options = {
                method: 'PUT',
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
        },
        checkName() {
            this.nametooltip = true
        },
        checkUsername() {
            this.usernametooltip = true
        },
        checkEmail() {
            this.emailtooltip = true
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
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
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

h2 {
    margin-bottom: 2rem;
    color: var(--primary-gray);
}

form {
    padding: 0 0 0.875rem 1.625rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

a {
    text-decoration: none;
    color: var(--secondary-text-color)
}

.input-block {
    position: relative;
    padding-bottom: 0.85rem;
}

.input {
    font-size: 1rem;
    color: var(--primary-text-color);
    resize: none;
    background-color: var(--app-background);
    border: 2px solid rgb(190, 190, 190);
    padding: 1rem;
    border-radius: 0.8rem;
    transition: all 200ms ease;
    position: relative;
    width: 20rem;
}


.input::placeholder {
    color: #CCCCCC;
}

input {
    height: 3.5rem;
}

input:focus, #bio:focus {
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

#close-icon:hover {
    cursor: pointer;
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
    width: 8rem;
    height: 8rem;
    overflow: hidden;
    margin-bottom: 1rem;
    background-color: #ffff;
    display: flex;
    justify-content: center;
    border: 1px solid #e8e8ff;
    border-radius: 100rem;
}

.imgInput-placeholder {
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    color: var(--primary-text-color);
}

#cancel {
    width: 24px;
    height: 24px;
    border-radius: 50px;
    background-color: #ffff;
    position: absolute;
    right: -5px;
    top: 5px;
    opacity: 0.8;
    display: flex;
    justify-content: center;
    align-items: center;
}

#image-preview {
    width: 100%;
}

.tooltip {
    position: absolute;
    font-size: 0.7rem;
    font-weight: 600;
    color: rgb(200, 0, 0) !important;
    bottom: 0;
    left: 0;
} 

.lds-dual-ring:after {
border: 3px solid #8e8e8e;
border-color: #b4b4b4 transparent #a5a5a5 transparent;

}
</style>