import React, { useState } from 'react';
import UploadButton from './components/UploadButton';
import DocumentViewer from './components/DocumentViewer';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
    const [documentText, setDocumentText] = useState("");
    const [documentId, setDocumentId] = useState("");

    const handleUploadSuccess = (data) => {
        setDocumentText(data.text);
        setDocumentId(data.filename);
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>AI Planet PDF Upload</h1>
            </header>
            <main>
                <DocumentViewer text={documentText} />
                <ChatInterface documentId={documentId} />
            </main>
            <UploadButton onSuccess={handleUploadSuccess} />
        </div>
    );
}

export default App;


