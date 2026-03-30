class Theme:
    
    DARK = {
        'bg_window': '#0a0e1a',
        'bg_card': '#1f2937',
        'bg_card_alt': '#1a1a2e',
        'bg_input': '#0f0f1a',
        'bg_button': '#374151',
        'bg_button_hover': '#4b5563',
        
        'text_primary': '#f9fafb',
        'text_secondary': '#9ca3af',
        'text_muted': '#6b7280',
        
        'accent': '#8b5cf6',
        'accent_hover': '#a78bfa',
        'accent_light': '#c4b5fd',
        
        'success': '#10b981',
        'success_hover': '#059669',
        'warning': '#f59e0b',
        'danger': '#ef4444',
        'danger_hover': '#dc2626',
        
        'border': '#374151',
        'glow': '#8b5cf6',
    }
    
    LIGHT = {
        'bg_window': '#f8fafc',
        'bg_card': '#ffffff',
        'bg_card_alt': '#f1f5f9',
        'bg_input': '#ffffff',
        'bg_button': '#e2e8f0',
        'bg_button_hover': '#cbd5e1',
        
        'text_primary': '#1e293b',
        'text_secondary': '#64748b',
        'text_muted': '#94a3b8',
        
        'accent': '#7c3aed',
        'accent_hover': '#8b5cf6',
        'accent_light': '#a78bfa',
        
        'success': '#059669',
        'success_hover': '#047857',
        'warning': '#d97706',
        'danger': '#dc2626',
        'danger_hover': '#b91c1c',
        
        'border': '#e2e8f0',
        'glow': '#7c3aed',
    }


class Config:
    
    WINDOW_WIDTH = 1050
    WINDOW_HEIGHT = 780
    WINDOW_MIN_WIDTH = 950
    WINDOW_MIN_HEIGHT = 720
    WINDOW_TITLE = "VibeRandom 1.0"
    
    SPIN_DURATION = 1500
    SPIN_ITERATIONS = 25
    CONFETTI_COUNT = 80
    
    RESULT_MIN_WIDTH = 450
    RESULT_FONT_SIZE = 42
    
    DEFAULT_VALUES = [
        "Test",
        "Test1",
    ]


theme = Theme()
config = Config()
