import './App.css';
import 'react-chatbot-kit/build/main.css'
import Chatbot from "react-chatbot-kit";
import chatBotConfig from "./ChatBotConfig";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";

function App() {
    return (
        <div className="App">
            <Chatbot
                config={chatBotConfig}
                messageParser={MessageParser}
                actionProvider={ActionProvider}
            />
        </div>
    );
}

export default App;
