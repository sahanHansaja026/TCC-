// Home.js
import React from 'react';
import { getUser } from '../AuthService/authService';

export default function Home() {
    const user = getUser();

    return (
        <div>
            <h2>Welcome, {user?.email}</h2>
            <p>Password: {user?.password}</p>
        </div>
    );
}