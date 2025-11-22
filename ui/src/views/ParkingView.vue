<script setup lang="ts">
import '../assets/parking.css'
</script>

<template>
  <div class="page">
    <h1>Parking</h1>
    <div role="doc-subtitle">Carriage Walk</div>
    <hr />
    <div class="spaces">
      <div class="space occupied">
        <h2>Front Door</h2>
        <span>
          <div class="text">Occupied</div>
        </span>
      </div>
      <div class="space vacant">
        <h2>Kitchen</h2>
        <span>
          <div class="text">Vacant</div>
        </span>
      </div>
    </div>
  </div>
</template>
