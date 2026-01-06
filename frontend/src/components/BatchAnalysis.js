import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, Download, Loader2, AlertCircle, CheckCircle, Zap } from 'lucide-react';
import { batchAnalyze, simpleBatchAnalyze } from '../services/api';
import toast from 'react-hot-toast';

const BatchAnalysis = () => {
  const [file, setFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const uploadedFile = acceptedFiles[0];
      
      if (!uploadedFile.name.endsWith('.csv')) {
        toast.error('Please upload a CSV file');
        return;
      }
      
      if (uploadedFile.size > 10 * 1024 * 1024) { // 10MB limit
        toast.error('File size must be less than 10MB');
        return;
      }
      
      setFile(uploadedFile);
      setDownloadUrl(null);
      toast.success('File uploaded successfully!');
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
    },
    multiple: false,
  });

  const handleProcessFile = async () => {
    if (!file) {
      toast.error('Please upload a file first');
      return;
    }

    setIsProcessing(true);
    try {
      console.log('Processing file:', file.name, 'Size:', file.size);
      
      const blob = await batchAnalyze(file);
      console.log('Received blob:', blob);
      
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);
      toast.success('Batch analysis completed successfully!');
    } catch (error) {
      console.error('Batch analysis error:', error);
      console.error('Error response:', error.response);
      console.error('Error data:', error.response?.data);
      
      const errorMessage = error.response?.data?.error || error.message || 'Failed to process file. Please try again.';
      toast.error(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSimpleProcessFile = async () => {
    if (!file) {
      toast.error('Please upload a file first');
      return;
    }

    setIsProcessing(true);
    try {
      console.log('Simple processing file:', file.name, 'Size:', file.size);
      
      const blob = await simpleBatchAnalyze(file);
      console.log('Received simple blob:', blob);
      
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);
      toast.success('Simple batch analysis completed!');
    } catch (error) {
      console.error('Simple batch analysis error:', error);
      const errorMessage = error.response?.data?.error || error.message || 'Failed to process file.';
      toast.error(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleDownload = () => {
    if (downloadUrl) {
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = 'text_analysis_results.csv';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      toast.success('Download started!');
    }
  };

  const sampleCSVContent = `text
"The acting was amazing but the story was boring"
"Fantastic movie with great direction and music"
"Terrible film, poor acting and confusing plot"
"Beautiful cinematography but weak storyline"`;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Batch Text Analysis
        </h1>
        <p className="text-lg text-gray-600">
          Upload a CSV file with a 'text' column to analyze multiple texts at once
        </p>
      </div>

      {/* File Upload Area */}
      <div className="glass-morphism rounded-2xl p-8">
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200 ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          
          <div className="flex flex-col items-center space-y-4">
            <div className="p-4 bg-primary-100 rounded-full">
              <Upload className="w-8 h-8 text-primary-600" />
            </div>
            
            {isDragActive ? (
              <div>
                <p className="text-lg font-medium text-primary-600">
                  Drop your CSV file here...
                </p>
              </div>
            ) : (
              <div>
                <p className="text-lg font-medium text-gray-900 mb-2">
                  Drag & drop your CSV file here
                </p>
                <p className="text-sm text-gray-600">
                  or click to browse files
                </p>
              </div>
            )}
            
            <div className="text-xs text-gray-500">
              Supported format: CSV (Max 10MB)
            </div>
          </div>
        </div>

        {file && (
          <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-5 h-5 text-green-600" />
                <div>
                  <p className="font-medium text-green-900">{file.name}</p>
                  <p className="text-sm text-green-700">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>
              <button
                onClick={() => {
                  setFile(null);
                  setDownloadUrl(null);
                }}
                className="text-red-600 hover:text-red-800 text-sm font-medium"
              >
                Remove
              </button>
            </div>
          </div>
        )}

        <div className="mt-6 flex justify-center space-x-4">
          <button
            onClick={handleProcessFile}
            disabled={!file || isProcessing}
            className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 text-white font-semibold rounded-xl hover:from-primary-700 hover:to-primary-800 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            {isProcessing ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                <span>Full Analysis</span>
              </>
            )}
          </button>
          
          <button
            onClick={handleSimpleProcessFile}
            disabled={!file || isProcessing}
            className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-green-600 to-green-700 text-white font-semibold rounded-xl hover:from-green-700 hover:to-green-800 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            {isProcessing ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                <span>Quick Analysis</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Download Section */}
      {downloadUrl && (
        <div className="glass-morphism rounded-xl p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Analysis Complete!
              </h3>
              <p className="text-gray-600">
                Your batch analysis is ready. Download the results below.
              </p>
              <p className="text-sm text-green-600 font-medium">
                Ready to download results
              </p>
            </div>
            <button
              onClick={handleDownload}
              className="flex items-center space-x-2 px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all duration-200"
            >
              <Download className="w-5 h-5" />
              <span>Download Results</span>
            </button>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="glass-morphism rounded-xl p-6">
        <div className="flex items-center space-x-2 mb-4">
          <AlertCircle className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-semibold text-gray-900">How to Use</h3>
        </div>
        
        <div className="space-y-4 text-gray-700">
          <div>
            <h4 className="font-medium mb-2">1. Prepare your CSV file:</h4>
            <ul className="list-disc list-inside space-y-1 text-sm ml-4">
              <li>Your CSV must have a column named 'text'</li>
              <li>Each row should contain one text to analyze</li>
              <li>Maximum file size: 10MB</li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium mb-2">2. Sample CSV format:</h4>
            <div className="bg-gray-50 p-3 rounded-lg text-sm font-mono">
              <pre>{sampleCSVContent}</pre>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium mb-2">3. Results include:</h4>
            <ul className="list-disc list-inside space-y-1 text-sm ml-4">
              <li>Sentiment analysis with confidence scores</li>
              <li>Multi-label topic classification</li>
              <li>Aspect-wise sentiment analysis</li>
              <li>Emotion detection</li>
              <li>Text analysis metrics</li>
              <li>Extracted keywords</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BatchAnalysis;
