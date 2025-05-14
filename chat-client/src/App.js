import './App.css';
import 'react-chatbot-kit/build/main.css'
import Chatbot from "react-chatbot-kit";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import chatBotConfig from "./ChatBotConfig";

function App() {
    return (<div>
        <Chatbot
            config={chatBotConfig}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
            headerText="Prototype d'agent conversationnel sur graphe de connaissance"
            placeholderText="Posez votre question ici"
        />
    </div>);
}

export default App;
