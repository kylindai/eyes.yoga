
const chat_event = new EventSource('/avatar/chat');
let count = 0;
chat_event.addEventListener('greeting', (event)=> {
  const event_data = JSON.parse(event.data);
  console.log(event_data);
  if (event_data.ts > 10) {
    chat_event.close();
  }
});
