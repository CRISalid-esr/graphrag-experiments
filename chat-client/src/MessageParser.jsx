import React from 'react';

const MessageParser = ({children, actions}) => {
    const parse = (newMessage) => {
        const messages = children?.props?.state?.messages
        actions.sendToGraphRag(messages, newMessage);

    };

    return (
        <div>
            {React.Children.map(children, (child) => {
                return React.cloneElement(child, {
                    parse: parse,
                    actions: {},
                });
            })}
        </div>
    );
};

export default MessageParser;