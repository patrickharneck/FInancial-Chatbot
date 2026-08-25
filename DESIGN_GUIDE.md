# 🎨 UI Design Reference Guide

## Color Palette

### Primary Colors
```
Primary Blue:      #1f77b4  (Main accent color)
Secondary Green:   #2ca02c  (Success indicators)
Accent Orange:     #ff7f0e  (Highlights)
```

### Status Colors
```
Success Green:     #4caf50  (✅ Success)
Danger Red:        #d62728  (❌ Errors)
Warning Orange:    #ff9800  (⚠️ Warnings)
Info Blue:         #1f77b4  (ℹ️ Information)
```

### Background Colors
```
Light Gray:        #f8f9fa  (Card backgrounds)
White:             #ffffff  (Main background)
Dark Text:         #2c3e50  (Text color)
Border Gray:       #e0e0e0  (Dividers)
```

### Gradients
```
Sidebar Gradient:  #667eea → #764ba2  (Purple gradient)
Title Gradient:    #667eea → #764ba2  (Purple gradient)
```

---

## Typography

### Font Stack
```
Primary: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
```

### Font Sizes & Weights

| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| Main Title (H1) | 2.5rem | 800 | Page headers |
| Section Header (H2) | 1.8rem | 700 | Major sections |
| Subsection (H3) | 1.3rem | 600 | Subsections |
| Body Text | 0.95rem | 400 | Regular content |
| Caption/Small | 0.85rem | 400 | Helper text |

### Line Height
- Headings: 1.2
- Body Text: 1.6-1.7
- Captions: 1.4

---

## Layout & Spacing

### Padding & Margins
```
Large (2rem):     Page container, major sections
Medium (1.5rem):  Cards, form groups
Small (1rem):     Internal padding, section spacing
Tiny (0.5rem):    Element padding, inline spacing
```

### Border & Border Radius
```
Card Border Radius: 8px
Button Border Radius: 8px
Subtle Border: 1px solid #e0e0e0
Left Border (Accent): 4px solid primary color
```

### Shadows
```
Light Shadow: 0 2px 4px rgba(0,0,0,0.05)
Medium Shadow: 0 4px 12px rgba(0,0,0,0.15)
```

---

## Component Styling

### Buttons

**Primary Button (Gradient)**
```
Background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
Color: White
Padding: 0.6rem 1.5rem
Border Radius: 8px
Font Weight: 600
```

**Secondary Button**
```
Background: White
Border: 1px solid #e0e0e0
Color: #2c3e50
Padding: 0.6rem 1.5rem
Border Radius: 8px
```

**Button Effects**
```
Hover: transform translateY(-2px)
Shadow: 0 4px 12px rgba(0,0,0,0.15)
Transition: all 0.3s ease
```

### Cards/Sections
```
Background: #f8f9fa
Border: 1px solid #e0e0e0
Border Left: 4px solid primary color
Padding: 1.5rem
Border Radius: 8px
Box Shadow: 0 2px 4px rgba(0,0,0,0.05)
```

### Input Fields
```
Border: 1px solid #e0e0e0
Border Radius: 6px
Padding: 0.5rem
Focus: primary color border
```

### Status Badges
```
Active:
  Background: #d4edda (light green)
  Color: #155724 (dark green)
  Padding: 0.25rem 0.75rem
  Border Radius: 20px
  Font Size: 0.85rem
  
Inactive:
  Background: #f8d7da (light red)
  Color: #721c24 (dark red)
```

---

## Page Layouts

### Chatbot Page Structure
```
┌─────────────────────────────────────────┐
│  Header Section (Centered Title)        │
│  Language Indicators (English/Chichewa) │
├──────────────────┬──────────────────────┤
│                  │                      │
│   Sidebar        │   Main Content       │
│   (Settings)     │   - Chat Display     │
│   (Status)       │   - Chat Input       │
│                  │   - Action Buttons   │
│                  │                      │
└──────────────────┴──────────────────────┘
```

### Evaluation Page Structure
```
┌─────────────────────────────────────────┐
│  Header: Evaluation Dashboard           │
├─────────────────────────────────────────┤
│  Settings Row (Size, Type, Run Button)  │
├─────────────────────────────────────────┤
│  Overall Metrics (4 columns)            │
├─────────────────────────────────────────┤
│  Language Performance (2 columns)       │
├─────────────────────────────────────────┤
│  Category Performance (Full width)      │
├─────────────────────────────────────────┤
│  Problematic Queries (Full width)       │
├─────────────────────────────────────────┤
│  Export Options (2 columns)             │
└─────────────────────────────────────────┘
```

---

## Responsive Breakpoints

### Desktop (> 768px)
- Full multi-column layouts
- Sidebar fully expanded
- 2+ column layouts
- Comfortable spacing

### Tablet/Mobile (≤ 768px)
- Reduced padding (1rem vs 2rem)
- Smaller fonts (1.8rem titles vs 2.5rem)
- Single column layouts
- Stacked elements

---

## Icon Usage

### Common Icons Used
```
Navigation:
  💬 Chatbot page
  📊 Evaluation page
  📍 Navigation indicator

Actions:
  🔄 Initialize/Refresh
  🗑️ Delete/Clear
  💾 Save
  📥 Download
  🔊 Audio/Sound

Status:
  ✅ Success/Ready
  ❌ Error/Failed
  ⚠️ Warning
  ℹ️ Information
  🟢 Active
  🔴 Inactive

Settings:
  ⚙️ Settings
  🎤 Voice/Audio
  🎙️ Microphone
  📏 Measurement
  🌍 Language

Features:
  📚 Documents
  🎯 Target/Reranker
  🤖 AI/LLM
  💭 Chat/Message
  📝 Text/Content
  📊 Data/Metrics
```

---

## Accessibility Guidelines

### Color Contrast
- Text on background: 4.5:1 minimum (WCAG AA)
- Large text: 3:1 minimum (WCAG AA)
- Focus indicators: High contrast

### Font Sizes
- Minimum: 0.85rem (captions)
- Body: 0.95rem+ (easily readable)
- Headers: 1.3rem+ (clear hierarchy)

### Spacing
- Adequate padding between clickable elements
- Clear visual separation between sections
- Sufficient line height for readability

### Interactive Elements
- Clear hover states
- Visible focus indicators
- Descriptive button labels
- Tooltips for abbreviations

---

## Animation & Transitions

### Hover Effects
```
Button Hover:
  - translateY(-2px)
  - box-shadow increase
  - transition: all 0.3s ease

Expandable Sections:
  - Smooth open/close
  - Icon rotation
  - No jarring movements
```

### Loading States
```
Spinner: 🔍 icon with text
Progress: Visual progress bar
Status: Clear status messages
```

---

## Best Practices

### For Developers
1. Keep consistent spacing using defined sizes
2. Use CSS variables for colors
3. Maintain button size consistency
4. Use semantic HTML
5. Test responsive design

### For Users
1. Clear visual hierarchy guides attention
2. Status indicators provide feedback
3. Spacing reduces cognitive load
4. Consistent styling aids usability
5. Colors convey meaning (status)

---

## Customization

### To Change Colors
Edit the CSS variables in `apply_custom_styling()`:

```css
:root {
    --primary-color: #YOUR_COLOR;
    --secondary-color: #YOUR_COLOR;
    /* ... etc ... */
}
```

### To Change Fonts
Modify the font stack:

```css
body {
    font-family: 'Your Font', sans-serif;
}
```

### To Add New Components
1. Follow existing spacing conventions (1rem, 1.5rem, 2rem)
2. Use color variables instead of hardcoded colors
3. Add proper border radius (8px for cards, 6px for inputs)
4. Include hover states for interactive elements

---

## Design Philosophy

### Modern Professional
- Clean, minimal design
- Professional color palette
- Clear visual hierarchy
- Smooth interactions

### User-Centric
- Intuitive navigation
- Clear feedback
- Helpful guidance
- Accessible design

### Performance-Focused
- Lightweight styling
- No heavy animations
- Quick page load
- Responsive behavior

---

**Version**: 2.0  
**Last Updated**: February 2026  
**Status**: Complete ✅
