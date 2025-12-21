# Michael Gar Fan Page - Project Guide

## Project Overview
This is a fan page website for Michael Gar, an elite British triathlete. The site showcases his achievements, career timeline, gallery, and social media presence.

## Tech Stack
- **HTML5** - Semantic markup
- **CSS3** - Custom styling with CSS variables, gradients, animations
- **Vanilla JavaScript** - Intersection Observer for scroll animations, parallax effects
- **Google Fonts** - Montserrat (headings), Open Sans (body)

## Project Structure
```
/
├── index.html          # Main fan page
├── styles.css          # Main stylesheet
├── favicon.svg         # Site favicon
├── news.json           # News articles data
├── images/             # Image assets
│   ├── gallery/        # Gallery photos
│   └── news/           # News article images
└── admin/              # Admin panel for news management
    ├── index.html      # Admin dashboard
    └── admin.css       # Admin styles
```

## Design System

### Colors (CSS Variables)
- `--primary-color`: #0066cc (Blue)
- `--accent-color`: #00d4aa (Teal)
- `--dark-bg`: #0a1628 (Dark blue background)
- `--darker-bg`: #060d18 (Darker background)
- `--card-bg`: #12233d (Card background)
- `--text-light`: #ffffff
- `--text-muted`: #a0aec0
- `--gradient-primary`: Blue to teal gradient

### Typography
- Headings: Montserrat (weights: 400, 600, 700, 800)
- Body: Open Sans (weights: 400, 600)

## Key Sections
1. **Hero** - Full-screen banner with badges, CTA buttons
2. **About** - Bio, stats cards, blockquote
3. **News** - Dynamic news cards loaded from `news.json`, supports images/YouTube/external links
4. **Achievements** - Timeline of career milestones
5. **Gallery** - Photo grid with lightbox
6. **Fan Comments** - Testimonial cards
7. **Follow** - Social media links (Instagram, World Triathlon, British Triathlon)
8. **World Triathlon Stats** - Rankings and results table

## News System
- **Data**: Articles stored in `news.json`
- **Fields**: id, title, date, content, image, youtubeUrl, externalLink, category
- **Categories**: announcement, race-result, training, media, other
- **Display**: Responsive card grid with scroll animations
- **Admin link**: Subtle lock icon in news section header

## Admin Panel
- Located at `/admin/`
- Password protected (session-based, password: michaelgar2025)
- Form to create news articles with all fields
- Generates JSON for copy/paste into `news.json`
- Step-by-step instructions for adding articles

## Social Links
- Instagram: @michaelgar_tri
- World Triathlon: Profile ID 160628
- British Triathlon: GB Elite Team profile

## Sponsor
- 707 Team Minini (https://www.707team.com/)

## Key Features
- Responsive design (mobile-first approach)
- Scroll-triggered animations via Intersection Observer
- Parallax effects on hero section
- Gradient text and buttons
- Custom styled scrollbars
- Animated badges and cards

## Recent Updates
- Added News section with dynamic JSON-powered article cards
- Redesigned admin panel with modern UI, password toggle, step-by-step instructions
- Added British Triathlon profile link
- Added 707 Minini sponsor button
- Added British Champion 2025 badge
