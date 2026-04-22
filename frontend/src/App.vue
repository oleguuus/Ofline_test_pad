<script setup lang="ts">
import { ref, onMounted } from 'vue'
import Dashboard from './components/Dashboard.vue'

// Управление темной темой
const isDark = ref(false)

const toggleTheme = () => {
  isDark.value = !isDark.value
  updateTheme()
}

const updateTheme = () => {
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

// Восстановление темы при загрузке
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    updateTheme()
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100 font-sans transition-colors duration-200">
    <header class="bg-white dark:bg-gray-800 shadow-md p-4 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-indigo-600">LocalTest Admin</h1>
        <button @click="toggleTheme" class="bg-gray-200 dark:bg-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition shadow-sm font-medium">
          {{ isDark ? 'Лайт' : 'Дарк' }} Мод
        </button>
      </div>
    </header>
    <main class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
      <Dashboard />
    </main>
  </div>
</template>

