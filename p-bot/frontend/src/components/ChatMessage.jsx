import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { FiUser, FiTool, FiMessageCircle, FiSettings, FiMapPin, FiInfo } from 'react-icons/fi';

const ChatMessage = ({ message, isUser, agent, router, imageUrl, isPartOfContext = true }) => {
  // Determine which agent is responding
  const isIssueAgent = agent === 'issue_detection';
  const isTenancyAgent = agent === 'tenancy_faq';
  
  // Get agent color classes
  const getAgentColorClasses = () => {
    if (isIssueAgent) {
      return {
        bg: 'bg-blue-50',
        icon: 'bg-blue-500 text-white',
        border: 'border-blue-200',
        text: 'text-blue-600',
        badge: 'bg-blue-100 border border-blue-200',
      };
    } else if (isTenancyAgent) {
      return {
        bg: 'bg-green-50',
        icon: 'bg-green-500 text-white',
        border: 'border-green-200',
        text: 'text-green-600',
        badge: 'bg-green-100 border border-green-200',
      };
    } else {
      return {
        bg: 'bg-gray-100',
        icon: 'bg-gray-700 text-white',
        border: 'border-gray-300',
        text: 'text-gray-600',
        badge: 'bg-gray-100 border border-gray-300',
      };
    }
  };
  
  // Get agent name
  const getAgentName = () => {
    if (isIssueAgent) {
      return 'Issue Detection Agent';
    } else if (isTenancyAgent) {
      return 'Tenancy FAQ Agent';
    } else {
      return 'P-Bot';
    }
  };
  
  // Get agent icon
  const getAgentIcon = () => {
    if (isIssueAgent) {
      return <FiTool className="h-4 w-4 mr-1" />;
    } else if (isTenancyAgent) {
      return <FiMessageCircle className="h-4 w-4 mr-1" />;
    } else {
      return <FiInfo className="h-4 w-4 mr-1" />;
    }
  };
  
  const colorClasses = !isUser ? getAgentColorClasses() : {
    bg: 'bg-blue-100',
    icon: 'bg-blue-500 text-white',
    border: 'border-blue-200',
    text: 'text-blue-600',
    badge: 'bg-blue-100 border border-blue-200',
  };
  
  // No need for these since we're handling the image directly
  // const hasImage = message.includes('*[Image attached]*');
  // const cleanMessage = message.replace('*[Image attached]*', '').trim();
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`relative max-w-xl rounded-2xl px-5 py-3 shadow-sm ${
          isUser
            ? 'bg-blue-100 text-blue-900 ml-auto rounded-br-2xl'
            : `${colorClasses.bg} text-gray-900 mr-auto rounded-bl-2xl`
        }`}
        style={{ minWidth: 80 }}
      >
        {/* Loopot logo in top-left for bot messages */}
        {!isUser && (
          <img
            src="/logo.svg"
            alt="Loopot Logo"
            className="absolute -top-4 -left-4 w-8 h-8 rounded-lg shadow border border-white bg-white"
            style={{ zIndex: 2 }}
          />
        )}
        {/* Display conversation context indicator */}
        {!isUser && isPartOfContext && (
          <div className="absolute -left-1 -top-1 w-3 h-3 bg-blue-500 rounded-full" title="Part of conversation context"></div>
        )}
      
        {/* If there's an image, show it first */}
        {imageUrl && (
          <div className="mb-2">
            <img
              src={imageUrl}
              alt={isUser ? "User uploaded image" : "Property issue visualization"}
              className="rounded-lg max-h-60 max-w-full object-contain"
            />
          </div>
        )}
        
        {/* Show the message content */}
        <div className="prose prose-sm break-words">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '');
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={dracula}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                ) : (
                  <code className={className} {...props}>
                    {children}
                  </code>
                );
              },
              img({ node, ...props }) {
                return (
                  <img
                    {...props}
                    className="max-w-full rounded-lg my-2 border border-gray-200"
                    alt={props.alt || "Image"}
                  />
                );
              },
            }}
          >
            {message}
          </ReactMarkdown>
        </div>
        
        {/* For bot messages, show which agent responded, with colored badge */}
        {!isUser && agent && (
          <div className={`mt-2 flex items-center text-xs rounded-full px-3 py-1 gap-1 ${colorClasses.badge} ${colorClasses.text} font-semibold w-fit`}> 
            {isIssueAgent ? <FiTool className="h-4 w-4 mr-1" /> : null}
            {isTenancyAgent ? <FiMessageCircle className="h-4 w-4 mr-1" /> : null}
            <span className="font-medium capitalize">
              {agent.replace('_', ' ')}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage; 