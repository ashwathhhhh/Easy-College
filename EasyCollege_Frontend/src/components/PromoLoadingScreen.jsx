import React from 'react';
import { motion } from 'framer-motion';
import {
    Loader2,
    Calendar,
    MapPin,
    Trophy,
    ExternalLink,
    Phone,
    Users,
    Sparkles
} from 'lucide-react';
import { CLUB_EVENTS, DEFAULT_PROMO_EVENT } from '../data/clubEvents';
import './PromoLoadingScreen.css';

function PromoLoadingScreen({
    statusMessage = 'Loading campus data...',
    subMessage = 'Hang tight! Check out what’s happening on campus 👇',
    event = DEFAULT_PROMO_EVENT,
    variant = 'hero'
}) {
    const promoEvent = event || CLUB_EVENTS[0];

    return (
        <div className={`promo-loading-container promo-container-${variant}`}>
            {/* Top Loading Header */}
            <motion.div
                className="promo-loading-header"
                initial={{ opacity: 0, y: -12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
            >
                <div className="promo-status-badge">
                    <Loader2 size={18} className="promo-spinner" />
                    <span className="promo-status-text">{statusMessage}</span>
                </div>
                <p className="promo-sub-text">{subMessage}</p>
            </motion.div>

            {/* CommitCon Spotlight Showcase Card */}
            <motion.div
                className={`promo-spotlight-card promo-variant-${variant}`}
                initial={{ opacity: 0, scale: 0.98, y: 10 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                transition={{ duration: 0.45, ease: 'easeOut' }}
            >
                {variant === 'side-by-side' ? (
                    <div className="promo-sbs-wrapper">
                        {/* Top Row: Mini Thumbnail Poster + Title & Badges */}
                        <div className="promo-sbs-top-row">
                            <a
                                href={promoEvent.link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="promo-sbs-thumb-frame"
                                aria-label="View CommitCon poster and register"
                            >
                                <img
                                    src={promoEvent.posterImage}
                                    alt={promoEvent.title}
                                    className="promo-sbs-thumb-img"
                                    loading="eager"
                                />
                                <div className="promo-sbs-thumb-badge">
                                    <ExternalLink size={11} />
                                </div>
                            </a>

                            <div className="promo-sbs-top-info">
                                <div className="promo-header-row">
                                    <span className="promo-badge">
                                        <Sparkles size={11} /> {promoEvent.badge}
                                    </span>
                                </div>
                                <h2 className="promo-event-title promo-sbs-title">{promoEvent.title}</h2>
                                {promoEvent.subtitle && (
                                    <p className="promo-event-subtitle promo-sbs-subtitle">{promoEvent.subtitle}</p>
                                )}
                                <span className="promo-club-pill promo-sbs-club">
                                    {promoEvent.clubName}
                                </span>
                            </div>
                        </div>

                        {/* Bottom Content: Highlights & CTA */}
                        <div className="promo-sbs-body">
                            <div className="promo-meta-grid promo-sbs-grid">
                                {promoEvent.prizes && (
                                    <div className="promo-meta-chip promo-prize-chip">
                                        <Trophy size={13} className="promo-meta-icon text-amber" />
                                        <span>{promoEvent.prizes}</span>
                                    </div>
                                )}
                                <div className="promo-meta-chip">
                                    <Calendar size={13} className="promo-meta-icon text-gold" />
                                    <span>{promoEvent.date}</span>
                                </div>
                                <div className="promo-meta-chip">
                                    <MapPin size={13} className="promo-meta-icon text-gold" />
                                    <span>{promoEvent.venue}</span>
                                </div>
                            </div>

                            <p className="promo-event-desc promo-sbs-desc">{promoEvent.description}</p>

                            <div className="promo-action-row">
                                <a
                                    href={promoEvent.link}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="promo-cta-gold-btn"
                                >
                                    <span>{promoEvent.ctaText || 'Register Now'}</span>
                                    <ExternalLink size={16} />
                                </a>
                            </div>
                        </div>
                    </div>
                ) : (
                    <>
                        {/* Poster Visual Column */}
                        <div className="promo-poster-col">
                    <a
                        href={promoEvent.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="promo-poster-frame"
                        aria-label="View CommitCon poster and register"
                    >
                        <img
                            src={promoEvent.posterImage}
                            alt={promoEvent.title}
                            className="promo-poster-img"
                            loading="eager"
                        />
                        <div className="promo-poster-overlay">
                            <span className="promo-poster-badge">
                                <ExternalLink size={13} /> Click to Register
                            </span>
                        </div>
                    </a>
                </div>

                {/* Event Details Content Column */}
                <div className="promo-details-col">
                    <div className="promo-header-row">
                        <span className="promo-badge">
                            <Sparkles size={13} /> {promoEvent.badge}
                        </span>
                        <span className="promo-club-pill">
                            {promoEvent.clubName}
                        </span>
                    </div>

                    <div className="promo-title-section">
                        <h2 className="promo-event-title">{promoEvent.title}</h2>
                        {promoEvent.subtitle && (
                            <p className="promo-event-subtitle">{promoEvent.subtitle}</p>
                        )}
                        {promoEvent.eligibility && (
                            <span className="promo-eligibility-tag">
                                <Users size={13} /> {promoEvent.eligibility}
                            </span>
                        )}
                    </div>

                    <p className="promo-event-desc">{promoEvent.description}</p>

                    {/* Event Highlights Meta Grid */}
                    <div className="promo-meta-grid">
                        <div className="promo-meta-chip">
                            <Calendar size={14} className="promo-meta-icon text-gold" />
                            <span>{promoEvent.date}</span>
                        </div>
                        <div className="promo-meta-chip">
                            <MapPin size={14} className="promo-meta-icon text-gold" />
                            <span>{promoEvent.venue}</span>
                        </div>
                        {promoEvent.prizes && (
                            <div className="promo-meta-chip promo-prize-chip">
                                <Trophy size={14} className="promo-meta-icon text-amber" />
                                <span>{promoEvent.prizes}</span>
                            </div>
                        )}
                        {promoEvent.contacts && (
                            <div className="promo-meta-chip promo-contact-chip">
                                <Phone size={13} className="promo-meta-icon" />
                                <span>{promoEvent.contacts}</span>
                            </div>
                        )}
                    </div>

                    {/* Call to Action Button */}
                    <div className="promo-action-row">
                        <a
                            href={promoEvent.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="promo-cta-gold-btn"
                        >
                            <span>{promoEvent.ctaText || 'Register Now'}</span>
                            <ExternalLink size={16} />
                        </a>
                    </div>
                </div>
                </>
            )}
            </motion.div>

            {/* Helper footer */}
            <div className="promo-helper-footer">
                <span>💡 Tip: Clicking registration opens in a new tab without interrupting your session.</span>
            </div>
        </div>
    );
}

export default PromoLoadingScreen;
