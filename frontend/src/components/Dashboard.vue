<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface Test {
  id: number;
  title: string;
  description: string | null;
  time_limit_minutes: number | null;
  tags_json: { tags: string[] } | null;
  created_at: string;
}

const tests = ref<Test[]>([])
const isModalOpen = ref(false)

// Форма создания теста
const newTestForm = ref({
  title: '',
  description: '',
  time_limit_minutes: null as number | null
})

// Загрузка списка тестов с бэкенда
const loadTests = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/tests/')
    tests.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке тестов:', error)
  }
}

// Создание нового теста
const createTest = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/tests/', {
      title: newTestForm.value.title,
      description: newTestForm.value.description || null,
      time_limit_minutes: newTestForm.value.time_limit_minutes || null
    })
    
    // Реактивно обновляем список
    tests.value.unshift(response.data)
    
    // Закрываем модалку и чистим форму
    isModalOpen.value = false
    newTestForm.value = { title: '', description: '', time_limit_minutes: null }
  } catch (error) {
    console.error('Ошибка при создании теста:', error)
  }
}

// Удаление теста
const deleteTest = async (id: number) => {
  if (!confirm('Вы уверены, что хотите удалить этот тест?')) return
  
  try {
    await axios.delete(`http://localhost:8000/api/tests/${id}`)
    tests.value = tests.value.filter(test => test.id !== id)
  } catch (error) {
    console.error('Ошибка при удалении теста:', error)
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('ru-RU', {
    day: '2-digit', month: 'long', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

onMounted(() => {
  loadTests()
})
</script>

<template>
  <div>
    <!-- Заголовок и кнопка создания -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold dark:text-gray-100">Управление тестами</h2>
      <button @click="isModalOpen = true" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg shadow-md transition font-medium">
        + Создать тест
      </button>
    </div>

    <!-- Модальное окно (Создание) -->
    <div v-if="isModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-xl w-full max-w-md m-4">
        <h3 class="text-lg font-bold mb-4">Новый тест</h3>
        
        <form @submit.prevent="createTest" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">Название <span class="text-red-500">*</span></label>
            <input v-model="newTestForm.title" type="text" required
                   class="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-500 bg-gray-50 dark:bg-gray-700 dark:border-gray-600" />
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Описание</label>
            <textarea v-model="newTestForm.description" rows="3"
                      class="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-500 bg-gray-50 dark:bg-gray-700 dark:border-gray-600"></textarea>
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Лимит времени (минуты)</label>
            <input v-model="newTestForm.time_limit_minutes" type="number" min="1"
                   class="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-500 bg-gray-50 dark:bg-gray-700 dark:border-gray-600" />
          </div>
          
          <div class="flex justify-end space-x-3 mt-6">
            <button type="button" @click="isModalOpen = false"
                    class="px-4 py-2 border rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 dark:border-gray-600 transition">
              Отмена
            </button>
            <button type="submit" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition">
              Создать
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Сетка тестов -->
    <div v-if="tests.length === 0" class="text-center py-10 text-gray-500 dark:text-gray-400">
      Тестов пока нет. Создайте свой первый тест!
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="test in tests" :key="test.id" 
           class="bg-white dark:bg-gray-800 rounded-xl shadow p-5 hover:shadow-lg transition-shadow border border-gray-100 dark:border-gray-700 relative group">
        
        <!-- Кнопка удаления (иконка корзины) -->
        <button @click="deleteTest(test.id)" class="absolute top-4 right-4 text-gray-400 hover:text-red-500 transition opacity-0 group-hover:opacity-100" title="Удалить тест">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
        </button>

        <h3 class="font-bold text-lg mb-2 pr-8 truncate">{{ test.title }}</h3>
        
        <p class="text-sm text-gray-500 dark:text-gray-400 mb-4 line-clamp-2 min-h-[40px]">
          {{ test.description || 'Нет описания' }}
        </p>

        <!-- Теги -->
        <div class="flex flex-wrap gap-2 mb-4">
          <span v-for="tag in (test.tags_json?.tags || [])" :key="tag" 
                class="px-2 py-1 text-xs bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 rounded">
            #{{ tag }}
          </span>
          <span v-if="test.time_limit_minutes" 
                class="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200 rounded">
            ⏱ {{ test.time_limit_minutes }} мин
          </span>
        </div>

        <div class="mt-auto pt-4 border-t border-gray-100 dark:border-gray-700 text-xs text-gray-400">
          Создан: {{ formatDate(test.created_at) }}
        </div>
      </div>
    </div>
  </div>
</template>
