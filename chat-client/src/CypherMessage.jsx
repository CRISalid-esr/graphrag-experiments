import React, {useState} from 'react';

const CypherMessage = ({payload}) => {
    const [expanded, setExpanded] = useState(false);
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(payload);
            setCopied(true);
            setTimeout(() => setCopied(false), 1500);
        } catch (err) {
            console.error('Failed to copy', err);
        }
    };

    return (
        <div style={{
            border: '1px solid #ccc',
            borderRadius: 8,
            padding: 10,
            backgroundColor: '#f9f9f9',
            fontFamily: 'monospace'
        }}>
            <div style={{display: 'flex', gap: 10, marginBottom: expanded ? 10 : 0}}>
                <button onClick={() => setExpanded(!expanded)} style={buttonStyle}>
                    {expanded ? 'Hide Query' : 'Show Query'}
                </button>
                {expanded && <button onClick={handleCopy} style={buttonStyle}>Copy</button>}
                {expanded && copied && <span style={{fontSize: 12, color: 'green'}}>Copied!</span>}
            </div>

            {expanded && (
                <pre style={{
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    background: '#eee',
                    padding: 10,
                    borderRadius: 4,
                    fontSize: 14,
                }}>
          <code>{payload}</code>
        </pre>
            )}
        </div>
    );
};

const buttonStyle = {
    background: '#e0e0e0',
    border: 'none',
    borderRadius: 4,
    padding: '4px 8px',
    cursor: 'pointer',
};

export default CypherMessage;
