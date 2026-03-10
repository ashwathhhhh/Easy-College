import React, { useState, useEffect, useCallback } from 'react';

import './Gpa.css';

function Gpa() {
    const [gpaData, setGpaData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchGpa = useCallback(async () => {
        setIsLoading(true);
        const authToken = localStorage.getItem('auth_token');
        const apiUrl = import.meta.env.VITE_API_BASE_URL;
        setError('');
        try {
            const response = await fetch(`${apiUrl}/api/gpa`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ auth_token: authToken })
            });
            const data = await response.json();
            if (response.ok) {
                setGpaData(data);
            } else {
                setError(data.error || 'Failed to fetch GPA data.');
            }
        } catch (err) {
            console.error("GPA API call failed:", err);
            setError('An error occurred while fetching GPA data.');
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchGpa();
    }, [fetchGpa]);

    if (isLoading) return (
        <div className="loading-overlay">
            <div className="loader"></div>
        </div>
    );
    if (error) return <div className="error-message">{error}</div>;
    if (!gpaData) return <p>No GPA data found.</p>;

    return (
        <div className="gpa-page-wrapper">
            <div className="gpa-card">
                {/* Header matching image */}
                <div className="gpa-header-section">
                    <h1>GPA Calculator</h1>
                    <p>Track your academic performance across all courses</p>
                </div>

                {/* Summary Cards Row */}
                <div className="summary-cards-row">
                    <div className="gpa-summary-card">
                        <div className="summary-label">Total Credits</div>
                        <div className="summary-value">{gpaData.total_credits}</div>
                    </div>
                    <div className="gpa-summary-card">
                        <div className="summary-label">Current GPA</div>
                        <div className="summary-value gpa-accent">{gpaData.gpa}</div>
                    </div>
                    <div className="gpa-summary-card">
                        <div className="summary-label">Total Courses</div>
                        <div className="summary-value courses-accent">{gpaData.table ? gpaData.table.length : 0}</div>
                    </div>
                </div>

                {/* Modernized Table */}
                <div className="table-section-glass">
                    <table className="gpa-modern-table">
                        <thead>
                            <tr>
                                <th>SEMESTER</th>
                                <th>COURSE CODE</th>
                                <th>COURSE NAME</th>
                                <th>CREDITS</th>
                                <th>GRADE</th>
                            </tr>
                        </thead>
                        <tbody>
                            {gpaData.table && gpaData.table.map((course, index) => (
                                <tr key={index}>
                                    <td>
                                        <span className="sem-badge">5</span> {/* Hardcoded since not in API response in snippet */}
                                    </td>
                                    <td className="course-code-cell">{course.course || '-'}</td>
                                    <td className="course-name-cell">{course.title}</td>
                                    <td>
                                        <span className="credits-badge-modern">{course.credits}</span>
                                    </td>
                                    <td className="grade-cell">
                                        {course.grade === 'Completed' ? (
                                            <span className="completed-badge">Completed</span>
                                        ) : (
                                            course.grade
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default Gpa;