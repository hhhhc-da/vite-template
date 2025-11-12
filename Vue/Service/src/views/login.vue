<template>
  <div class="login-card">
    <h2>用户登录</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="username" placeholder="请输入用户名" required>
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="password" placeholder="请输入密码" required>
      </div>
      <button type="submit" class="login-btn">登录</button>
      <div class="error-message" v-if="error">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { setLoginCookie } from '../utils/auth'

const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')

const handleLogin = async () => {
  try {
    const response = await axios.post('http://192.168.1.72:81/login', {
      username: username.value,
      password: password.value
    });

    const { username: resName, token } = response.data;

    if (response.status === 200 && token) {
      setLoginCookie(resName, token);
      router.push('/home');
    } else {
      error.value = response.data.error || '用户名或密码错误';
    }
  } catch (err) {
    console.error('登录请求失败:', err);
    if (err.response?.data?.error) {
      error.value = err.response.data.error;
    } else {
      error.value = '网络错误，请稍后再试';
    }
  }
};
</script>

<style scoped>
.login-card {
  width: 350px;
  padding: 2rem;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #359469;
}

.error-message {
  color: #e74c3c;
  margin-top: 1rem;
  text-align: center;
}
</style>