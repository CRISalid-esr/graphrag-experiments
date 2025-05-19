import React from 'react';
import {createCustomMessage} from "react-chatbot-kit";

const ActionProvider = ({setState, children}) => {

    const sendToGraphRag = async (messages, newMessage) => {
        try {
            // const host = 'http://localhost:8000';
            const host = '';
            // random uuid for the loading message
            const loadingMessageId = Math.random().toString(36).substring(2, 15);
            const loadingMessage = createCustomMessage('En attente de la réponse...', 'loading', {
                payload: 'En attente de la réponse...',
                loading: true,
                id: loadingMessageId,
            });
            setState((prev) => ({
                    ...prev,
                    messages: [...prev.messages, loadingMessage],
                }
            ));
            const url = `${host}/api`;
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    history: messages,
                    message: newMessage,
                })
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            const botMessage = createCustomMessage(data.reply, 'chatbot', {
                payload: data.reply,
            });
            let queryMessage = null;
            if (data.query) {
                queryMessage = createCustomMessage(data.query, 'query', {
                    payload: data.query,
                });
            }

            setState((prev) => ({
                ...prev,
                messages: [...prev.messages.filter((message) => message.type !== 'loading'), botMessage, queryMessage].filter(Boolean),
            }));
        } catch (error) {
            console.error("Error:", error);
            const errorMessage = createCustomMessage(
                "Sorry, I couldn't reach the server.",
                'chatbot',
                {payload: "Sorry, I couldn't reach the server."}
            );
            setState((prev) => ({
                ...prev,
                messages: [...prev.messages, errorMessage],
            }));
        }
    };

    return (
        <div>
            {React.Children.map(children, (child) => {
                return React.cloneElement(child, {
                    actions: {sendToGraphRag},
                });
            })}
        </div>
    );
};

export default ActionProvider;
