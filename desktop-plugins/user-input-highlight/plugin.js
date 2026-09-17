// Hermes Message Accents — customize the user-message bubble.
// The plugin ID remains stable for existing installations.

import { jsx, jsxs } from 'react/jsx-runtime';
import { useState, useEffect } from 'react';

const SCHEMES = {
    gold: {
        label: 'Neon Gold',
        bg: 'color-mix(in srgb, var(--ui-accent) 22%, var(--ui-bg-elevated))',
        border: 'var(--ui-accent)',
        shadow: '0 4px 16px -2px rgba(218, 165, 32, 0.35)',
        borderWidth: '2px'
    },
    pink: {
        label: 'Cyber Pink',
        bg: 'rgba(255, 20, 147, 0.16)',
        border: '#ff1493',
        shadow: '0 4px 16px -2px rgba(255, 20, 147, 0.35)',
        borderWidth: '2px'
    },
    blue: {
        label: 'Electric Blue',
        bg: 'rgba(0, 191, 255, 0.16)',
        border: '#00bfff',
        shadow: '0 4px 16px -2px rgba(0, 191, 255, 0.35)',
        borderWidth: '2px'
    },
    purple: {
        label: 'Glow Purple',
        bg: 'rgba(138, 43, 226, 0.16)',
        border: '#8a2be2',
        shadow: '0 4px 16px -2px rgba(138, 43, 226, 0.35)',
        borderWidth: '2px'
    },
    emerald: {
        label: 'Vibrant Emerald',
        bg: 'rgba(16, 185, 129, 0.16)',
        border: '#10b981',
        shadow: '0 4px 16px -2px rgba(16, 185, 129, 0.35)',
        borderWidth: '2px'
    }
};

const STYLE_ID = 'user-input-highlight-styles';

export default {
    id: 'user-input-highlight',
    name: 'Hermes Message Accents',
    register(ctx) {
        console.log('[UserInputHighlight] Registering plugin...');

        // Track active scheme reactively so any registered UI components can re-render
        const listeners = new Set();
        let activeScheme = ctx.storage.get('scheme', 'gold');

        function updateStyle(scheme) {
            const config = SCHEMES[scheme] || SCHEMES.gold;
            let el = document.getElementById(STYLE_ID);
            if (!el) {
                el = document.createElement('style');
                el.id = STYLE_ID;
                document.head.appendChild(el);
            }
            el.textContent = `
                .composer-human-message {
                    background: ${config.bg} !important;
                    border-color: ${config.border} !important;
                    border-width: ${config.borderWidth} !important;
                    box-shadow: ${config.shadow} !important;
                    transition: background 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
                }
            `;
        }

        function setScheme(scheme) {
            if (!SCHEMES[scheme]) return;
            activeScheme = scheme;
            ctx.storage.set('scheme', scheme);
            updateStyle(scheme);
            listeners.forEach(fn => fn(scheme));
        }

        // Initialize immediately
        updateStyle(activeScheme);

        // Register custom palette commands in ⌘K
        Object.keys(SCHEMES).forEach(scheme => {
            ctx.register({
                id: `highlight-select-${scheme}`,
                area: 'palette',
                data: {
                    id: `highlight.select.${scheme}`,
                    label: `Highlight User Input: Set to ${SCHEMES[scheme].label}`,
                    run: () => setScheme(scheme)
                }
            });
        });

        ctx.register({
            id: 'highlight-cycle',
            area: 'palette',
            data: {
                id: 'highlight.cycle',
                label: 'Highlight User Input: Cycle Color Scheme',
                run: () => {
                    const keys = Object.keys(SCHEMES);
                    const idx = keys.indexOf(activeScheme);
                    const next = keys[(idx + 1) % keys.length];
                    setScheme(next);
                }
            }
        });

        // Register status bar indicator to easily toggle & see state
        ctx.register({
            id: 'highlight-status',
            area: 'statusBar.right',
            render: () => {
                const [current, setCurrent] = useState(activeScheme);

                useEffect(() => {
                    listeners.add(setCurrent);
                    return () => {
                        listeners.delete(setCurrent);
                    };
                }, []);

                const label = SCHEMES[current]?.label || 'Highlighter';

                return jsxs('button', {
                    type: 'button',
                    className: 'px-2 py-0.5 text-[10px] rounded hover:bg-(--ui-control-active-background) text-(--ui-text-secondary) flex items-center gap-1',
                    onClick: () => {
                        const keys = Object.keys(SCHEMES);
                        const idx = keys.indexOf(current);
                        const next = keys[(idx + 1) % keys.length];
                        setScheme(next);
                    },
                    title: 'Click to cycle user input highlight color',
                    children: [
                        jsx('span', {
                            style: {
                                display: 'inline-block',
                                width: '6px',
                                height: '6px',
                                borderRadius: '50%',
                                backgroundColor: SCHEMES[current]?.border.startsWith('var') ? 'gold' : SCHEMES[current]?.border
                            }
                        }),
                        label
                    ]
                });
            }
        });

        // Return cleanup disposer
        return () => {
            const el = document.getElementById(STYLE_ID);
            if (el) el.remove();
            listeners.clear();
        };
    }
};
