import {createCustomMessage} from 'react-chatbot-kit';
import CypherMessage from "./CypherMessage";
import MarkdownMessage from "./MarkdownMessage";

var initialMessage = `Bonjour, je peux vous aider à accéder aux informations sur la recherche à l'université.`;
const chatBotConfig = {
    initialMessages: [
        createCustomMessage(initialMessage, 'chatbot', {payload: initialMessage}),
    ],
    customStyles: {botMessageBox: {backgroundColor: '#376B7E',}, chatButton: {backgroundColor: '#5ccc9d',},},
    customMessages: {
        query: (props) => <CypherMessage {...props} />,
        chatbot: (props) => <MarkdownMessage {...props} />,
    },
};
export default chatBotConfig;