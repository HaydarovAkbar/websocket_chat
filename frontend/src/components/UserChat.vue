<template>
  <div>
    <div v-for="msg in messages" :key="msg">{{ msg }}</div>
    <input v-model="message" @keyup.enter="sendMessage" placeholder="Type a message..."/>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ws: null,
      message: "",
      messages: [],
    };
  },
  methods: {
    connectWebSocket() {
      // this.ws = new WebSocket("ws://localhost:7000/ws/chat/");
      this.ws = new WebSocket("ws://192.168.10.189:7000/ws/chat/");
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.messages.push(data.message);
      };
    },
    sendMessage() {
      if (this.message) {
        this.ws.send(JSON.stringify({message: this.message}));
        this.message = "";
      }
    },
  },
  mounted() {
    this.connectWebSocket();
  },
};
</script>