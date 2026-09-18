// src/data/clubEvents.js
/**
 * Campus Club Events & Promotional Spotlight Data
 * Configured for CommitCon Hackathon by GitHub Campus Club, PSG College of Technology
 */

export const CLUB_EVENTS = [
    {
        id: 'commitcon-2026',
        clubName: 'GitHub Campus Club under CSEA',
        badge: '⚡ Hackathon & Ideathon',
        badgeColor: '#eab308',
        themeGradient: 'linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%)',
        accentGlow: 'rgba(234, 179, 8, 0.3)',
        accentColor: '#facc15',
        iconType: 'code',
        title: 'CommitCon Hackathon',
        subtitle: 'Ideathon (1st Years) | Hackathon (2nd – 4th Years)',
        eligibility: 'All Departments Welcome',
        description: 'Organised by GitHub Campus Club under CSEA. Compete for cash prizes, build cutting-edge solutions, and level up your developer portfolio.',
        date: 'October 9–10',
        venue: 'PSG College of Technology',
        prizes: 'Prize Pool: ₹14,000',
        contacts: 'Shashwath (98456 77934) • Prithikka (94891 17183)',
        posterImage: '/events/commitcon-poster.jpg',
        ctaText: 'Register Now',
        link: 'https://shorturl.at/mUbH5',
        featured: true
    }
];

export const DEFAULT_PROMO_EVENT = CLUB_EVENTS[0];
