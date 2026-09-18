import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Smartphone, LayoutGrid, Image, Layers } from 'lucide-react';
import PromoLoadingScreen from './PromoLoadingScreen';
import './PromoPreview.css';

const VARIANTS = [
    {
        id: 'balanced',
        num: '1',
        name: 'Balanced Compact',
        icon: LayoutGrid,
        desc: 'Proportionally scaled poster with tight hierarchy & CTA above the fold',
        path: '/promo-preview-1'
    },
    {
        id: 'hero',
        num: '2',
        name: 'Cinematic Hero Banner',
        icon: Image,
        desc: 'Wide panoramic top banner with event details & ₹14k prize front-and-center',
        path: '/promo-preview-2'
    },
    {
        id: 'side-by-side',
        num: '3',
        name: 'Side-by-Side Mini',
        icon: Layers,
        desc: 'Poster thumbnail beside title at the top, 100% visible with zero scrolling',
        path: '/promo-preview-3'
    }
];

function PromoPreview({ initialVariant }) {
    const location = useLocation();
    const navigate = useNavigate();

    // Determine initial variant based on prop, query param, or path
    const getActiveVariantFromRoute = () => {
        if (initialVariant) return initialVariant;
        if (location.pathname.includes('-1')) return 'balanced';
        if (location.pathname.includes('-2')) return 'hero';
        if (location.pathname.includes('-3')) return 'side-by-side';

        const params = new URLSearchParams(location.search);
        const qVariant = params.get('variant');
        if (qVariant === '1' || qVariant === 'balanced') return 'balanced';
        if (qVariant === '2' || qVariant === 'hero') return 'hero';
        if (qVariant === '3' || qVariant === 'side-by-side') return 'side-by-side';

        return 'hero';
    };

    const [selectedVariant, setSelectedVariant] = useState(getActiveVariantFromRoute);

    useEffect(() => {
        setSelectedVariant(getActiveVariantFromRoute());
    }, [location.pathname, location.search, initialVariant]);

    const handleSelectVariant = (vId) => {
        setSelectedVariant(vId);
        const match = VARIANTS.find(v => v.id === vId);
        if (match) {
            navigate(match.path, { replace: true });
        }
    };

    const currentMeta = VARIANTS.find(v => v.id === selectedVariant) || VARIANTS[0];

    return (
        <div className="promo-preview-page">
            {/* Mobile View Switcher Bar */}
            <header className="promo-preview-toolbar">
                <div className="promo-toolbar-header">
                    <div className="promo-toolbar-badge">
                        <Smartphone size={15} />
                        <span>Mobile Layout Preview</span>
                    </div>
                    <span className="promo-active-badge">Option {currentMeta.num}: {currentMeta.name}</span>
                </div>

                {/* Pill Switchers */}
                <div className="promo-variant-pills" role="tablist">
                    {VARIANTS.map((v) => {
                        const Icon = v.icon;
                        const isActive = selectedVariant === v.id;
                        return (
                            <button
                                key={v.id}
                                type="button"
                                role="tab"
                                aria-selected={isActive}
                                className={`promo-variant-btn ${isActive ? 'active' : ''}`}
                                onClick={() => handleSelectVariant(v.id)}
                            >
                                <Icon size={14} />
                                <span className="btn-label">Option {v.num}: {v.name.split(' ')[0]}</span>
                            </button>
                        );
                    })}
                </div>

                <p className="promo-variant-hint">
                    ✨ {currentMeta.desc}
                </p>
            </header>

            {/* The Actual Promo Screen Component with the chosen variant */}
            <main className="promo-preview-stage">
                <PromoLoadingScreen
                    statusMessage="Simulating fast loading..."
                    subMessage={`Previewing Option ${currentMeta.num} (${currentMeta.name})`}
                    variant={selectedVariant}
                />
            </main>
        </div>
    );
}

export default PromoPreview;
