import React from 'react';
import { User, Bot, AlertTriangle, FileText } from 'lucide-react';

const Message = ({ message }) => {
  const { role, content, sources, isError } = message;
  const isUser = role === 'user';

  const Icon = isUser ? User : (isError ? AlertTriangle : Bot);
  const bgColor = isUser ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100';
  const alignment = isUser ? 'self-end' : 'self-start';
  const iconColor = isUser ? 'text-white' : 'text-blue-600 dark:text-blue-500';
  
  if (isError) {
     bgColor = 'bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-200';
  }

  return (
    <div className={`flex items-end space-x-3 max-w-xl ${alignment}`}>
      {!isUser && (
        <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 ${isUser ? 'bg-blue-600' : 'bg-white dark:bg-gray-800'}`}>
          <Icon size={24} className={isError ? 'text-red-500' : iconColor} />
        </div>
      )}
      <div className="flex flex-col">
        <div className={`px-4 py-3 rounded-lg ${bgColor} ${isUser ? 'rounded-br-none' : 'rounded-bl-none'}`}>
          <p className="text-base whitespace-pre-wrap">{content}</p>
        </div>
        {sources && sources.length > 0 && (
          <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 flex flex-wrap gap-2">
            <span className="font-semibold">Sources:</span>
            {sources.map((source, i) => (
              <span key={i} className="flex items-center gap-1 bg-gray-100 dark:bg-gray-600 px-2 py-1 rounded-full">
                <FileText size={12} />
                {source.split('/').pop()}
              </span>
            ))}
          </div>
        )}
      </div>
       {isUser && (
        <div className="w-10 h-10 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
          <Icon size={24} className={iconColor} />
        </div>
      )}
    </div>
  );
};

export default Message;
