import React, { useState, useEffect, useCallback } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './Cgpa.css';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function Cgpa() {
    const [cgpaData, setCgpaData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    const fetchCgpa = useCallback(async () => {
        setIsLoading(true);
        const authToken = localStorage.getItem('auth_token');
        const apiUrl = import.meta.env.VITE_API_BASE_URL;
        setError('');
        try {
            const response = await fetch(`${apiUrl}/api/cgpa`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ auth_token: authToken })
            });
            const data = await response.json();
            if (response.ok) {
                setCgpaData(data);
            } else {
                setError(data.error || 'Failed to fetch CGPA data.');
            }
        } catch (err) {
            console.error("CGPA API call failed:", err);
            setError('An error occurred while fetching CGPA data.');
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchCgpa();
    }, [fetchCgpa]);

    if (isLoading) return (
        <div className="loading-overlay">
            <div className="loader"></div>
        </div>
    );
    if (error) return <div className="error-message">{error}</div>;
    if (!cgpaData || !cgpaData.semwise_data || cgpaData.semwise_data.length === 0) {
        return <p>No CGPA data available to display.</p>;
    }

    // Performance colors from image
    const pink = '#FF5CBE';
    const cyan = '#4DD0E1';

    const chartData = {
        labels: cgpaData.semwise_data.map(d => `${d.sem}`),
        datasets: [
            {
                label: 'SGPA',
                data: cgpaData.semwise_data.map(d => d.sgpa),
                borderColor: pink,
                backgroundColor: pink,
                fill: false,
                tension: 0.4,
                pointRadius: 6,
                pointHoverRadius: 8,
                borderWidth: 3,
                pointBackgroundColor: '#fff',
                pointBorderColor: pink,
                pointBorderWidth: 2,
            },
            {
                label: 'CGPA',
                data: cgpaData.semwise_data.map(d => d.cgpa),
                borderColor: cyan,
                backgroundColor: cyan,
                fill: false,
                tension: 0.4,
                pointRadius: 6,
                pointHoverRadius: 8,
                borderWidth: 3,
                pointBackgroundColor: '#fff',
                pointBorderColor: cyan,
                pointBorderWidth: 2,
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                align: 'center',
                labels: {
                    color: 'white',
                    font: { size: 14, family: 'Outfit', weight: '500' },
                    usePointStyle: true,
                    pointStyle: 'circle',
                    padding: 25,
                }
            },
            tooltip: {
                backgroundColor: 'rgba(30, 30, 30, 0.9)',
                titleFont: { size: 14, family: 'Outfit' },
                bodyFont: { size: 13, family: 'Outfit' },
                padding: 12,
                cornerRadius: 8,
                displayColors: true,
            }
        },
        scales: {
            x: {
                ticks: { color: '#94a3b8', font: { size: 12, family: 'Outfit' } },
                grid: { color: 'rgba(255,255,255,0.05)', drawBorder: false },
                title: {
                    display: false
                }
            },
            y: {
                ticks: {
                    color: '#94a3b8',
                    font: { size: 12, family: 'Outfit' },
                    padding: 10,
                },
                grid: { color: 'rgba(255,255,255,0.1)', drawBorder: false },
                beginAtZero: false,
                title: {
                    display: true,
                    text: 'Grade Points',
                    color: '#fff',
                    font: { size: 14, family: 'Outfit', weight: '600' }
                }
            }
        },
    };

    return (
        <div className="cgpa-page-wrapper">
            <div className="cgpa-card">
                {/* Summary Section */}
                <div className="cgpa-summary" style={{ position: 'relative' }}>
                    <h2>Total Credits: {cgpaData.total_credits}</h2>
                    <h2>Total Credit Points: {cgpaData.credit_points_total}</h2>
                    <h2>Overall CGPA: {cgpaData.cgpa}</h2>
                </div>

                {/* Table Section */}
                <div className="table-section">
                    <table className="cgpa-table">
                        <thead>
                            <tr>
                                <th>SEMESTER</th>
                                <th>SGPA</th>
                                <th>CGPA (UP TO THIS SEM)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {cgpaData.semwise_data.map((sem, index) => (
                                <tr key={index}>
                                    <td>{sem.sem}</td>
                                    <td>{sem.sgpa}</td>
                                    <td>{sem.cgpa}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* Chart Section */}
                <div className="chart-section">
                    <h2 className="chart-title">Academic Performance Trends</h2>
                    <div className="chart-container">
                        <Line data={chartData} options={chartOptions} />
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Cgpa;