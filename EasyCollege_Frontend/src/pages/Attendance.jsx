import React, { useState, useEffect, useCallback } from 'react';
import { Info, Plus, Minus, Wand2, Save, CloudOff, RefreshCw } from 'lucide-react';
import { motion } from 'framer-motion';
import './Attendance.css';

function Attendance() {
    const [attendanceData, setAttendanceData] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [showPopup, setShowPopup] = useState(true);
    const [viewMode, setViewMode] = useState('table'); // 'cards' or 'table'
    const [simulation, setSimulation] = useState({});
    const [isOfflineView, setIsOfflineView] = useState(false);
    const [lastSaved, setLastSaved] = useState(null);
    const [showSavePrompt, setShowSavePrompt] = useState(false);

    const fetchAttendance = useCallback(async () => {
        setIsLoading(true);
        setIsOfflineView(false);
        const authToken = localStorage.getItem('auth_token');
        const apiUrl = import.meta.env.VITE_API_BASE_URL || '';
        setError('');
        try {
            const response = await fetch(`${apiUrl}/api/attendance`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ auth_token: authToken })
            });
            const data = await response.json();
            if (response.ok) {
                setAttendanceData(data);

                // Check if we should prompt to save
                const saved = localStorage.getItem('saved_attendance_data');
                if (!saved || JSON.stringify(JSON.parse(saved).data) !== JSON.stringify(data)) {
                    setShowSavePrompt(true);
                }
            } else {
                setError(data.error || 'Failed to fetch data.');
            }
        } catch (err) {
            console.error("Attendance API call failed:", err);
            setError('An error occurred. Please try again.');
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        const saved = localStorage.getItem('saved_attendance_data');
        if (saved) {
            const parsed = JSON.parse(saved);
            setLastSaved(parsed.timestamp);
        }
        fetchAttendance();
    }, [fetchAttendance]);

    const saveAttendanceLocally = () => {
        const dataToSave = {
            data: attendanceData,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem('saved_attendance_data', JSON.stringify(dataToSave));
        setLastSaved(dataToSave.timestamp);
        setShowSavePrompt(false);
    };

    const loadSavedAttendance = () => {
        const saved = localStorage.getItem('saved_attendance_data');
        if (saved) {
            const parsed = JSON.parse(saved);
            setAttendanceData(parsed.data);
            setLastSaved(parsed.timestamp);
            setIsOfflineView(true);
            setError('');
        }
    };

    const togglePopup = () => setShowPopup(!showPopup);

    const getAttendanceClass = (percentageStr) => {
        const value = parseInt(percentageStr);
        if (value >= 75) return 'attendance-good';
        if (value >= 65) return 'attendance-medium';
        return 'attendance-low';
    };

    const handleSimulate = (courseCode, type, value) => {
        setSimulation(prev => {
            const currentObj = prev[courseCode] || { bunk: 0, attend: 0 };
            return {
                ...prev,
                [courseCode]: {
                    ...currentObj,
                    [type]: Math.max(0, currentObj[type] + value)
                }
            };
        });
    };

    const getSimulatedCourse = (course) => {
        const sim = simulation[course.course_code] || { bunk: 0, attend: 0 };
        if (sim.bunk === 0 && sim.attend === 0) {
            return { ...course, isSimulated: false, simBunk: 0, simAttend: 0 };
        }

        const simulatedTotal = parseInt(course.total_hours) + sim.bunk + sim.attend;
        const simulatedPresent = parseInt(course.present_hours) + sim.attend;
        const simulatedAbsent = parseInt(course.absent_hours) + sim.bunk;
        const newPercentage = simulatedTotal > 0 ? Math.round((simulatedPresent / simulatedTotal) * 100) : parseInt(course.physical_attendance);

        const originalPhys = parseInt(course.physical_attendance);
        const originalMed = parseInt(course.with_exemption);
        const exemptionDiff = originalMed - originalPhys;
        const newMedPercentage = newPercentage + exemptionDiff;

        // Recalculate status simply based on new percentage (approximation for UI)
        let newStatus = course.status;
        let newCount = course.count;
        if (newPercentage >= 75) {
            newStatus = "Remaining bunks";
            newCount = Math.floor((simulatedPresent - (0.75 * simulatedTotal)) / 0.75);
            if (newCount < 0) newCount = 0;
        } else {
            newStatus = "Classes to attend";
            newCount = Math.ceil(((0.75 * simulatedTotal) - simulatedPresent) / 0.25);
        }

        let newExemptionBunks = course.exemption_bunks;
        if (course.exemption_bunks !== undefined) {
            newExemptionBunks = 0;
            if (newMedPercentage >= 75 && newPercentage >= 65) {
                let p1 = newPercentage;
                let p2 = newMedPercentage;
                let dEx = 0;
                const assumedExemptionHours = Math.max(0, Math.floor(((originalMed / 100) * parseInt(course.total_hours))) - Math.floor(((originalPhys / 100) * parseInt(course.total_hours))));

                while (p1 > 65 && p2 > 75 && dEx < 50) {
                    dEx += 1;
                    p1 = Math.ceil((simulatedPresent / (simulatedTotal + dEx)) * 100);
                    p2 = Math.ceil(((simulatedPresent + assumedExemptionHours) / (simulatedTotal + dEx)) * 100);
                    if (p1 > 65 && p2 > 75) {
                        newExemptionBunks += 1;
                    }
                }
            }
        }

        return {
            ...course,
            total_hours: simulatedTotal,
            present_hours: simulatedPresent,
            absent_hours: simulatedAbsent,
            physical_attendance: `${newPercentage}`,
            with_exemption: `${newMedPercentage}`,
            status: newStatus,
            count: newCount,
            exemption_bunks: newExemptionBunks,
            isSimulated: true,
            simBunk: sim.bunk,
            simAttend: sim.attend
        };
    };

    const simulatedData = attendanceData.map(getSimulatedCourse);

    const renderSimulateControls = (course) => (
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px' }}>
                <span style={{ fontSize: '10px', color: '#888' }}>Attend</span>
                <div style={{ display: 'flex', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                    <button
                        onClick={() => handleSimulate(course.course_code, 'attend', -1)}
                        style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', padding: '2px 4px' }}
                    ><Minus size={12} /></button>
                    <span style={{ fontSize: '12px', padding: '0 4px', lineHeight: '18px' }}>{course.simAttend}</span>
                    <button
                        onClick={() => handleSimulate(course.course_code, 'attend', 1)}
                        style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', padding: '2px 4px' }}
                    ><Plus size={12} /></button>
                </div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2px' }}>
                <span style={{ fontSize: '10px', color: '#888' }}>Bunk</span>
                <div style={{ display: 'flex', background: 'rgba(255,255,255,0.1)', borderRadius: '4px', overflow: 'hidden' }}>
                    <button
                        onClick={() => handleSimulate(course.course_code, 'bunk', -1)}
                        style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', padding: '2px 4px' }}
                    ><Minus size={12} /></button>
                    <span style={{ fontSize: '12px', padding: '0 4px', lineHeight: '18px' }}>{course.simBunk}</span>
                    <button
                        onClick={() => handleSimulate(course.course_code, 'bunk', 1)}
                        style={{ background: 'transparent', border: 'none', color: '#fff', cursor: 'pointer', padding: '2px 4px' }}
                    ><Plus size={12} /></button>
                </div>
            </div>
        </div>
    );

    if (isLoading) return (
        <div className="loading-overlay">
            <div className="loader"></div>
        </div>
    );

    if (error === 'Attendance data is currently unavailable.') {
        return (
            <div className="attendance-sync-wrapper">
                <motion.div
                    className="attendance-sync-card"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                >


                    <h2 className="sync-title">Attendance is being updated</h2>
                    <p className="sync-description">
                        Check back later once it is updated
                    </p>

                    <button className="sync-retry-btn" onClick={fetchAttendance}>
                        Refresh Status
                    </button>

                    {lastSaved && (
                        <button
                            className="sync-offline-btn"
                            onClick={loadSavedAttendance}
                            style={{ 
                                marginTop: '12px', 
                                background: 'rgba(255,255,255,0.05)', 
                                border: '1px solid rgba(255,255,255,0.1)',
                                color: '#94a3b8',
                                padding: '14px',
                                borderRadius: '14px',
                                width: '100%',
                                cursor: 'pointer',
                                fontWeight: 600
                            }}
                        >
                            View Last Saved ({new Date(lastSaved).toLocaleDateString()})
                        </button>
                    )}
                </motion.div>
            </div>
        );
    }

    if (error) return <div className="error-message">{error}</div>;

    return (
        <div className="attendance-page-wrapper">
            <div className="attendance-main-card">
                {isOfflineView && (
                    <div className="offline-banner">
                        <CloudOff size={16} />
                        <span>Viewing saved attendance from {new Date(lastSaved).toLocaleString()}</span>
                        <button onClick={fetchAttendance} className="try-live-btn">Try Live Data</button>
                    </div>
                )}

                {showSavePrompt && (
                    <div className="save-prompt-banner">
                        <Save size={16} />
                        <span>Wanna save this attendance to view when ecampus is down?</span>
                        <div className="save-prompt-actions">
                            <button onClick={saveAttendanceLocally} className="save-confirm-btn">Save</button>
                            <button onClick={() => setShowSavePrompt(false)} className="save-cancel-btn">Maybe later</button>
                        </div>
                    </div>
                )}
                <div className="attendance-header-section">
                    <h1>
                        Attendance Tracker
                        <div className="header-actions">
                            <button onClick={() => setShowSavePrompt(true)} className="action-icon-btn" title="Save for offline">
                                <Save size={24} />
                            </button>
                            <button onClick={togglePopup} className="info-icon-btn" title="How is this calculated?">
                                <Info size={24} />
                            </button>
                        </div>
                    </h1>
                    <p>Monitor your class attendance and simulate predicting future percentage changes</p>
                </div>

                <div className="attendance-view-toggle">
                    <div className="attendance-toggle-wrapper">
                        <span className={`attendance-toggle-label ${viewMode === 'cards' ? 'active' : ''}`}>Card View</span>
                        <label className="switch">
                            <input
                                type="checkbox"
                                checked={viewMode === 'table'}
                                onChange={() => setViewMode(viewMode === 'cards' ? 'table' : 'cards')}
                            />
                            <span className="slider"></span>
                        </label>
                        <span className={`attendance-toggle-label ${viewMode === 'table' ? 'active' : ''}`}>Table View</span>
                    </div>
                </div>

                {viewMode === 'table' && (
                    <div className="attendance-table-container">
                        <table className="attendance-modern-table">
                            <thead>
                                <tr>
                                    <th>Code</th>
                                    <th>Course</th>
                                    <th><span className="full-text">Total</span><span className="short-text">TOT</span></th>
                                    <th><span className="full-text">Present</span><span className="short-text">PRESE</span></th>
                                    <th><span className="full-text">Absent</span><span className="short-text">ABSEN</span></th>
                                    <th>%</th>
                                    <th><span className="full-text">% (Med)</span><span className="short-text">% (ME</span></th>
                                    <th><span className="full-text">Bunks</span><span className="short-text">BUNKS</span></th>
                                    <th><span className="full-text">Med Bunks</span><span className="short-text">MED BU</span></th>
                                    <th>Updated</th>
                                    <th>Predictor <Wand2 size={12} style={{ marginLeft: '4px' }} /></th>
                                </tr>
                            </thead>
                            <tbody>
                                {simulatedData.map((course, index) => (
                                    <tr key={index} style={course.isSimulated ? { background: 'rgba(99, 102, 241, 0.1)' } : {}}>
                                        <td className="course-code-cell">{course.course_code}</td>
                                        <td className="course-name-cell">{course.course_name}</td>
                                        <td style={{ fontWeight: 600 }}>{course.total_hours}</td>
                                        <td style={{ fontWeight: 600 }}>{course.present_hours}</td>
                                        <td style={{ fontWeight: 600 }}>{course.absent_hours}</td>
                                        <td className={`percentage-cell ${getAttendanceClass(course.physical_attendance)}`}>
                                            {course.physical_attendance}
                                            {course.isSimulated && <span style={{ fontSize: '10px', display: 'block' }}>Simulated</span>}
                                        </td>
                                        <td className={`percentage-cell ${getAttendanceClass(course.with_exemption)}`}>
                                            {course.with_exemption}
                                        </td>
                                        <td style={{ fontWeight: 700, color: course.status !== "Remaining bunks" ? '#f87171' : '#ccc' }}>
                                            {course.status !== "Remaining bunks" ? `-${course.count}` : course.count}
                                        </td>
                                        <td style={{ fontWeight: 700, color: course.exemption_bunks < 0 ? '#f87171' : '#ccc' }}>
                                            {course.exemption_bunks !== undefined ? course.exemption_bunks : '-'}
                                        </td>
                                        <td style={{ fontSize: '0.9em', color: '#888' }}>
                                            {course.updated_till || '-'}
                                        </td>
                                        <td>
                                            {renderSimulateControls(course)}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {viewMode === 'cards' && (
                    <>
                        <h2 className="detailed-view-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                            Detailed View <Wand2 size={18} color="var(--primary)" />
                        </h2>
                        <div className="cards-container">
                            {simulatedData.map((course, index) => (
                                <div className={`attendance-card ${course.isSimulated ? 'simulated-card' : ''}`} key={index} style={course.isSimulated ? { borderColor: 'var(--primary)', boxShadow: '0 0 15px rgba(99, 102, 241, 0.2)' } : {}}>
                                    <div className="course-header">
                                        <div className="course-name">{course.course_name}</div>
                                        <div className="course-code">{course.course_code}</div>
                                    </div>

                                    <div className="attendance-stats">
                                        <div className="stat-item">
                                            <div className="stat-label">Physical Attendance</div>
                                            <div className={`stat-value ${getAttendanceClass(course.physical_attendance)}`}>
                                                {course.physical_attendance}%
                                            </div>
                                        </div>
                                        <div className="stat-item">
                                            <div className="stat-label">With Exemption</div>
                                            <div className="stat-value">{course.with_exemption}%</div>
                                        </div>
                                    </div>

                                    <div className="attendance-stats">
                                        <div className="stat-item">
                                            <div className="stat-label">Present / Total</div>
                                            <div className="stat-value">{course.present_hours} / {course.total_hours}</div>
                                        </div>
                                        <div className="stat-item">
                                            <div className="stat-label">{course.status}</div>
                                            <div className={`stat-value ${course.status !== "Remaining bunks" ? 'text-danger' : ''}`}>
                                                {course.status === "Remaining bunks" ? course.count : `Attend ${course.count}`}
                                            </div>
                                        </div>
                                    </div>

                                    <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px dashed rgba(255,255,255,0.1)' }}>
                                        <div style={{ fontSize: '0.9rem', marginBottom: '8px', color: 'var(--primary)', fontWeight: '600', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px' }}>
                                            <Wand2 size={14} /> Interactive Predictor
                                        </div>
                                        {renderSimulateControls(course)}
                                    </div>

                                    {course.updated_till && !course.isSimulated && (
                                        <div style={{
                                            textAlign: 'center',
                                            fontSize: '0.8em',
                                            color: 'var(--text-secondary)',
                                            marginTop: '15px',
                                            paddingTop: '10px',
                                        }}>
                                            Updated till: {course.updated_till}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    </>
                )}
            </div>

            {showPopup && (
                <div className="popup">
                    <div className="popup-content">
                        <div className="popup-icon">ℹ️</div>
                        <div className="popup-text">
                            <strong>Predictor:</strong> Use +/- to see how future classes impact your percentage.<br />
                            Normal bunks ensure physical attendance &gt; 75%,
                            exemption bunks ensure exemption &gt; 75% and physical &gt; 65%.
                        </div>
                        <button className="close-btn" onClick={() => setShowPopup(false)}>×</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Attendance;
