<script setup>
import { ref } from 'vue'

const file = ref(null)  // The file ref
const step = ref(0)     // Divide into several steps
// 0: Submit file
// 1: Uploading
// 2: Found shortest
// 3: Waiting for best
// 4: Got odd
const result_id = ref(-1) // Get the result id from Celery
const last_error = ref("")

// Retrieve the file object for loading
function handleFileChange(e) {
  file = e.target.files[0]
  console.log(file)
  // console.log(this.$emit('input', e.target.files[0]))
}

// TODO: Load and submit the plan to endpoint
function submitEmpirePlan() {
  // TODO: Check and send
  step.value = 1
  console.log(step.value)
  step.value = 2

  // TODO: When getting the id of Celery task
  step.value = 3
}

// TODO: Consult celery on the result
function retrieve_min_ood() {

  // TODO: On retrieve result
  step.value = 4
  odd.value = 100
}
</script>

<template>
  <div class="card">
      <h2>Welcome to</h2>
      <h1>Millennium Falcon</h1>
      <h2>Console</h2>
      <p style="color:red;">{{ last_error }}</p>
  </div>
  <div class="card" id="empire-plan-uploader" v-if="step===0">
    <p>Please send me the top-secret file of the empire:</p>
    <input type="file" @change="handleFileChange"/>
    <br>
    <button type="button" @click="submitEmpirePlan">Submit</button>
  </div>
  <div class="card" id="result-keeper" v-else>
    <p v-if="step!=4">Processing...</p>
    <p v-if="step===1">Loading plan</p>
    <p v-if="step===2">Finding the shortest path</p>
    <p v-if="step===3">Finding the less risky path</p>
    <p v-if="step===4">Odd: {{ odd }}</p>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
</style>
