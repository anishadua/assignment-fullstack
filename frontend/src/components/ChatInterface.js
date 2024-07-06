import React, { useState } from 'react';
import axios from 'axios';

const ChatInterface = ({ documentId }) => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const handleAskQuestion = async () => {
        try {
            const response = await axios.post('http://localhost:8000/question/', {
                document_id: documentId,
                question: question,
            });
            setAnswer(response.data.answer);
        } catch (error) {
            console.error('Error asking question:', error);
            alert('Error asking question: ' + error.response.data.detail);
        }
    };

    return (
        <div>
            <div>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask a question..."
                />
                <button onClick={handleAskQuestion}>Send</button>
            </div>
            <div>
                <p>{answer}</p>
            </div>
        </div>
    );
};

export default ChatInterface;
