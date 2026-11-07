# ☕ Love Over Coffee (LOC) Jaipur — Web App & Digital Menu Brochure System

> **Jaipur's Iconic Late-Night Specialty Cafe & Bistro**  
> Serving handcrafted Arabica coffees, signature frappes, artisanal sourdough melts, and comforting gourmet bites until **4:00 AM**.

---

## 🌟 Brand Highlights & Description

> *"Where specialty roast craft meets Jaipur’s vibrant late-night cafe culture. Handcrafted single-origin espressos, signature iced hazelnut frappes, artisanal sourdough melts, and comforting gourmet bites — thoughtfully prepared with culinary passion and served fresh until 4:00 AM."*

---

## 🏛️ Multi-View Architecture

1. **Home Landing View (`#/`)**:
   - Asymmetric 55/45 split hero section in Deep Forest Green (`#11261F`) with editorial serif typography (`Playfair Display`) and golden caramel script accent (`Caveat`).
   - 4-Column value proposition strip (100% Arabica, Open Till 4 AM, Cozy Ambience, 4.3★ Rating).
   - "Our Specials" with real-time category filtering and instant cart addition.
   - "Our Story" split banner featuring the C-16 JLN Road chapter and amber neon sign.
   - Special Offer polaroid frame with rosette latte art and instant 20% discount coupon generator.
   - Customer Google reviews carousel with authentic Jaipur testimonials.
   - Comprehensive footer with outlet addresses, contact details, and social channels.

2. **The Menu Gateway View (`#/menu-gateway`)**:
   - Elegant full-screen modal card layout with `← Back to Home`.
   - **Card 1 — Download Complete Brochure**: Direct print/PDF formatting with `window.print()` containing all 55+ items, descriptions, and outlet directory.
   - **Card 2 — Visit Live Menu with Prices**: Transitions smoothly into the interactive digital brochure.

3. **Full Interactive Menu & Printable Brochure (`#/menu-brochure`)**:
   - Sticky header with search input, 10 category filter pills, `📥 Download Brochure (PDF)`, and direct **WhatsApp Quick-Order** (`+91 79761 98506`).
   - Complete C-Scheme Jaipur dataset across 10 categories (55+ items with exact pricing in ₹ and culinary tags).
   - Print-optimized `@media print` styling for clean, professional PDF export.

---

## 📍 Jaipur Outlets & Timings

- **C-Scheme Flagship (4.6★):** F-5, Jamnalal Bajaj Marg, Ashok Nagar, C-Scheme, Jaipur (`+91 79761 98506`)
- **Tonk Road Late-Night Hub:** B2 Bypass, Opp. Bella Casa, Surplus House, Jaipur (`072320 99909` / `+91 99287 83999` — *Open till 4:00 AM*)
- **JLN Road (New Chapter):** C-16, JLN Road, Jawahar Circle, Near Airport Terminal 2
- **Durgapura HQ:** S-7 Lakhanpuri, Durgapura, Jaipur (`+91 99287 83999`)
- **Neighborhood Outlets:** Vaishali Nagar, Vidhyadhar Nagar & Jagatpura

---

## 🛠️ Tech Stack & Design System

- **Styling:** Tailwind CSS (Custom Beanona Coffee & Café editorial theme)
- **Icons:** Lucide Icons
- **Fonts:** Playfair Display, Caveat, Plus Jakarta Sans
- **Interactivity:** Vanilla JS router (`hashchange`), slide-over shopping bag drawer, live search modal, animated toast alerts.

---

## 🚀 Running Locally

```bash
# Serve with any static web server
python3 -m http.server 4321
# Open http://localhost:4321
```
