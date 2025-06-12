import { useState } from 'react';
import api from '../api';

function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/register/', { username, password, email });
            alert(response.data.message);
        } catch (error) {
            alert(error.response.data.detail);
        }
    };

    return (
        <form onSubmit={handleRegister}>
            <h2>Register</h2>
            <input placeholder="Username" onChange={e => setUsername(e.target.value)} />
            <input type='email' placeholder='email' onChange={e => setEmail(e.target.value)} />
            <input placeholder="Password" type="password" onChange={e => setPassword(e.target.value)} />
            <button type="submit">Register</button>
        </form>
    );
}

export default Register;