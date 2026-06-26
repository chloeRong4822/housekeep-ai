<template>
  <div class="login-page">
    <div class="login-box">
      <div class="logo">
        <el-icon><House /></el-icon>
        <h2>家政AI获客中台</h2>
        <p>让获客更简单</p>
      </div>
      <el-form :model="form" class="login-form">
        <el-form-item>
          <el-input v-model="form.phone" placeholder="手机号" size="large">
            <template #prefix><el-icon><Phone /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.code" placeholder="验证码" size="large">
            <template #prefix><el-icon><Key /></el-icon></template>
            <template #append>
              <el-button @click="sendCode" :disabled="counting">{{ codeText }}</el-button>
            </template>
          </el-input>
        </el-form-item>
        <el-button type="primary" size="large" class="login-btn" @click="login">登录</el-button>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({ phone: '', code: '' })
const counting = ref(false)
const codeText = ref('获取验证码')
let timer = null

const sendCode = () => {
  if (!form.phone) return
  counting.value = true
  let count = 60
  codeText.value = `${count}s`
  timer = setInterval(() => {
    count--
    if (count <= 0) {
      clearInterval(timer)
      counting.value = false
      codeText.value = '获取验证码'
    } else {
      codeText.value = `${count}s`
    }
  }, 1000)
}

const login = () => {
  // 模拟登录
  localStorage.setItem('token', 'demo-token')
  localStorage.setItem('company', JSON.stringify({ name: '和阳家政', balance: 2580 }))
  router.push('/')
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-box {
  width: 420px;
  padding: 40px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.logo {
  text-align: center;
  margin-bottom: 30px;
}
.logo .el-icon {
  font-size: 48px;
  color: #667eea;
}
.logo h2 {
  margin-top: 12px;
  font-size: 24px;
  color: #333;
}
.logo p {
  margin-top: 8px;
  color: #999;
  font-size: 14px;
}
.login-btn {
  width: 100%;
  margin-top: 10px;
}
</style>
