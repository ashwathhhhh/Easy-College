import React from 'react';
import { NavLink, Link, useNavigate } from 'react-router-dom';
import { LogOut, Info, Phone, LayoutDashboard, User } from 'lucide-react';
import { motion } from 'framer-motion';

function Navbar() {
    const navigate = useNavigate();
    const storedUser = localStorage.getItem('user');
    const isLoggedIn = !!storedUser;

    let userName = '';
    if (isLoggedIn) {
        try {
            userName = JSON.parse(storedUser);
        } catch (e) {
            userName = storedUser;
        }
    }

    const handleLogout = () => {
        localStorage.removeItem('user');
        localStorage.removeItem('credentials'); // Keep for backward compatibility cleanup
        localStorage.removeItem('auth_token');
        localStorage.removeItem('login_type');
        navigate('/');
    };

    const contactUrl = "https://mail.google.com/mail/u/0/?view=cm&to=campuslyapi@gmail.com&su=Contact%20from%20Easy%20College&body=Hello,%0D%0A%0D%0AI'm%20contacting%20you%20regarding%20Easy%20College.%0D%0A%0D%0ARegards,%0D%0A[Your%20Name]";

    return (
        <motion.nav
            className="navbar"
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="title-container">
                <Link to={isLoggedIn ? "/dashboard" : "/"} className="logo">
                    Easy College
                </Link>
            </div>

            <div className="navbar-links">
                {isLoggedIn && (
                    <div className="user-greeting" title={userName}>
                        <User size={16} />
                        <span>{userName}</span>
                    </div>
                )}

                {isLoggedIn && (
                    <NavLink to="/dashboard" className={({ isActive }) => isActive ? "active" : ""}>
                        <LayoutDashboard size={18} />
                        <span className="hide-mobile">Dashboard</span>
                    </NavLink>
                )}

                <a href={contactUrl} target="_blank" rel="noopener noreferrer">
                    <Phone size={18} />
                    <span className="hide-mobile">Contact</span>
                </a>

                {isLoggedIn && (
                    <>
                        <NavLink to="/about" className={({ isActive }) => isActive ? "active" : ""}>
                            <Info size={18} />
                            <span className="hide-mobile">About</span>
                        </NavLink>
                        <button onClick={handleLogout}>
                            <LogOut size={18} />
                            <span className="hide-mobile">Logout</span>
                        </button>
                    </>
                )}
            </div>
        </motion.nav>
    );
}

export default Navbar;