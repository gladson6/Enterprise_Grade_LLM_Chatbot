import React, { useState } from 'react';
import { sendLead } from '../api';
import { Loader } from 'lucide-react';

const LeadForm = ({ onSubmitSuccess, initialQuery }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [company, setCompany] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      await sendLead({ name, email, company, query: initialQuery });
      onSubmitSuccess();
    } catch (err) {
      setError("Failed to submit form. Please try again.");
      console.error("Lead form error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 bg-gray-100 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-600">
      <h3 className="font-semibold text-center mb-2 text-gray-800 dark:text-gray-200">
        Let's connect you with an expert.
      </h3>
      <p className="text-sm text-center text-gray-600 dark:text-gray-400 mb-4">
        I couldn't find a specific answer. Please provide your details, and a human expert will get back to you.
      </p>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <input
            type="text"
            placeholder="Your Name*"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="w-full p-2 rounded-md bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="email"
            placeholder="Your Email*"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full p-2 rounded-md bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <input
          type="text"
          placeholder="Company Name (Optional)"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
          className="w-full p-2 rounded-md bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-green-600 text-white p-2 rounded-md hover:bg-green-700 disabled:bg-green-400 flex items-center justify-center"
        >
          {isLoading ? <Loader className="animate-spin" /> : 'Submit Request'}
        </button>
        {error && <p className="text-red-500 text-xs text-center">{error}</p>}
      </form>
    </div>
  );
};

export default LeadForm;
