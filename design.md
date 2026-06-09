# Super SaaS Premium Design System

## Visual Theme & Atmosphere
- **Style:** Ultra-modern, high-end SaaS aesthetic.
- **Philosophy:** Minimalism meets "Glassmorphism" and "Bento Grid" layouts.
- **Vibe:** Professional, futuristic, and extremely premium.

## Color Palette (Tailwind / CSS)
- **Background:** `bg-[#030712]` (Slate-950) with subtle mesh gradients.
- **Primary:** `text-[#6366f1]` (Indigo-500) and `bg-[#6366f1]`.
- **Secondary:** `text-[#ec4899]` (Pink-500) and `bg-[#ec4899]`.
- **Accent:** `text-[#8b5cf6]` (Violet-500).
- **Glass:** `bg-white/5 backdrop-blur-xl border border-white/10`.

## Typography
- **Primary Font:** Inter or Outfit (Sans-serif).
- **Headings:** Bold, tight letter spacing, subtle gradient text for <h1>.
- **Body:** Clean, legible, high contrast (`text-slate-300`).

## Component Stylings
### Buttons
- **Primary:** Rounded-full, indigo-600 to violet-600 gradient, hover:scale-105 transition.
- **Glass:** White/10 background, backdrop-blur, hover:bg-white/20.

### Cards (Bento Style)
- Background: `bg-slate-900/50`.
- Border: `border border-slate-800`.
- Hover: Glow effect using `shadow-[0_0_20px_rgba(99,102,241,0.2)]`.

## Layout Principles
- **Grid:** Responsive Bento Grid for feature sections.
- **Spacing:** Generous whitespace (padding/margin) to breathe.
- **Micro-animations:** Use `framer-motion` for all entries and hover states.

## Do's and Don'ts
- **DO:** Use smooth gradients.
- **DO:** Use Lucide icons for everything.
- **DO:** Include high-quality hero sections with "wow" factors.
- **DON'T:** Use plain red/blue/green.
- **DON'T:** Use sharp corners (use `rounded-2xl` or `rounded-3xl`).
