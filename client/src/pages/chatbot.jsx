import { useState } from 'react';
import axios from 'axios';

const ChatBox = () => {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChat = async () => {
        if (!prompt.trim()) return;

        setLoading(true);
        setResponse('');
        setError('');

        try {
            const res = await axios.post('http://localhost:8000/chat', {
                prompt,
            });

            setResponse(res.data.text);
        } catch (err) {
            setError('Something went wrong. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Chat with AI</h2>
            <textarea
                rows={4}
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Ask something..."
            />
            <br />
            <button onClick={handleChat} disabled={loading}>
                {loading ? 'Thinking...' : 'Send'}
            </button>

            {response && (
                <div className="response">
                    <h4>Response:</h4>
                    <p>{response}</p>
                </div>
            )}

            {error && <p className="error">{error}</p>}
        </div>
    );
};

export default ChatBox;
