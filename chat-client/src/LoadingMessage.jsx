import React from 'react';

const LoadingMessage = () => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '1rem' }}>
      <svg
        width="120"
        height="24"
        viewBox="0 0 120 24"
        xmlns="http://www.w3.org/2000/svg"
        fill="#376B7E"
      >
        <circle cx="12" cy="12" r="12">
          <animate
            attributeName="r"
            from="12"
            to="12"
            begin="0s"
            dur="0.6s"
            values="12;6;12"
            calcMode="linear"
            repeatCount="indefinite"
          />
        </circle>
        <circle cx="60" cy="12" r="12">
          <animate
            attributeName="r"
            from="12"
            to="12"
            begin="0.2s"
            dur="0.6s"
            values="12;6;12"
            calcMode="linear"
            repeatCount="indefinite"
          />
        </circle>
        <circle cx="108" cy="12" r="12">
          <animate
            attributeName="r"
            from="12"
            to="12"
            begin="0.4s"
            dur="0.6s"
            values="12;6;12"
            calcMode="linear"
            repeatCount="indefinite"
          />
        </circle>
      </svg>
    </div>
  );
};

export default LoadingMessage;
