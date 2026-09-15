import React from 'react';
import { Navigate } from 'react-router-dom';

const BLOCKED_ROLL_NUMBERS = ['23N244'];

export const isUserBlocked = (userStr, rollStr) => {
    if (rollStr && BLOCKED_ROLL_NUMBERS.includes(rollStr.toUpperCase().trim())) {
        return true;
    }
    if (userStr) {
        const upper = String(userStr).toUpperCase();
        if (BLOCKED_ROLL_NUMBERS.some(blocked => upper.includes(blocked))) {
            return true;
        }
    }
    return false;
};

const PrivateRoute = ({ children }) => {
    const user = localStorage.getItem('user');
    const rollNumber = localStorage.getItem('roll_number');

    if (isUserBlocked(user, rollNumber)) {
        localStorage.removeItem('user');
        localStorage.removeItem('auth_token');
        localStorage.removeItem('roll_number');
        localStorage.removeItem('credentials');
        return <Navigate to="/" replace state={{ error: 'This service is not enabled for you' }} />;
    }

    const isLoggedIn = !!user;
    return isLoggedIn ? children : <Navigate to="/" replace />;
};

export default PrivateRoute;