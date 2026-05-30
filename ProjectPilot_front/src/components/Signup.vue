<script setup>
import '@fortawesome/fontawesome-free/css/all.css'
import { ref } from 'vue'
import { createUserWithEmailAndPassword } from 'firebase/auth'
import { doc, setDoc, serverTimestamp } from 'firebase/firestore'
import { auth, db } from '@/firebase'

const shake = ref(false)
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const usernameError = ref('')
const emailError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')
const authError = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const emit = defineEmits(['switch-to-login', 'signup-success'])
const triggerShake = () => {
  shake.value = true
  setTimeout(() => {
    shake.value = false
  }, 400)
}
const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}
const signup = async () => {
  usernameError.value = ''
  emailError.value = ''
  passwordError.value = ''
  confirmPasswordError.value = ''
  authError.value = ''

  if (!username.value) {
    usernameError.value = 'Username is required'
    triggerShake()
    return
  }

  if (!email.value) {
    emailError.value = 'Email is required'
    triggerShake()
    return
  }

  if (!isValidEmail(email.value)) {
    emailError.value = 'Invalid email format'
    triggerShake()
    return
  }

  if (!password.value) {
    passwordError.value = 'Password is required'
    triggerShake()
    return
  }

  if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match'
    triggerShake()
    return
  }

  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email.value, password.value)
    
    await setDoc(doc(db, 'users', userCredential.user.uid), {
      username: username.value,
      email: email.value,
      created_at: serverTimestamp()
    })
    
  } catch (error) {
    const code = error?.code
    if (code === 'auth/email-already-in-use') {
      authError.value = 'This email is already registered'
    } else if (code === 'auth/weak-password') {
      passwordError.value = 'Password should be at least 6 characters'
    } else {
      authError.value = 'Sign up failed'
    }
  }
}
</script>

<template>
  <form class="form" @submit.prevent="signup" :class="{ shake }">
    <h1>Create an account</h1>
    
    <div class="flex-column">
      <label>Username</label>
    </div>
    <div class="inputForm" :class="{ error: usernameError }">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" viewBox="0 0 448 512" height="20"><path d="M224 256c70.7 0 128-57.3 128-128S294.7 0 224 0 96 57.3 96 128s57.3 128 128 128zm89.6 32h-16.7c-22.2 10.2-46.9 16-72.9 16s-50.6-5.8-72.9-16h-16.7C60.2 288 0 348.2 0 422.4V464c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48v-41.6c0-74.2-60.2-134.4-134.4-134.4z"/></svg>
      <input placeholder="Choose a Username" v-model="username" class="input" type="text">
    </div>
    <p v-if="usernameError" class="error-text">{{ usernameError }}</p>

    <div class="flex-column">
      <label>Email</label>
    </div>
    <div class="inputForm" :class="{ error: emailError }">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" viewBox="0 0 32 32" height="20"><g data-name="Layer 3" id="Layer_3"><path d="m30.853 13.87a15 15 0 0 0 -29.729 4.082 15.1 15.1 0 0 0 12.876 12.918 15.6 15.6 0 0 0 2.016.13 14.85 14.85 0 0 0 7.715-2.145 1 1 0 1 0 -1.031-1.711 13.007 13.007 0 1 1 5.458-6.529 2.149 2.149 0 0 1 -4.158-.759v-10.856a1 1 0 0 0 -2 0v1.726a8 8 0 1 0 .2 10.325 4.135 4.135 0 0 0 7.83.274 15.2 15.2 0 0 0 .823-7.455zm-14.853 8.13a6 6 0 1 1 6-6 6.006 6.006 0 0 1 -6 6z"></path></g></svg>
      <input placeholder="Enter your Email" v-model="email" class="input" type="text">
    </div>
    <p v-if="emailError" class="error-text">{{ emailError }}</p>

    <div class="flex-column">
      <label>Password</label>
    </div>
    <div class="inputForm" :class="{ error: passwordError }">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" viewBox="-64 0 512 512" height="20"><path d="m336 512h-288c-26.453125 0-48-21.523438-48-48v-224c0-26.476562 21.546875-48 48-48h288c26.453125 0 48 21.523438 48 48v224c0 26.476562-21.546875 48-48 48zm-288-288c-8.8125 0-16 7.167969-16 16v224c0 8.832031 7.1875 16 16 16h288c8.8125 0 16-7.167969 16-16v-224c0-8.832031-7.1875-16-16-16zm0 0"></path><path d="m304 224c-8.832031 0-16-7.167969-16-16v-80c0-52.929688-43.070312-96-96-96s-96 43.070312-96 96v80c0 8.832031-7.167969 16-16 16s-16-7.167969-16-16v-80c0-70.59375 57.40625-128 128-128s128 57.40625 128 128v80c0 8.832031-7.167969 16-16 16zm0 0"></path></svg>        
      <input placeholder="Enter your Password" v-model="password" class="input" :type="showPassword ? 'text' : 'password'">
      <div class="eye-icon" @click="showPassword = !showPassword">
        <i :class="showPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'" />
      </div>
    </div>
    <p v-if="passwordError" class="error-text">{{ passwordError }}</p>

    <div class="flex-column">
      <label>Confirm Password</label>
    </div>
    <div class="inputForm" :class="{ error: confirmPasswordError }">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" viewBox="-64 0 512 512" height="20"><path d="m336 512h-288c-26.453125 0-48-21.523438-48-48v-224c0-26.476562 21.546875-48 48-48h288c26.453125 0 48 21.523438 48 48v224c0 26.476562-21.546875 48-48 48zm-288-288c-8.8125 0-16 7.167969-16 16v224c0 8.832031 7.1875 16 16 16h288c8.8125 0 16-7.167969 16-16v-224c0-8.832031-7.1875-16-16-16zm0 0"></path><path d="m304 224c-8.832031 0-16-7.167969-16-16v-80c0-52.929688-43.070312-96-96-96s-96 43.070312-96 96v80c0 8.832031-7.167969 16-16 16s-16-7.167969-16-16v-80c0-70.59375 57.40625-128 128-128s128 57.40625 128 128v80c0 8.832031-7.167969 16-16 16zm0 0"></path></svg>        
      <input placeholder="Confirm your Password" v-model="confirmPassword" class="input" :type="showConfirmPassword ? 'text' : 'password'">
      <div class="eye-icon" @click="showConfirmPassword = !showConfirmPassword">
        <i :class="showConfirmPassword ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'" />
      </div>
    </div>
    <p v-if="confirmPasswordError" class="error-text">{{ confirmPasswordError }}</p>

    <p v-if="authError" class="error-text">{{ authError }}</p>

    <button class="button-submit" type="submit">Sign Up</button>
    <p class="p">Already have an account? <span class="span" @click="$emit('switch-to-login')">Log In</span></p>
  </form>
</template>

<style scoped>
h1 {
  align-self: center;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background-color: #ffffff;
  padding: 30px;
  width: 450px;
  border-radius: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
::placeholder {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
.form button {
  align-self: flex-end;
}
.flex-column > label {
  color: #151717;
  font-weight: 600;
}

.inputForm {
  border: 1.5px solid #ecedec;
  border-radius: 10px;
  height: 50px;
  display: flex;
  align-items: center;
  padding-left: 10px;
  transition: 0.2s ease-in-out;
}
.input {
  margin-left: 10px;
  border-radius: 10px;
  border: none;
  width: 100%;
  height: 100%;
}

.input:focus {
  outline: none;
}

.inputForm:focus-within {
  border: 1.5px solid #2d79f3;
}

.flex-row {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  justify-content: space-between;
}

.flex-row > div > label {
  font-size: 14px;
  color: black;
  font-weight: 400;
}
.span {
  font-size: 14px;
  margin-left: 5px;
  color: #2d79f3;
  font-weight: 500;
  cursor: pointer;
}
.button-submit {
  margin: 20px 0 10px 0;
  background-color: #1570EF;
  border: none;
  color: white;
  font-size: 15px;
  font-weight: 500;
  border-radius: 10px;
  height: 50px;
  width: 100%;
  cursor: pointer;
}
.p {
  text-align: center;
  color: black;
  font-size: 14px;
  margin: 5px 0;
}

.btn {
  margin-top: 10px;
  width: 100%;
  height: 50px;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 500;
  gap: 10px;
  border: 1px solid #ededef;
  background-color: white;
  cursor: pointer;
  transition: 0.2s ease-in-out;
}
.btn:hover {
  border: 1px solid #2d79f3;
}
.eye-icon {
  cursor: pointer;
  padding: 0 10px;
  user-select: none;
  font-size: 18px;
}
.error-text {
  color: #ff4d4f;
  font-size: 13px;
  margin-top: 5px;
  margin-left: 5px;
  text-align: left;
  font-weight: bold;
}
.inputForm.error {
  border: 2px solid #ff4d4f;
}
@keyframes shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-6px); }
  50% { transform: translateX(6px); }
  75% { transform: translateX(-6px); }
  100% { transform: translateX(0); }
}
.form.shake {
  animation: shake 0.35s ease-in-out;
}
</style>
