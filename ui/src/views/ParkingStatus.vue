<script setup lang="ts">
import { onMounted, ref } from 'vue'

type Status = {
  spaces: {
    kitchen_occupied: boolean
    frontdoor_occupied: boolean
  }
}

const loading = ref(false)
const status = ref<Status>()

const getStatus = async () => {
  loading.value = true
  const res = await fetch('/api/status')
  status.value = await res.json()
  loading.value = false
}

onMounted(() => {
  getStatus()
})
</script>

<template>
  <div>
    <h1>Parking</h1>

    <div class="spaces">
      <div>
        <div>Kitchen space</div>
        <div v-if="status">{{ status.spaces.kitchen_occupied ? 'Occupied' : 'Free' }}</div>
        <div v-else>-</div>
      </div>
      <div>
        <div>Front door space</div>
        <div v-if="status">{{ status?.spaces.frontdoor_occupied ? 'Occupied' : 'Free' }}</div>
        <div v-else>-</div>
      </div>
    </div>

    <div class="actions">
      <button @click="getStatus">{{ loading ? 'Loading..' : 'Update' }}</button>
    </div>
  </div>
</template>

<style scoped>
.spaces {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin: 1rem 0;

  & > * {
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1px solid white;
    padding: 1rem;
  }
}

.actions {
  display: flex;
  justify-content: center;
}

button {
  background: #1976d2;
  color: #fff;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  padding: 0.75rem 1.5rem;
}
</style>
