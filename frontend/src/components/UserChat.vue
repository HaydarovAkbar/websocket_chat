<!--<template>-->
<!--  <div>-->
<!--    <div v-for="msg in messages" :key="msg">{{ msg }}</div>-->
<!--    <input v-model="message" @keyup.enter="sendMessage" placeholder="Type a message..."/>-->
<!--  </div>-->
<!--</template>-->

<!--<script>-->
<!--export default {-->
<!--  data() {-->
<!--    return {-->
<!--      ws: null,-->
<!--      message: "",-->
<!--      messages: [],-->
<!--    };-->
<!--  },-->
<!--  methods: {-->
<!--    connectWebSocket() {-->
<!--      // this.ws = new WebSocket("ws://localhost:7000/ws/chat/");-->
<!--      // this.ws = new WebSocket("ws://192.168.10.189:7000/ws/chat/");-->
<!--      this.ws = new WebSocket("ws://192.168.10.30:7000/ws/chat/");-->
<!--      this.ws.onmessage = (event) => {-->
<!--        const data = JSON.parse(event.data);-->
<!--        this.messages.push(data.message);-->
<!--      };-->
<!--    },-->
<!--    sendMessage() {-->
<!--      if (this.message) {-->
<!--        this.ws.send(JSON.stringify({message: this.message}));-->
<!--        this.message = "";-->
<!--      }-->
<!--    },-->
<!--  },-->
<!--  mounted() {-->
<!--    this.connectWebSocket();-->
<!--  },-->
<!--};-->
<!--</script>-->

<template>
  <div>
    <div v-if="!isAuthenticated">
      <!-- Login Form -->
      <h2>Login</h2>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="login">Login</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
    <div v-else>
      <!-- Chat Interface -->
      <div class="chat-header">
        <h2>Welcome, {{ username }}</h2>
        <button @click="logout">Logout</button>
      </div>
      <div class="chat-window">
        <div v-for="(msg, index) in messages" :key="index" class="message">
          <span :class="{ 'own-message': msg.sender === 'self' }">{{ msg.sender }}: {{ msg.message }}</span>
        </div>
      </div>
      <input
          v-model="message"
          @keyup.enter="sendMessage"
          placeholder="Type a message..."
      />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ws: null, // WebSocket instance
      username: "",
      password: "",
      isAuthenticated: false,
      message: "",
      messages: [],
      errorMessage: "",
    };
  },
  methods: {
    login() {
      // Simulate login (replace with API call to authenticate user)
      if (this.username.trim() && this.password.trim()) {
        this.isAuthenticated = true;
        this.connectWebSocket();
        this.errorMessage = "";
      } else {
        this.errorMessage = "Please enter valid username and password.";
      }
    },
    logout() {
      this.isAuthenticated = false;
      this.ws.close();
      this.ws = null;
      this.username = "";
      this.password = "";
      this.messages = [];
      this.message = "";
    },
    connectWebSocket() {
      this.ws = new WebSocket(`ws://192.168.10.30:7000/ws/chat/`);
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.messages.push(data);
      };
      this.ws.onopen = () => {
        console.log("WebSocket connected");
      };
      this.ws.onclose = () => {
        console.log("WebSocket closed");
      };
      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };
    },
    sendMessage() {
      if (this.message.trim()) {
        const messageData = { sender: "self", message: this.message.trim() };
        this.ws.send(JSON.stringify(messageData));
        this.messages.push(messageData);
        this.message = "";
      }
    },
  },
  // destroyed() {
  //   if (this.ws) {
  //     this.ws.close();
  //   }
  // },
};
</script>

<style scoped>
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.chat-window {
  border: 1px solid #ccc;
  height: 300px;
  overflow-y: scroll;
  padding: 10px;
  margin-bottom: 10px;
}
.message {
  margin: 5px 0;
}
.own-message {
  font-weight: bold;
  color: blue;
}
.error {
  color: red;
}
</style>
