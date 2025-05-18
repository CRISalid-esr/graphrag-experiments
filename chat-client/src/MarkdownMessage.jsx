import React from 'react';

const MarkdownMessage = ({payload}) => {
    return <div dangerouslySetInnerHTML={{__html: payload}}/>
};

export default MarkdownMessage;