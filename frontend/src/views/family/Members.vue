<template>
  <ion-page>
    <ion-header :translucent="true">
      <ion-toolbar>
        <ion-buttons slot="start">
          <ion-menu-button color="primary"></ion-menu-button>
        </ion-buttons>
        <ion-title>Family</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-fab vertical="top" horizontal="end" slot="fixed">
      <ion-fab-button @click="setOpen(true)">
        <ion-icon :icon="add"></ion-icon>
      </ion-fab-button>
    </ion-fab>

    <ion-content :fullscreen="true">
      <div id="container">
        <!-- Modal for Adding Member -->
        <ion-modal :is-open="isOpen" @ion-modal-did-dismiss="setOpen(false)">
          <ion-header>
            <ion-toolbar>
              <ion-title>Add a Member</ion-title>
              <ion-buttons slot="end">
                <ion-button @click="setOpen(false)">Close</ion-button>
              </ion-buttons>
            </ion-toolbar>
          </ion-header>

          <ion-content class="ion-padding">
            <form @submit.prevent="addMember()">
              <ion-item>
                <ion-label position="floating">Name</ion-label>
                <ion-input v-model="name" type="text" required></ion-input>
              </ion-item>
              <ion-item>
                <ion-label position="floating">Email</ion-label>
                <ion-input v-model="email" type="email" required></ion-input>
              </ion-item>
              <ion-item>
                <ion-label position="floating">Phone</ion-label>
                <ion-input v-model="phone" type="tel" required></ion-input>
              </ion-item>
              <ion-button type="submit" color="primary" expand="block" class="ion-margin-top">
                Add
              </ion-button>
            </form>
          </ion-content>
        </ion-modal>

        <!-- List of Family Members -->
        <ion-list>
          <ion-item v-for="(member, index) in members" :key="index">
            <ion-label>
              <h2>{{ member.name }}</h2>
              <p>{{ member.email }}</p>
              <p>{{ member.phone }}</p>
            </ion-label>
          </ion-item>
        </ion-list>
      </div>
    </ion-content>
  </ion-page>
</template>

<style scoped>
#container {
  padding: 1rem;
}
</style>
<script lang="ts" setup>
import { add } from 'ionicons/icons';
import { ref, onMounted } from 'vue';

// Modal State
const isOpen = ref(false);
const setOpen = (open: boolean) => (isOpen.value = open);

// Individual form fields
const name = ref('');
const email = ref('');
const phone = ref('');

// Family Members List
const members = ref<Array<{ name: string; email: string; phone: string }>>([]);

// Load Members from LocalStorage on Mounted
onMounted(() => {
  const storedMembers = localStorage.getItem('familyMembers');
  if (storedMembers) {
    members.value = JSON.parse(storedMembers);
  }
});



// Add Member Function
const addMember = () => {
  console.log('Add member');
  setOpen(false);
  console.log(name)
  console.log(email)
  console.log(phone)

  // Trim fields
  const trimmedName = name.value.trim();
  const trimmedEmail = email.value.trim();
  const trimmedPhone = phone.value.trim();

  console.log(trimmedName)
  console.log(trimmedEmail)
  console.log(trimmedPhone)


  // Add to members array
  members.value.push({ name: trimmedName, email: trimmedEmail, phone: trimmedPhone });

  // Save to localStorage
  localStorage.setItem('familyMembers', JSON.stringify(members.value));

  // Reset form and close modal
  name.value = '';
  email.value = '';
  phone.value = '';
  setOpen(false);
  alert('Member added successfully!');
};
</script>