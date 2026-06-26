<template>
  <el-container class="layout">
    <el-aside width="220px" class="sidebar">
      <div class="sidebar-logo">
        <el-icon><House /></el-icon>
        <span>AI获客中台</span>
      </div>
      <el-menu :default-active="$route.path" router class="sidebar-menu" background-color="#1a1a2e" text-color="#b8c5d6" active-text-color="#fff">
        <el-menu-item index="/dashboard">
          <el-icon><DataLine /></el-icon>
          <span>数据看板</span>
        </el-menu-item>
        <el-menu-item index="/leads">
          <el-icon><List /></el-icon>
          <span>AI线索看板</span>
        </el-menu-item>
        <el-menu-item index="/content">
          <el-icon><MagicStick /></el-icon>
          <span>AI内容工厂</span>
        </el-menu-item>
        <el-menu-item index="/nannies">
          <el-icon><User /></el-icon>
          <span>阿姨管理</span>
        </el-menu-item>
        <el-menu-item index="/insight">
          <el-icon><TrendCharts /></el-icon>
          <span>数据洞察</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-left">{{ $route.name }}</div>
        <div class="header-right">
          <el-tag type="success" effect="dark">余额: ¥{{ company.balance }}</el-tag>
          <el-dropdown>
            <span class="user-info">
              <el-avatar :size="32" icon="User" />
              {{ company.name }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>账户设置</el-dropdown-item>
                <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const company = reactive(JSON.parse(localStorage.getItem('company') || '{}'))

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.layout { min-height: 100vh; }
.sidebar {
  background: #1a1a2e;
  color: #fff;
}
.sidebar-logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.sidebar-logo .el-icon { font-size: 28px; color: #667eea; }
.sidebar-menu { border-right: none; }
.header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.header-left { font-size: 18px; font-weight: bold; color: #333; }
.header-right { display: flex; align-items: center; gap: 16px; }
.user-info { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.main { background: #f5f7fa; padding: 20px; }
</style>
