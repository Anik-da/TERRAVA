---
name: Terrava AI-AgOS
colors:
  surface: '#0b1326'
  surface-dim: '#0b1326'
  surface-bright: '#31394d'
  surface-container-lowest: '#060e20'
  surface-container-low: '#131b2e'
  surface-container: '#171f33'
  surface-container-high: '#222a3d'
  surface-container-highest: '#2d3449'
  on-surface: '#dae2fd'
  on-surface-variant: '#bccbb9'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#869585'
  outline-variant: '#3d4a3d'
  surface-tint: '#4ae176'
  primary: '#4be277'
  on-primary: '#003915'
  primary-container: '#22c55e'
  on-primary-container: '#004b1e'
  inverse-primary: '#006e2f'
  secondary: '#8bd79b'
  on-secondary: '#003918'
  secondary-container: '#005829'
  on-secondary-container: '#81cc90'
  tertiary: '#ffba61'
  on-tertiary: '#472a00'
  tertiary-container: '#ef9900'
  on-tertiary-container: '#5c3800'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#6bff8f'
  primary-fixed-dim: '#4ae176'
  on-primary-fixed: '#002109'
  on-primary-fixed-variant: '#005321'
  secondary-fixed: '#a6f4b5'
  secondary-fixed-dim: '#8bd79b'
  on-secondary-fixed: '#00210b'
  on-secondary-fixed-variant: '#005226'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
    letterSpacing: 0em
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0em
  label-caps:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  gutter: 20px
  margin-mobile: 16px
  margin-desktop: 40px
---

## Brand & Style

The design system is engineered for the future of industrial agriculture, positioning the product as a high-capital, intelligent operating system. The aesthetic merges the utilitarian precision of developer tools with the premium finish of high-end aerospace interfaces. 

The visual direction follows a **Modern-Glassmorphic** approach:
- **Atmosphere:** Deeply immersive dark mode using high-density layouts and sophisticated depth.
- **Tone:** Technical, authoritative, and futuristic. It should feel like a command center for a global enterprise.
- **Visual Language:** High-contrast data visualization, translucent glass panels, and precision-engineered micro-interactions.
- **Target Audience:** Large-scale commercial growers, ag-tech investors, and automated farm operators who require reliability and rapid data synthesis.

## Colors

The palette is rooted in the "Deep Navy" of nighttime fields, punctuated by high-vibrancy agricultural greens and "Insight Gold."

- **Primary Green (#22C55E):** Used for growth indicators, active statuses, and primary actions. It signifies health and operational success.
- **Forest Green (#166534):** Used for low-priority UI elements, background fills, and contextual grounding.
- **Gold (#F59E0B):** Reserved for high-value insights, AI-driven suggestions, and premium tier features.
- **Dark Navy (#0F172A):** The foundational canvas. All layers sit on this "Infinite Field" base.
- **White/Off-white (#F8FAFC):** High-contrast typography and subtle surface highlights to ensure legibility in low-light environments.

## Typography

This design system utilizes **Inter** for all primary communication to ensure maximum readability and a clean, technical aesthetic. Headings use tight tracking and heavy weights to evoke a sense of structural strength. 

For data-dense environments, sensor readings, and coordinate systems, **JetBrains Mono** is introduced. This monospaced font provides the necessary precision for "Ag-Data" visualization and developer-grade technical logs.

- **Scale:** High contrast between display types and body copy.
- **Alignment:** Use optical alignment for numbers in tables to ensure "scannability."

## Layout & Spacing

The layout philosophy uses a **12-column fluid grid** for desktop, optimized for high-density dashboard layouts. 

- **Grid:** On desktop, use a 40px margin with 20px gutters. On mobile, transition to a 4-column layout with 16px margins.
- **Rhythm:** A strict 4px baseline grid ensures vertical consistency across data tables and control panels.
- **Density:** The system supports "Standard" and "Compact" views. Compact view reduces vertical padding in lists and tables by 50% for expert users managing massive sensor arrays.

## Elevation & Depth

Depth is achieved through **Glassmorphism** and tonal layering rather than traditional heavy shadows.

- **Tiers:**
  - **Level 0 (Base):** #0F172A. Solid, matte.
  - **Level 1 (Panels):** Semi-transparent #1E293B (80% opacity) with a 12px backdrop blur.
  - **Level 2 (Floating Modals):** Semi-transparent #334155 (60% opacity) with a 24px backdrop blur and a 1px inner stroke of white at 10% opacity.
- **Gradients:** Use subtle "Linear" style gradients on borders (from Primary Green to transparent) to highlight active panels or AI-suggested insights.
- **Shadows:** Only used for high-level overlays; use a single, wide-spread ambient glow (#000000 at 40% opacity, 30px blur).

## Shapes

The shape language is "Soft-Technical." Elements use a subtle 0.25rem (4px) base radius to maintain a professional, sharp-edged feel while avoiding the aggressive nature of pure 0px corners.

- **Base Radius:** 4px (Soft) for buttons, inputs, and small widgets.
- **Large Radius:** 8px (rounded-lg) for main container panels and cards.
- **Extra Large:** 12px (rounded-xl) for global navigation overlays or system-level modals.

## Components

### Buttons
- **Primary:** Solid Primary Green (#22C55E) with Black text. High-gloss finish.
- **Secondary:** Ghost style. Transparent background with a 1px Forest Green border.
- **AI-Action:** Gold (#F59E0B) text with a subtle outer glow effect.

### Cards
- **Sensor Cards:** Glassmorphic background, 1px subtle border, and a "pulse" indicator in the top right for live data status.
- **Insight Cards:** Feature a Gold gradient top-border (2px) to denote AI-generated content.

### Inputs
- **Data Fields:** Dark Navy background, 1px border (#F8FAFC at 10%). On focus, the border glows Primary Green with a 4px outer blur.
- **Toggle Switches:** Rectangular with sharp 2px corners, using Primary Green for the 'On' state.

### Navigation
- **Sidebar:** Fixed glassmorphic panel on the left. Icons use thin strokes (1.5px) and transition from grey to Primary Green on active state.
- **Status Bar:** Top-aligned, high-density bar showing global system health, connectivity, and weather data.

### Lists & Tables
- **Data Rows:** Zebra striping using #1E293B at 30% opacity. Hover state increases the background opacity and adds a 1px border highlight.