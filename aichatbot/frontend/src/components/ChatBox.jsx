import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader, Server, FileText } from 'lucide-react';
import Message from './Message';
import LeadForm from './LeadForm';
import { sendMessage } from '../api';

const ChatBox = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hello! How can I help you with our IT services today?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showLeadForm, setShowLeadForm] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const history = messages.slice(-10); // Send last 10 messages as history
      const response = await sendMessage(input, history);
      
      const assistantMessage = {
        role: 'assistant',
        content: response.reply,
        sources: response.sources
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Simple logic to trigger lead form
      if (response.reply.toLowerCase().includes("don't have enough information") || response.reply.toLowerCase().includes("contact our support")) {
        setTimeout(() => setShowLeadForm(true), 1000);
      }

    } catch (err) {
      console.error("API Error:", err);
      const errorMessage = { role: 'assistant', content: "Sorry, I'm having trouble connecting to my brain right now. Please try again in a moment.", isError: true };
      setMessages(prev => [...prev, errorMessage]);
      setError('Failed to get a response from the server.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleLeadSubmit = () => {
    setMessages(prev => [...prev, {role: 'assistant', content: "Thanks! A member of our team will reach out to you shortly."}]);
    setShowLeadForm(false);
  };

  return (
    <div className="w-full max-w-3xl h-[70vh] flex flex-col bg-white dark:bg-gray-800 shadow-2xl rounded-lg border border-gray-200 dark:border-gray-700">
      <div className="flex-1 p-6 overflow-y-auto">
        <div className="flex flex-col space-y-4">
          {messages.map((msg, index) => (
            <Message key={index} message={msg} />
          ))}
          {isLoading && (
            <div className="flex items-center space-x-2 self-start">
              <div className="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                 <Loader className="animate-spin text-blue-600" size={20}/>
              </div>
              <div className="px-4 py-2 rounded-lg bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100">
                Thinking...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      {showLeadForm && <LeadForm onSubmitSuccess={handleLeadSubmit} initialQuery={messages.slice(-2)[0].content} />}

      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <form onSubmit={handleSend} className="flex items-center space-x-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about our services..."
            className="flex-1 p-3 bg-gray-100 dark:bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            disabled={isLoading || showLeadForm}
          />
          <button
            type="submit"
            className="bg-blue-600 text-white p-3 rounded-lg hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
            disabled={!input.trim() || isLoading || showLeadForm}
            aria-label="Send message"
          >
            <Send size={20} />
          </button>
        </form>
         {error && <p className="text-red-500 text-sm mt-2 text-center">{error}</p>}
      </div>
    </div>
  );
};

export default ChatBox;
