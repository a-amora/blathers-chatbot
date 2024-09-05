import React, { useState } from 'react';
import { upload, ask } from './utils/utils';
import './App.css';

const App = () => {
  const [answer, setAnswer] = useState('');
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null); // State to track selected item

  const uploadDoc = async (file) => {
    try {
      const response = await upload(file);
      console.log('Upload response:', response);
    } catch (error) {
      console.error('Error uploading document:', error);
    }
  };

  const askBlathers = async () => {
    if (!question.trim()) {
      console.error('Question is empty');
      return;
    }

    setIsLoading(true);
    try {
      setAnswer('');
      const response = await ask(question);
      setAnswer(response);
    } catch (error) {
      console.error('Error asking question:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      uploadDoc(file);
    }
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
    // To do
  };

  return (
    <div className="app-container">
      <div className="sidebar">
        <p><b>Say Hello to Blathers!</b></p>
        <p>Blathers is an AI assistant here to serve your project needs.  Blathers can answer questions about complex documents you've shared.   Each time you upload a document to Blathers, it is saved to your personal repository, making it easy for you to choose which document she is assisting you with.</p>
        <p>Try uploading a document below to get started!</p>

        <div className="context-list">
          <label><b>Blathers Documents</b></label>
          <ul>
            <li>Example 1</li>
            <li>Example 2</li>
          </ul>
        </div>

        <label htmlFor="file_input"><b>Upload a Document</b></label>
        <input type="file" id="file_input" onChange={handleFileChange} />

        <div className="version"><b>v0.01</b></div> 
      </div>

      <div className="main-content">
        <div className="answer-container">
          <textarea
            id="answer"
            value={answer}
            readOnly
            rows="4"
            cols="50"
          />
          {isLoading && <div className="loading">Loading...</div>}
        </div>

        <textarea
          id="question"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          rows="2"
          cols="50"
        />

        <button onClick={askBlathers} disabled={isLoading}>Ask Blathers</button>
      </div>
    </div>
  );
};

export default App;
