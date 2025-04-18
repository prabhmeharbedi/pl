import React, { useState } from 'react';
import { FiSend, FiMapPin, FiImage } from 'react-icons/fi';
import ImageUploader from './ImageUploader';

const ChatInput = ({ onSendMessage, onSendMessageWithImage, isLoading }) => {
  const [message, setMessage] = useState('');
  const [location, setLocation] = useState('');
  const [showLocationInput, setShowLocationInput] = useState(false);
  const [showImageUploader, setShowImageUploader] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (message.trim() && !isLoading) {
      if (selectedImage) {
        // Send message with image
        onSendMessageWithImage(message, selectedImage, location);
        
        // Reset the image after sending
        setSelectedImage(null);
        setShowImageUploader(false);
      } else {
        // Send text-only message
        onSendMessage(message, location);
      }
      
      // Reset the message
      setMessage('');
    }
  };

  const handleImageSelected = (file) => {
    setSelectedImage(file);
  };

  const handleImageRemoved = () => {
    setSelectedImage(null);
  };

  const toggleLocationInput = () => {
    setShowLocationInput(!showLocationInput);
  };

  const toggleImageUploader = () => {
    setShowImageUploader(!showImageUploader);
  };

  return (
    <div className="mt-4">
      {showLocationInput && (
        <div className="mb-2">
          <div className="flex items-center">
            <FiMapPin className="text-gray-400 mr-2" />
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Enter your location (city, state, country)"
              className="flex-1 p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
            />
          </div>
          <p className="text-xs text-gray-500 mt-1">
            Location helps provide more accurate information for tenancy questions.
          </p>
        </div>
      )}
      
      {showImageUploader && (
        <ImageUploader 
          onImageSelected={handleImageSelected} 
          onImageRemoved={handleImageRemoved} 
        />
      )}
      
      <form onSubmit={handleSubmit} className="mt-2">
        <div className="flex">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message here..."
            className="flex-1 p-3 border border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          
          <div className="flex border-t border-b border-gray-300">
            <button
              type="button"
              onClick={toggleLocationInput}
              className={`p-3 hover:bg-gray-100 ${showLocationInput ? 'bg-blue-50 text-blue-500' : 'text-gray-500'}`}
              disabled={isLoading}
              title="Add location"
            >
              <FiMapPin />
            </button>
            
            <button
              type="button"
              onClick={toggleImageUploader}
              className={`p-3 hover:bg-gray-100 ${showImageUploader || selectedImage ? 'bg-blue-50 text-blue-500' : 'text-gray-500'}`}
              disabled={isLoading}
              title="Add image"
            >
              <FiImage />
            </button>
          </div>
          
          <button
            type="submit"
            className={`bg-blue-500 text-white p-3 rounded-r-lg ${
              isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'
            }`}
            disabled={isLoading || (!message.trim())}
          >
            {isLoading ? (
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              <FiSend />
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInput; 