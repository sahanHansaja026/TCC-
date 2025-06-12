// Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { setUser } from '../AuthService/authService';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();

        // Simulate login
        const user = { email, password };
        setUser(user);

        navigate('/home');
    };

    return (
        <form onSubmit={handleLogin}>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            /><br />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            /><br />
            <button type="submit">Login</button>
        </form>
    );
}