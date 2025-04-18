import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiImage, FiX, FiCheckCircle } from 'react-icons/fi';

const ImageUploader = ({ onImageSelected, onImageRemoved }) => {
  const [preview, setPreview] = useState(null);
  
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      
      // Only accept images
      if (!file.type.startsWith('image/')) {
        alert('Please upload an image file (JPEG, PNG, etc.)');
        return;
      }
      
      // Create a preview URL
      const previewUrl = URL.createObjectURL(file);
      setPreview(previewUrl);
      
      // Pass the file to the parent component
      onImageSelected(file);
    }
  }, [onImageSelected]);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.webp']
    },
    maxFiles: 1,
    maxSize: 5 * 1024 * 1024, // 5MB
  });
  
  const handleRemoveImage = () => {
    // Release the object URL to avoid memory leaks
    if (preview) {
      URL.revokeObjectURL(preview);
    }
    
    // Clear the preview
    setPreview(null);
    
    // Notify the parent component
    onImageRemoved();
  };
  
  return (
    <div className="mt-2">
      {!preview ? (
        <div 
          {...getRootProps()} 
          className={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-colors
            ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-blue-400'}`}
        >
          <input {...getInputProps()} />
          <FiImage className="mx-auto h-8 w-8 text-gray-400" />
          <p className="mt-1 text-sm text-gray-500">
            {isDragActive 
              ? 'Drop the image here...' 
              : 'Drag & drop an image, or click to select one'}
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Supports JPEG, PNG, GIF (max 5MB)
          </p>
        </div>
      ) : (
        <div className="relative rounded-lg overflow-hidden border border-gray-200">
          <img 
            src={preview} 
            alt="Property issue preview" 
            className="w-full object-contain max-h-64"
          />
          <div className="absolute inset-0 bg-black bg-opacity-50 opacity-0 hover:opacity-100 transition-opacity flex items-center justify-center">
            <button
              onClick={handleRemoveImage}
              className="bg-red-500 text-white p-2 rounded-full hover:bg-red-600"
              title="Remove image"
            >
              <FiX />
            </button>
          </div>
          <div className="absolute bottom-0 right-0 p-2 bg-green-500 text-white rounded-tl-lg flex items-center">
            <FiCheckCircle className="mr-1" />
            <span className="text-sm">Image ready</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploader; 