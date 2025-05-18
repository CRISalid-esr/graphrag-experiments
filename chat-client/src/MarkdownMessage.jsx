import React from 'react';
import logo from './logo.svg'; // Ensure this path is correct
import './MarkdownMessage.css';

const MarkdownMessage = ({ payload }) => {
  return (
    <div className="react-chatbot-kit-chat-bot-message-container">
      <div className="react-chatbot-kit-chat-bot-avatar">
        <div className="react-chatbot-kit-chat-bot-avatar-container">
          <img
            src={logo}
            alt="Crisalid"
            style={{
              height: '100%',
              width: '100%',
              objectFit: 'contain',
              borderRadius: '50%',
            }}
          />
        </div>
      </div>
      <div className="react-chatbot-kit-chat-bot-message">
        <div dangerouslySetInnerHTML={{ __html: payload }} />
        <div className="react-chatbot-kit-chat-bot-message-arrow"></div>
      </div>
    </div>
  );
};

export default MarkdownMessage;
