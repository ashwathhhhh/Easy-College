import React from 'react';
import { Link } from 'react-router-dom';
import { BarChart3, Calculator, MessageSquare, GraduationCap, BookOpen } from 'lucide-react';
import { motion } from 'framer-motion';

function Dashboard() {
    const user = JSON.parse(localStorage.getItem('user'));

    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const item = {
        hidden: { y: 20, opacity: 0 },
        show: { y: 0, opacity: 1 }
    };

    const MotionLink = motion(Link);

    return (
        <div className="dashboard-container">
            <motion.div
                className="dashboard-options"
                variants={container}
                initial="hidden"
                animate="show"
            >
                <MotionLink to="/attendance" className="dashboard-card" variants={item}>
                    <div className="dashboard-icon-wrapper">
                        <BarChart3 size={32} strokeWidth={1.5} />
                    </div>
                    <div className="dashboard-title">Attendance</div>
                    <div className="dashboard-description">Track your class attendance and stay on top of daily requirements.</div>
                </MotionLink>

                <MotionLink to="/gpa" className="dashboard-card" variants={item}>
                    <div className="dashboard-icon-wrapper">
                        <Calculator size={32} strokeWidth={1.5} />
                    </div>
                    <div className="dashboard-title">GPA Calculator</div>
                    <div className="dashboard-description">Calculate your semester GPA with ease and precision.</div>
                </MotionLink>

                <MotionLink to="/cgpa" className="dashboard-card" variants={item}>
                    <div className="dashboard-icon-wrapper">
                        <GraduationCap size={32} strokeWidth={1.5} />
                    </div>
                    <div className="dashboard-title">CGPA Calculator</div>
                    <div className="dashboard-description">Monitor your cumulative grade point average across all semesters.</div>
                </MotionLink>

                <MotionLink to="/internals" className="dashboard-card" variants={item}>
                    <div className="dashboard-icon-wrapper">
                        <BookOpen size={32} strokeWidth={1.5} />
                    </div>
                    <div className="dashboard-title">Internal Marks</div>
                    <div className="dashboard-description">View your CA marks and track your internal assessment performance.</div>
                </MotionLink>

                <MotionLink to="/feedback" className="dashboard-card" variants={item}>
                    <div className="dashboard-icon-wrapper">
                        <MessageSquare size={32} strokeWidth={1.5} />
                    </div>
                    <div className="dashboard-title">Feedback</div>
                    <div className="dashboard-description">Automate the feedback form process done in our college.</div>
                </MotionLink>
            </motion.div>
        </div>
    );
}

export default Dashboard;