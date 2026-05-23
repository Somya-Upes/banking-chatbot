import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = {
      sender: "user",
      text: message,
    };

    setChat((prev) => [...prev, userMessage]);
    setMessage(""); // Clear input immediately
    setIsLoading(true); // Start loading spinner

    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
      const response = await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMessage.text,
          session_id: "frontend-user",
        }),
      });

      const data = await response.json();

      const botMessage = {
        sender: "bot",
        text: data.answer,
      };

      setChat((prev) => [...prev, botMessage]);
    } catch (error) {
      setChat((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "Error connecting to backend. Please make sure the server is awake.",
        },
      ]);
    }

    setIsLoading(false); // Stop loading spinner
  };

  return (
    <div className="app">
      <h1>Banking Support Chatbot</h1>

      <div className="chat-box">
        {chat.map((msg, index) => (
          <div
            key={index}
            className={msg.sender === "user" ? "user-msg" : "bot-msg"}
          >
            {msg.text}
          </div>
        ))}
        {isLoading && (
          <div className="bot-msg" style={{ fontStyle: "italic", opacity: 0.7 }}>
            Typing... (If server is asleep, this may take up to 50 seconds)
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Ask something..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              sendMessage();
            }
          }}
        />

        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;