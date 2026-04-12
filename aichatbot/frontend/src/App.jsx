import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageSquare, X, User, Bot, Loader, FileText, Maximize, Minimize } from 'lucide-react';
import axios from 'axios';

// --- API Logic ---

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const sendMessage = async (message, history) => {
    try {
        const response = await apiClient.post('/chat', {
            message: message,
            history,
        });
        return response.data;
    } catch (error) {
        console.error('Error sending message:', error.response ? error.response.data : error.message);
        throw error;
    }
};

export const sendLead = async (leadData) => {
    try {
        const response = await apiClient.post('/lead', leadData);
        return response.data;
    } catch (error) {
        console.error('Error sending lead:', error.response ? error.response.data : error.message);
        throw error;
    }
};


// --- Child Components ---

const Message = ({ message }) => {
    const isUser = message.role === 'user';
    const isError = message.isError || false;
    const bubbleStyles = isUser ? 'bg-red-600 text-white rounded-br-none' : `bg-gray-200 text-gray-800 rounded-bl-none ${isError ? 'bg-red-100 text-red-700' : ''}`;
    const Avatar = isUser ? User : Bot;
    const avatarStyles = isUser ? 'bg-gray-300 text-gray-700' : 'bg-red-600 text-white';
    
    return (
        <div className={`flex items-start gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
            {!isUser && (
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${avatarStyles}`}>
                    <Avatar size={18} />
                </div>
            )}
            <div className="flex flex-col items-start max-w-xs md:max-w-md">
                <div className={`px-4 py-3 rounded-2xl ${bubbleStyles}`}>
                    <p className="text-sm leading-relaxed">{message.content}</p>
                </div>
                {/* The sources display has been removed from here */}
            </div>
            {isUser && (
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${avatarStyles}`}>
                    <Avatar size={18} />
                </div>
            )}
        </div>
    );
};

const LeadForm = ({ onSubmitSuccess, initialQuery, onClose }) => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitError, setSubmitError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isSubmitting || !name || !email) return;
        setIsSubmitting(true);
        setSubmitError(null);
        try {
            await sendLead({ name, email, query: initialQuery });
            onSubmitSuccess();
        } catch (error) {
            setSubmitError("Failed to submit. Please try again.");
            console.error("Failed to submit lead:", error);
        } finally {
            setIsSubmitting(false);
        }
    };
    
    return (
        <div className="p-4 bg-gray-100 border-t border-gray-200 relative">
            <button onClick={onClose} className="absolute top-2 right-2 text-gray-400 hover:text-gray-600" aria-label="Close form"><X size={18} /></button>
            <p className="text-sm font-semibold text-center text-gray-700 mb-3">Connect with our team</p>
            <form onSubmit={handleSubmit} className="space-y-3">
                <input type="text" placeholder="Your Name" value={name} onChange={(e) => setName(e.target.value)} required className="w-full p-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"/>
                <input type="email" placeholder="Your Email" value={email} onChange={(e) => setEmail(e.target.value)} required className="w-full p-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"/>
                <textarea rows="2" readOnly value={initialQuery} className="w-full p-2 text-sm bg-gray-200 border border-gray-300 rounded-md cursor-not-allowed"/>
                <button type="submit" disabled={isSubmitting} className="w-full bg-red-600 text-white py-2 rounded-md hover:bg-red-700 transition-colors disabled:bg-red-400 disabled:cursor-not-allowed">
                    {isSubmitting ? 'Submitting...' : 'Submit Request'}
                </button>
                {submitError && <p className="text-red-500 text-xs text-center mt-2">{submitError}</p>}
            </form>
        </div>
    );
};


// --- Main App Component ---
function App() {
    const [isOpen, setIsOpen] = useState(false);
    // --- NEW: State for full-screen mode ---
    const [isFullScreen, setIsFullScreen] = useState(false);
    const [messages, setMessages] = useState([
        { role: 'assistant', content: "Hello! I'm the KAITOZ AI assistant. How can I help you today?" }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showLeadForm, setShowLeadForm] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); };
    useEffect(scrollToBottom, [messages, isLoading]);

    const handleSend = async (e) => {
        if (e) e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        const currentInput = input;
        setInput('');
        setIsLoading(true);
        setError(null);
        setShowLeadForm(false);

        try {
            const history = messages.slice(-10).map(({ role, content }) => ({ role, content }));
            const response = await sendMessage(currentInput, history);
            const assistantMessage = { role: 'assistant', content: response.reply, sources: response.sources || [] };
            setMessages(prev => [...prev, assistantMessage]);

            const lowercasedReply = response.reply.toLowerCase();
            const triggerPhrases = ["connect you with our support", "fill out the form", "don't have enough information", "cannot find the answer", "does not contain", "not mention"];
            if (triggerPhrases.some(phrase => lowercasedReply.includes(phrase))) {
                setTimeout(() => setShowLeadForm(true), 500);
            }
        } catch (err) {
            console.error("API Error:", err);
            const errorMessage = { role: 'assistant', content: "Sorry, I'm having trouble connecting to the server. Please check the backend and try again.", isError: true };
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

    // --- NEW: Dynamic classes for the main chat window ---
    const chatWindowClasses = isFullScreen
        ? "fixed inset-0 w-full h-full flex flex-col bg-white z-50"
        : "fixed bottom-6 right-6 w-[calc(100%-48px)] max-w-md h-[70vh] max-h-[600px] flex flex-col bg-white shadow-2xl rounded-xl border border-gray-200 z-50";

    return (
        <div className="font-sans">
             <div className="bg-white min-h-screen p-10">
                <h1 className="text-3xl font-bold text-red-600">KAITOZ Website Content</h1>
                <p className="mt-4 text-gray-700">This is where your main website page content would go.</p>
             </div>
            {!isOpen && (<button onClick={() => setIsOpen(true)} className="fixed bottom-6 right-6 bg-red-600 text-white w-16 h-16 rounded-full flex items-center justify-center shadow-lg hover:scale-110 transition-transform z-50" aria-label="Open chat"><MessageSquare size={30} /></button>)}
            
            {isOpen && (
                <div className={chatWindowClasses}>
                    <div className={`flex justify-between items-center p-4 border-b border-gray-200 bg-gray-50 ${isFullScreen ? '' : 'rounded-t-xl'}`}>
                        <h3 className="text-lg font-bold text-gray-800">KAITOZ AI Assistant</h3>
                        <div className="flex items-center space-x-2">
                            {/* --- NEW: Full-screen toggle button --- */}
                            <button onClick={() => setIsFullScreen(!isFullScreen)} className="text-gray-500 hover:text-gray-800 p-1" aria-label={isFullScreen ? 'Exit full-screen' : 'Enter full-screen'}>
                                {isFullScreen ? <Minimize size={18} /> : <Maximize size={18} />}
                            </button>
                            <button onClick={() => setIsOpen(false)} className="text-gray-500 hover:text-gray-800 p-1" aria-label="Close chat">
                                <X size={20} />
                            </button>
                        </div>
                    </div>
                    <div className="flex-1 p-6 overflow-y-auto">
                        <div className="flex flex-col space-y-4">
                            {messages.map((msg, index) => <Message key={index} message={msg} />)}
                            {isLoading && (<div className="flex items-start gap-3"><div className="w-8 h-8 rounded-full bg-red-600 text-white flex items-center justify-center flex-shrink-0"><Bot size={18} /></div><div className="px-4 py-3 rounded-2xl bg-gray-200 text-gray-800 rounded-bl-none flex items-center"><Loader className="animate-spin text-red-600 mr-2" size={16}/><span className="text-sm">Thinking...</span></div></div>)}
                            <div ref={messagesEndRef} />
                        </div>
                    </div>
                    {showLeadForm && <LeadForm onSubmitSuccess={handleLeadSubmit} initialQuery={messages.slice(-2)[0].content} onClose={() => setShowLeadForm(false)} />}
                    <div className={`p-4 border-t border-gray-200 bg-white ${isFullScreen ? '' : 'rounded-b-xl'}`}>
                        <form onSubmit={handleSend} className="flex items-center space-x-3">
                            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask about our services..." className="flex-1 p-3 bg-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 transition" disabled={isLoading || showLeadForm} />
                            <button type="submit" className="bg-red-600 text-white p-3 rounded-lg hover:bg-red-700 disabled:bg-red-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center" disabled={!input.trim() || isLoading || showLeadForm} aria-label="Send message"><Send size={20} /></button>
                        </form>
                        {error && <p className="text-red-500 text-sm mt-2 text-center">{error}</p>}
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;

