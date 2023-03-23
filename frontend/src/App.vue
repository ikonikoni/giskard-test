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

// Retrieve the file object for later loading
function handleFileChange(e) {
  file.value = e.target.files[0]
}

// TODO: Load and submit the plan to endpoint
function submitEmpirePlan() {
  // Check file and send to the API endpoint
  if (file.value != null) {
    step.value = 1

    // Read file
    const reader = new FileReader();
    reader.onload = function(res) {
      // Parse as json
      try {
        console.log(res.target.result)
        const empire_plan_json = JSON.parse(res.target.result)

        // Check countdown
        if (empire_plan_json.countdown === undefined) {
          throw new Error()
        }
        // Check bounty_hunter_plan
        if (empire_plan_json.bounty_hunters === undefined) {
          throw new Error()
        }

        console.log(empire_plan_json)
        // TODO: Send to API endpoint
      } catch (error) {
        // Clean up
        step.value = 0
        file.value = null
        last_error.value = "Cannot decode the empire plan, select another one"
        return
      }
    }.bind(this)
    reader.onerror = function(err) {
      last_error.value = "Cannot read the file, select another one"
    }.bind(this)
    reader.readAsText(file.value)
  } else {
    step.value = 0
    last_error.value = "Please select a file containing the empire plan"
  }
  // step.value = 2

  // TODO: When getting the id of Celery task
  // step.value = 3
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
