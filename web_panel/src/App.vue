<template>
  <div id="app">
    <el-container style="height: 100vh">
      <el-header style="background-color: #409eff; color: white; display: flex; align-items: center; justify-content: space-between">
        <div style="display: flex; align-items: center">
          <el-icon style="margin-right: 10px"><Location /></el-icon>
          <h1 style="margin: 0">GeoTrack Messenger</h1>
        </div>
        <div v-if="isAuthenticated">
          <el-button @click="logout" type="danger" plain>Logout</el-button>
        </div>
      </el-header>
      <el-container>
        <el-aside v-if="isAuthenticated" width="250px" style="background-color: #f5f5f5">
          <el-menu
            :default-active="$route.path"
            router
            background-color="#f5f5f5"
            text-color="#333"
            active-text-color="#409eff"
          >
            <el-menu-item index="/dashboard">
              <el-icon><Dashboard /></el-icon>
              <span>Dashboard</span>
            </el-menu-item>
            <el-menu-item index="/map">
              <el-icon><Location /></el-icon>
              <span>Live Map</span>
            </el-menu-item>
            <el-menu-item index="/users">
              <el-icon><User /></el-icon>
              <span>Users</span>
            </el-menu-item>
            <el-menu-item index="/locations">
              <el-icon><Position /></el-icon>
              <span>Locations</span>
            </el-menu-item>
            <el-menu-item index="/geofences">
              <el-icon><MapLocation /></el-icon>
              <span>Geofences</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    const logout = async () => {
      await authStore.logout()
      router.push('/login')
    }
    
    onMounted(() => {
      authStore.checkAuthStatus()
    })
    
    return {
      isAuthenticated,
      logout
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.el-header {
  padding: 0 20px;
}

.el-aside {
  border-right: 1px solid #e6e6e6;
}

.el-main {
  padding: 20px;
  background-color: #f9f9f9;
}
</style>
