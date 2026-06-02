---
name: 'Terrava AgOS: High-Response Mode'
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
  on-surface-variant: '#b9caca'
  inverse-surface: '#dae2fd'
  inverse-on-surface: '#283044'
  outline: '#849495'
  outline-variant: '#3a494a'
  surface-tint: '#00dce5'
  primary: '#e9feff'
  on-primary: '#003739'
  primary-container: '#00f5ff'
  on-primary-container: '#006c71'
  inverse-primary: '#00696e'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#fff8f7'
  on-tertiary: '#68000a'
  tertiary-container: '#ffd3cf'
  on-tertiary-container: '#bd1e26'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#63f7ff'
  primary-fixed-dim: '#00dce5'
  on-primary-fixed: '#002021'
  on-primary-fixed-variant: '#004f53'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3ad'
  on-tertiary-fixed: '#410004'
  on-tertiary-fixed-variant: '#930013'
  background: '#0b1326'
  on-background: '#dae2fd'
  surface-variant: '#2d3449'
typography:
  display-sos:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.04em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  alert-status:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 32px
  control-gap: 8px
---

## Brand & Style

The design system is a premium, mission-critical interface designed for high-stakes agricultural operations and rapid response management. It targets professional farm operators and industrial agronomists who require immediate cognitive clarity during equipment failures or environmental shifts.

The aesthetic combines **Glassmorphism** with a **High-Contrast "Control Center"** layout. It evokes a sense of technical precision and urgent reliability. Surfaces are layered with translucent glass textures to maintain environmental context, while critical interactive zones utilize dense, high-contrast panels to minimize reaction time. The emotional response is one of controlled authority—the user should feel fully informed and empowered to take decisive action.

## Colors

The palette is optimized for dark-mode environments to reduce eye strain during nighttime monitoring while maximizing the impact of signal colors.

- **Primary (Electric Cyan):** Used for active data streams, interactive focus states, and primary navigation paths.
- **Secondary (Agricultural Green):** Reserved for system-healthy states, growth metrics, and "Go" actions.
- **Tertiary/Emergency Red (#EF4444):** A high-alert token used exclusively for SOS triggers, critical equipment failure, and safety hazards.
- **Neutral:** A deep navy-black base that provides the necessary depth for glassmorphism layers.

Glass effects should use a 75% opacity neutral base with a 20px backdrop blur to ensure legibility over dynamic map backgrounds or video feeds.

## Typography

This design system utilizes a technical, highly legible typographic stack. **Geist** provides a clean, developer-centric clarity for general UI and body text, while **JetBrains Mono** is utilized for telemetry data and coordinates to ensure character distinction.

The `display-sos` level is specifically engineered for critical alerts, featuring tight tracking and heavy weights to command immediate attention. All "Emergency Red" states should pair with `alert-status` labels for maximum visibility. In high-response scenarios, prioritize uppercase labels for secondary metadata to increase scanability.

## Layout & Spacing

The layout follows a **Fixed Grid** model on desktop to ensure that critical controls remain in a predictable physical location for "muscle memory" interaction. A 12-column grid is used for the main dashboard, with 24px gutters.

On mobile devices, the layout reflows into a single-column stack, prioritizing the "Critical Status" header. Spacing is strictly based on a 4px increment system. For rapid response, interactive elements (buttons/toggles) must have a minimum touch target of 48px, separated by at least 8px (`control-gap`) to prevent accidental triggers of adjacent systems.

## Elevation & Depth

Hierarchy is established through **Glassmorphic layering** and **Internal Glows**. 

- **Level 0 (Base):** Dark neutral background, usually a map or satellite feed.
- **Level 1 (Panels):** Backdrop-blur glass surfaces with a 1px inner border (0.1 opacity white) to define edges.
- **Level 2 (Modals/Critical Alerts):** High-contrast, solid backgrounds with an external glow. 

For SOS and high-alert states, the element should not use traditional shadows. Instead, it uses a **Pulsing Outer Glow** tinted with the Emergency Red (#EF4444) token. This pulse should animate between a 4px and 12px blur radius at a 1.5s interval to simulate a physical warning beacon.

## Shapes

The design system utilizes **Soft** geometry (4px base radius) to maintain a modern, technical feel without appearing overly friendly or casual. 

Interactive components like buttons and input fields use `rounded-md` (4px). Larger containers and dashboard cards use `rounded-lg` (8px). SOS buttons and critical overrides use the same 4px radius but are distinguished by their high-contrast fill and thickness rather than increased roundedness.

## Components

### Buttons
- **Primary:** Glass effect with a cyan border and white text.
- **Emergency SOS:** Solid #EF4444 fill, white text (Geist Bold), with a continuous pulse animation. 
- **Action:** JetBrains Mono labels for technical overrides.

### Alerts & Chips
- **Critical Status:** A high-visibility banner spanning the top of the UI. It uses the Tertiary color and `display-sos` typography.
- **Telemetry Chips:** Small, semi-transparent labels with mono fonts for real-time sensor data.

### Input Fields
- Dark, recessed fields with 1px borders that glow cyan when focused. Error states shift the entire border and helper text to Emergency Red.

### Cards (Control Modules)
- Glass panels with integrated headers. During a high-alert state, the card's border-color should transition to #EF4444 to indicate which specific system requires the operator's attention.

### SOS Pulsing System
- Define an animation token `pulse-critical` which toggles the `box-shadow` from `0 0 0px #EF4444` to `0 0 20px #EF4444` to create a visual "heartbeat" for the system during emergency response.