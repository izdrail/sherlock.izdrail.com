<template>
  <ion-page>
    <ion-header>
      <ion-toolbar color="primary">
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>Cyber Detect Chatbot</ion-title>
        <ion-buttons slot="end">
          <ion-button title="Clear Chat" @click="clearChat">
            <ion-icon :icon="trashOutline" slot="icon-only"></ion-icon>
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="chat-content ion-padding">
      <div class="chat-container">
        <!-- Messages List -->
        <div v-for="msg in messages" :key="msg.id" :class="['chat-bubble-wrapper', msg.sender]">
          <div class="chat-bubble">
            <div class="sender-name">{{ msg.sender === 'user' ? 'You' : 'Sherlock AI' }}</div>
            <div class="message-text">{{ msg.text }}</div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="chat-bubble-wrapper assistant">
          <div class="chat-bubble typing-bubble">
            <ion-spinner name="dots" color="primary"></ion-spinner>
          </div>
        </div>

        <!-- Suggestion Chips -->
        <div v-if="suggestions.length > 0" class="suggestions-container ion-margin-top ion-margin-bottom">
          <div class="suggestions-label">Suggested Questions:</div>
          <div class="chips-wrapper">
            <ion-chip
              v-for="(s, idx) in suggestions"
              :key="idx"
              outline
              color="primary"
              @click="sendSuggestion(s)"
            >
              <ion-label>{{ s }}</ion-label>
            </ion-chip>
          </div>
        </div>
      </div>
    </ion-content>

    <ion-footer>
      <ion-toolbar>
        <div class="input-container">
          <ion-input
            v-model="inputMessage"
            placeholder="Ask a cybersecurity question..."
            @keyup.enter="sendMessage"
            class="chat-input"
          ></ion-input>
          <ion-button color="primary" @click="sendMessage" :disabled="isTyping || !inputMessage.trim()">
            <ion-icon :icon="sendOutline" slot="icon-only"></ion-icon>
          </ion-button>
        </div>
      </ion-toolbar>
    </ion-footer>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonButtons,
  IonButton,
  IonMenuButton,
  IonContent,
  IonFooter,
  IonInput,
  IonIcon,
  IonSpinner,
  IonChip,
  IonLabel,
} from '@ionic/vue';
import { sendOutline, trashOutline } from 'ionicons/icons';
import { AssistantService } from '@/services/assistantService';
import { AssistantStorage, ChatMessageItem } from '@/services/assistantStorage';

export default defineComponent({
  name: 'Chatbot',
  components: {
    IonPage,
    IonHeader,
    IonToolbar,
    IonTitle,
    IonButtons,
    IonButton,
    IonMenuButton,
    IonContent,
    IonFooter,
    IonInput,
    IonIcon,
    IonSpinner,
    IonChip,
    IonLabel,
  },
  setup() {
    const inputMessage = ref('');
    const isTyping = ref(false);
    const conversationId = ref<string | undefined>(undefined);
    const messages = ref<ChatMessageItem[]>([]);
    const suggestions = ref<string[]>([
      'Is this email a scam?',
      'How to spot phishing?',
      'How to generate a strong password?',
      'What is 2FA?',
    ]);

    const loadHistory = () => {
      const history = AssistantStorage.getChatHistory();
      if (history.length > 0) {
        messages.value = history;
      } else {
        const welcomeMsg: ChatMessageItem = {
          id: 'welcome_' + Date.now(),
          sender: 'assistant',
          text: 'Hello! I am your AI Cybersecurity Awareness Assistant. Ask me anything about identifying phishing scams, suspicious links, or improving your digital security.',
          timestamp: new Date().toISOString(),
        };
        messages.value = [welcomeMsg];
        AssistantStorage.saveChatMessage(welcomeMsg);
      }
    };

    const sendMessage = async () => {
      const text = inputMessage.value.trim();
      if (!text || isTyping.value) return;

      const userMsg: ChatMessageItem = {
        id: 'user_' + Date.now(),
        sender: 'user',
        text,
        timestamp: new Date().toISOString(),
      };
      messages.value.push(userMsg);
      AssistantStorage.saveChatMessage(userMsg);
      inputMessage.value = '';

      isTyping.value = true;
      try {
        const response = await AssistantService.sendChatMessage(text, conversationId.value);
        conversationId.value = response.conversationId;

        const botMsg: ChatMessageItem = {
          id: 'bot_' + Date.now(),
          sender: 'assistant',
          text: response.reply,
          timestamp: new Date().toISOString(),
        };
        messages.value.push(botMsg);
        AssistantStorage.saveChatMessage(botMsg);

        if (response.suggestions && response.suggestions.length > 0) {
          suggestions.value = response.suggestions;
        }
      } finally {
        isTyping.value = false;
      }
    };

    const sendSuggestion = (suggestionText: string) => {
      inputMessage.value = suggestionText;
      sendMessage();
    };

    const clearChat = () => {
      AssistantStorage.clearChatHistory();
      messages.value = [];
      conversationId.value = undefined;
      loadHistory();
    };

    onMounted(() => {
      loadHistory();
    });

    return {
      inputMessage,
      isTyping,
      messages,
      suggestions,
      sendMessage,
      sendSuggestion,
      clearChat,
      sendOutline,
      trashOutline,
    };
  },
});
</script>

<style scoped>
.chat-content {
  --background: var(--ion-color-step-50, #121212);
}
.chat-container {
  display: flex;
  flex-direction: column;
  min-height: 100%;
}
.chat-bubble-wrapper {
  display: flex;
  margin-bottom: 12px;
}
.chat-bubble-wrapper.user {
  justify-content: flex-end;
}
.chat-bubble-wrapper.assistant {
  justify-content: flex-start;
}
.chat-bubble {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 0.95rem;
  line-height: 1.4;
}
.chat-bubble-wrapper.user .chat-bubble {
  background: var(--ion-color-primary, #0054e9);
  color: #fff;
  border-bottom-right-radius: 2px;
}
.chat-bubble-wrapper.assistant .chat-bubble {
  background: var(--ion-color-step-150, #222);
  color: var(--ion-text-color, #fff);
  border-bottom-left-radius: 2px;
}
.sender-name {
  font-size: 0.75rem;
  font-weight: bold;
  opacity: 0.8;
  margin-bottom: 4px;
}
.typing-bubble {
  display: flex;
  align-items: center;
  padding: 8px 16px;
}
.suggestions-container {
  margin-top: auto;
}
.suggestions-label {
  font-size: 0.8rem;
  color: var(--ion-color-medium, #888);
  margin-bottom: 6px;
}
.chips-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.input-container {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 4px 8px;
}
.chat-input {
  flex: 1;
}
</style>
