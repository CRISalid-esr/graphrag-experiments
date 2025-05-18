import './App.css';
import 'react-chatbot-kit/build/main.css';
import Chatbot from "react-chatbot-kit";
import MessageParser from "./MessageParser";
import ActionProvider from "./ActionProvider";
import chatBotConfig from "./ChatBotConfig";

import logo from './logo.svg';
import gplLogo from './GPLv3_Logo.svg';

function App() {
    return (
        <div className="App">
            <header className="Sticky-header">
                <img src={logo} alt="Crisalid logo" className="Header-logo"/>
                <div className="Header-title">
                    <strong>Consortium CRISalid</strong><br/>
                    LLM powered Current Research Information Systems
                </div>
            </header>

            <div className="App-body">
                <Chatbot
                    config={chatBotConfig}
                    messageParser={MessageParser}
                    actionProvider={ActionProvider}
                    headerText="Prototype d'agent conversationnel sur graphe de connaissance"
                    placeholderText="Posez votre question ici"
                />
            </div>

            {/* Sticky GPL Logo in Bottom-Right */}
            <img src={gplLogo} alt="GPLv3 Logo" className="GPL-sticky-logo"/>
        </div>
    );
}

export default App;
