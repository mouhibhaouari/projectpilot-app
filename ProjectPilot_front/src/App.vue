<script setup lang="ts">
import { ref } from 'vue'
import FolderSelector from '@/components/FolderSelector.vue'
import Console from '@/components/Console.vue';
import Login from '@/components/Login.vue';
import Signup from '@/components/Signup.vue';
import { auth } from '@/firebase'
import { onAuthStateChanged, signOut } from 'firebase/auth'

const isLoggedIn = ref(false) 
const isAuthReady = ref(false)
const currentAuthScreen = ref('login')

onAuthStateChanged(auth, (user) => {
  isLoggedIn.value = !!user
  if (!user) {
    currentAuthScreen.value = 'login'
  }
  isAuthReady.value = true
})

const handleLogout = () => {
  signOut(auth)
}
</script>
<template>
  <div class="container">
     <div class="logo">
        <img src="./assets/logo.svg" alt="">
      </div>
      <button v-if="isAuthReady && isLoggedIn" @click="handleLogout" class="signout-btn">
        Sign Out
      </button>
    <Transition name="fade" mode="out-in">
      <div v-if="!isAuthReady" class="loading-screen">
          <div class="loading-box">
  <div class="WH animation color"></div>
  <div class="WH animation color"></div>
  <div class="WH animation color"></div>
</div>
      </div>
      <div v-else-if="!isLoggedIn" class="login-screen">
        <Transition name="fade" mode="out-in">
          <Login 
            v-if="currentAuthScreen === 'login'"
            @login-success="isLoggedIn = true"
            @switch-to-signup="currentAuthScreen = 'signup'"
          />
          <Signup 
            v-else-if="currentAuthScreen === 'signup'"
            @switch-to-login="currentAuthScreen = 'login'"
          />
        </Transition>
      </div>
      <div v-else class="main-content">
        <div class="folder-selector">
          <FolderSelector />
        </div>
        <div class="console">
          <Console />
        </div>
      </div>
    </Transition>
  </div>
</template>
<style scoped>
  .container {
    position: relative;
    width: 100%;
    height: 100vh; 
    background-color: #050A24;
    background-image: url("./assets/bg.png");
    background-size: cover;
    background-position: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding-top: 100px;
  }
.console {
    width: 85%;
    max-width: 1000px;
    height: 45vh;
    margin-bottom: 40px;
  }
  .logo {
    position: absolute;
    top: 80px;
    left: 80px;
    z-index: 100;
  }

  .logo img {
    width: 163px;
    height: 53px;
    object-fit: contain;
  }

  .signout-btn {
    position: absolute;
    top: 80px;
    right: 80px;
    z-index: 100;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: 10px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 500;
    transition: all 0.3s ease;
    font-family: inherit;
  }

  .signout-btn:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-1px);
  }

  .folder-selector {
    width: 85%;
    max-width: 1000px;
    background-color: whitesmoke;
    border-radius: 12px;
    padding: 18px 35px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
  }

  @media (max-width: 1400px) {
    .container {
      padding-top: 90px;
    }

    .logo {
      top: 20px;
      left: 25px;
    }

    .signout-btn {
      top: 20px;
      right: 25px;
    }

    .logo img {
      width: 150px;
      height: 48px;
    }

    .folder-selector {
      width: 88%;
      padding: 16px 30px;
    }
  }

  @media (max-width: 1024px) {
    .container {
      padding-top: 80px;
    }

    .logo {
      top: 15px;
      left: 20px;
    }

    .signout-btn {
      top: 15px;
      right: 20px;
      padding: 8px 18px;
      font-size: 14px;
    }

    .logo img {
      width: 130px;
      height: 42px;
    }

    .folder-selector {
      width: 90%;
      padding: 14px 25px;
    }
  }
  .login-screen {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.main-content {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
/* From Uiverse.io by TemRevil */ 
.loading-box {
  width: 150px;
  height: 150px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.WH {
  width: 20px;
  height: 70px;
}
.color {
  background-color: #3395ff;
}
.animation {
  animation: Loading 1s infinite cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

@keyframes Loading {
  0% {
    height: 0;
  }
  25% {
    height: 70px;
  }
  50% {
    height: 70px;
    transform: rotate(-10deg);
  }
  75% {
    height: 70px;
    transform: rotate(10deg);
  }
  100% {
    height: 0;
  }
}
.loading-screen {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    width: 100vw;
}
</style>