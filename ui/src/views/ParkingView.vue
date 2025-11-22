<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import '../assets/parking.css'

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

const frontdoor = computed(() => ({
  loading: loading.value,
  occupied: !loading.value && status.value?.spaces.frontdoor_occupied,
  vacant: !loading.value && !status.value?.spaces.frontdoor_occupied,
  text: !loading.value && status.value?.spaces.frontdoor_occupied ? 'Occupied' : 'Vacant',
}))

const kitchen = computed(() => ({
  loading: loading.value,
  occupied: !loading.value && status.value?.spaces.kitchen_occupied,
  vacant: !loading.value && !status.value?.spaces.kitchen_occupied,
  text: !loading.value && status.value?.spaces.kitchen_occupied ? 'Occupied' : 'Vacant',
}))

onMounted(() => {
  getStatus()
})
</script>

<template>
  <div class="page">
    <h1>Parking</h1>
    <div role="doc-subtitle">Carriage Walk</div>
    <hr />
    <div class="spaces">
      <div
        class="space"
        :class="{
          occupied: frontdoor.occupied,
          vacant: frontdoor.vacant,
        }"
      >
        <h2>Front Door</h2>
        <span>
          <img
            v-if="frontdoor.loading"
            width="50"
            height="50"
            src="/img/spinner.svg"
            alt="Loading front door"
          />
          <div v-else class="text">
            {{ frontdoor.text }}
          </div>
        </span>
      </div>
      <div
        class="space"
        :class="{
          occupied: kitchen.occupied,
          vacant: kitchen.vacant,
        }"
      >
        <h2>Kitchen</h2>
        <span>
          <img
            v-if="kitchen.loading"
            width="50"
            height="50"
            src="/img/spinner.svg"
            alt="Loading kitchen"
          />
          <div v-else class="text">
            {{ kitchen.text }}
          </div>
        </span>
      </div>
    </div>
  </div>
</template>
