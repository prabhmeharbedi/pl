import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { FiUser, FiTool, FiMessageCircle } from 'react-icons/fi';

const ChatMessage = ({ message, isUser, agent, router }) => {
  // Determine which agent is responding
  const isIssueAgent = agent === 'issue_detection';
  const isTenancyAgent = agent === 'tenancy_faq';
  
  // Get agent color classes
  const getAgentColorClasses = () => {
    if (isIssueAgent) {
      return {
        bg: 'bg-issue-agent-light',
        icon: 'bg-issue-agent text-white',
        border: 'border-issue-agent',
      };
    } else if (isTenancyAgent) {
      return {
        bg: 'bg-tenancy-agent-light',
        icon: 'bg-tenancy-agent text-white',
        border: 'border-tenancy-agent',
      };
    } else {
      return {
        bg: 'bg-gray-100',
        icon: 'bg-gray-700 text-white',
        border: 'border-gray-300',
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
      return <FiTool className="h-4 w-4" />;
    } else if (isTenancyAgent) {
      return <FiMessageCircle className="h-4 w-4" />;
    } else {
      return 'P';
    }
  };
  
  const colorClasses = !isUser ? getAgentColorClasses() : {
    bg: 'bg-blue-100',
    icon: 'bg-blue-500 text-white',
    border: 'border-blue-300',
  };
  
  return (
    <div className={`p-4 rounded-lg mb-4 max-w-4xl ${
      isUser 
        ? 'bg-blue-100 ml-auto' 
        : colorClasses.bg
    } border ${isUser ? 'border-blue-200' : colorClasses.border}`}>
      <div className="flex items-start">
        <div className={`rounded-full w-8 h-8 flex items-center justify-center ${
          isUser 
            ? 'bg-blue-500 text-white' 
            : colorClasses.icon
        }`}>
          {isUser ? <FiUser className="h-4 w-4" /> : getAgentIcon()}
        </div>
        <div className="ml-3 flex-1">
          <div className="font-semibold flex items-center">
            {isUser ? 'You' : getAgentName()}
            
            {/* Show routing information if available */}
            {!isUser && router && (
              <span className="ml-2 text-xs font-normal text-gray-500 bg-gray-100 py-1 px-2 rounded">
                {router.explanation}
              </span>
            )}
          </div>
          <div className="mt-1 prose prose-sm max-w-none">
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
                }
              }}
            >
              {message}
            </ReactMarkdown>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage; 