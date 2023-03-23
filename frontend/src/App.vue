<script setup>
import { ref } from 'vue'

const file = ref(null)  // The file ref
const step = ref(0)     // Divide into several steps
// 0: Submit file
// 1: Uploading
// 2: Finding shortest
// 3: Waiting for best
// 4: Got odd
const result_id = ref(-1) // Get the result id from Celery
const last_error = ref("")
const odd = ref(0)

function reinit() {
  step.value = 0
  file.value = null
  last_error.value = ""
}

function cancelCurrentOperation() {
  reinit()
  last_error.value = "You have cancelled the last operation"
}

// Retrieve the file object for later loading
function handleFileChange(e) {
  file.value = e.target.files[0]
}

// Consult celery on the result
function queryMinOdd(id) {
  fetch("/api/retrieve-max-odd?id=" + id)
    .then((response) => response.json())
    .then((res) => {
      console.log(res)
      switch (res.error) {
        case 0:
          odd.value = res.odd
          step.value = 4
          break
        case 1:
          // Continue
          break
        case 2:
          reinit()
          last_error.value = "Cannot submit the empire plan, please retry"
          break
        default:
          break
      }
    })
    .catch((error) => {
      reinit()
      last_error.value = "Cannot submit the empire plan, please retry"
    })
}

function keepQueryMinOdd(id) {
  queryMinOdd(id)
  if (step.value == 3)
    setTimeout(keepQueryMinOdd, 500, id)
}

function onEmpirePlanSubmit(res) {
  if (res.error !== 0) {
    // Clean up
    reinit()
    last_error.value = "Cannot resolve the empire plan, please retry"
    return
  }
  // Shortest found
  if (res.min_day === 0) {
    // That is not possible
    step.value = 4
    odd.value = 0
    return
  }
  step.value = 3
  // Poll the min odd API endpoint
  setTimeout(keepQueryMinOdd, 500, res.id)
}

// Load and submit the plan to endpoint
function submitEmpirePlan() {
  // Clear error msg
  last_error.value = ""

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

        step.value = 2
        // Send to API endpoint
        fetch("/api/empire-plan-uploader", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: res.target.result
        })
        .then((response) => response.json())
        .then(onEmpirePlanSubmit)
        .catch((error) => {
          // Clean up
          reinit()
          console.log(error)
          last_error.value = "Cannot submit the empire plan, please retry"
        })
      } catch (error) {
        // Clean up
        reinit()
        last_error.value = "Cannot decode the empire plan, select another one"
        return
      }
    }.bind(this)
    reader.onerror = function(err) {
      last_error.value = "Cannot read the file, select another one"
    }.bind(this)
    reader.readAsText(file.value)
  } else {
    reinit()
    last_error.value = "Please select a file containing the empire plan"
  }
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
    <p v-if="step===4 && odd > 0">You can make it!</p>
    <p v-if="step===4 && odd == 0">You can not beat the Death Star...</p>
    <p v-if="step===4">Odd: {{ odd }}</p>
    <button v-if="step > 0 && step < 4" type="button" @click="cancelCurrentOperation">Cancel</button>
    <button v-if="step===4" type="button" @click="reinit">Retry</button>
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
