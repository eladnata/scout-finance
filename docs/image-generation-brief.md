# Scout Finance — Image Generation Brief

This document lists every photograph the website needs, with enough detail to hand each entry to an AI image generator (e.g. ChatGPT/DALL·E, Midjourney) as its own prompt. Copy one section at a time — do not combine slots into a single prompt.

## Brand context (include this in every prompt)

Scout Finance is an Israeli audit, financial-control and management-consulting firm serving complex organizations, including cross-border groups. The site's visual identity is **quiet institutional authority** — closer to a serious accounting/audit firm than a flashy startup. Every image must share this register:

- **Palette:** deep navy (#03162A, #06203D), steel blue (#145B9F, #176BBD), cool gray (#67798B), white and soft off-white. No warm tones, no gold, no bright accent colors.
- **Lighting:** natural or soft architectural office lighting. Nothing glossy, nothing stock-photo-glamorous.
- **Mood:** documentary and restrained, not staged or promotional. Real working moments, not posed "success" shots.
- **Universally avoid across every image:** handshakes, thumbs-up, forced smiles, visible screens with fabricated data/charts/dashboards, laptop screens facing camera, generic stock-photo clichés (people pointing at whiteboards, high-fiving), any flags, glowing world maps, tourism landmarks, or airport departure boards, gold/luxury styling, glassmorphism, obvious AI artifacts (extra fingers, warped text, nonsensical documents).
- **Do not include any text, logos, charts, or numbers that would need to be legible** — if paperwork appears, it should read as generic blurred/out-of-focus documents, never fabricated real-looking data.

Each image below will be placed into a **responsive image slot** on the site, so composition and crop matter as much as subject.

---

## 1. Hero — homepage banner image

**Priority:** P0 (highest — this is the first image every visitor sees)
**File base name:** `hero`
**Required output size:** 1600 × 2000 px (portrait), aspect ratio **4:5**
**Crop safety:** keep all faces and hands within the central 60% of the frame — the site may crop the outer edges on some screen sizes.

**Prompt content:**
A small team of finance/audit professionals (2–3 people, mixed gender, business-casual attire — no ties required, but sharp and professional) in a genuine working session around a table, reviewing printed financial control documents. One person is mid-gesture pointing at a physical document, not a screen. The setting is a modern but understated office with navy/steel/neutral tones — glass partitions, muted gray walls, natural window light from one side. Documentary photography style, shallow depth of field, candid rather than posed — as if caught mid-conversation, not looking at camera. No exaggerated smiles; focused, professional expressions.

**Explicitly avoid:** handshakes, visible client data, fabricated charts/dashboards on any screen, direct eye contact with camera, staged "teamwork" clichés.

---

## 2. Leadership — founder portrait

**Priority:** P0
**File base name:** `leadership`
**Required output size:** 1600 × 2000 px (portrait), aspect ratio **4:5**

**⚠️ Important — do not AI-generate this one.** This slot is a portrait of a specific real, named individual (the firm's founder, Tomer Natan). Generating a fabricated photo of a real named person is misleading and should not be published as if it were him. **Recommended: commission or schedule a real photograph instead.**

If you still want an AI-generated placeholder purely to preview the layout (never to publish as the final image), use this prompt and treat the output as a stand-in only:

A professional editorial portrait of a man in his 40s, dark business attire, confident and approachable expression, direct eye contact with the camera, photographed against a softly blurred modern office background (dark navy/steel tones, architectural lines visible but out of focus). Understated, natural lighting — one soft key light, no harsh studio look. Waist-up composition, centered, with headroom above for the crop.

---

## 3. Method — process/methodology section

**Priority:** P1
**File base name:** `method`
**Required output size:** 1800 × 1200 px (landscape), aspect ratio **3:2**

**Prompt content:**
Two or three professionals collaboratively reviewing a printed process map or a bound report spread across a table — visible structure (boxes, flow lines) but no readable text or numbers, treat it as abstract/blurred detail. Setting is the same navy/steel/neutral office environment as the hero image, for visual consistency. Natural light, mid-shot from a slightly elevated angle looking down at the table and the people around it. Documentary style, unposed.

**Explicitly avoid:** whiteboards with visible writing, laptop screens facing the camera, exaggerated pointing gestures.

---

## 4. International — cross-border operations section

**Priority:** P1
**File base name:** `international`
**Required output size:** 1920 × 1200 px (landscape), aspect ratio **16:10**

**Prompt content:**
A credible, modern international-business or logistics environment that conveys cross-border scale without clichés — for example: a modern shipping-port container terminal at dusk with cranes in soft silhouette, OR a clean corporate office lobby with floor-to-ceiling glass overlooking a city skyline at blue hour, OR an airport cargo/logistics facility (working area, not passenger terminal). Cool navy/steel color grading to match the site. Wide, architectural composition with strong horizontal lines.

**Explicitly avoid:** national flags of any kind, glowing/animated-looking world maps, airport passenger departure boards, tourist landmarks (Eiffel Tower, Big Ben, etc.), airplanes in flight as the main subject.

---

## 5. Sector — Public institutions

**Priority:** P2
**File base name:** `sector-public`
**Required output size:** 1600 × 1200 px (landscape), aspect ratio **4:3**

**Prompt content:**
A restrained, documentary-style exterior or interior view of a modern public-sector or government-style institutional building — clean architectural lines, stone or concrete facade, glass entrance, muted daylight. No people needed, or at most one or two in the far distance for scale. Should feel civic and orderly, coordinated in color grading (cool, neutral) with the other sector images below.

**Explicitly avoid:** flags, recognizable government seals/emblems, courthouses or buildings tied to a specific identifiable institution.

---

## 6. Sector — Industry/operations

**Priority:** P2
**File base name:** `sector-industry`
**Required output size:** 1600 × 1200 px (landscape), aspect ratio **4:3**

**Prompt content:**
A real, orderly industrial or operational environment — for example, a clean modern manufacturing floor, a logistics warehouse with organized racking, or a controlled production line — photographed in a documentary style with cool, neutral color grading matching the other sector images. Should feel operational and precise, not gritty or chaotic. Good natural or industrial overhead lighting.

**Explicitly avoid:** visible safety violations, cluttered/messy environments, any branded machinery or visible company logos.

---

## 7. Sector — Mission-driven / nonprofit organizations

**Priority:** P2
**File base name:** `sector-purpose`
**Required output size:** 1600 × 1200 px (landscape), aspect ratio **4:3**

**Prompt content:**
A small team in a modest, genuine nonprofit or mission-driven organizational setting — for example, a community or social-services office space — engaged in real, quiet working activity (reviewing documents, planning at a table). Documentary style, coordinated cool/neutral color grading with the other sector images. Warm human tone but still restrained, not sentimental or overly emotional.

**Explicitly avoid:** stereotypical "charity" imagery (children in poverty, donation boxes with visible currency, exaggerated emotional expressions), any recognizable branding.

---

## After generation — what to do with the files

1. Save each generated image at (or upscale to) its exact required pixel size and aspect ratio listed above.
2. Name the files using the slot's base name, e.g. `hero.jpg`, `method.jpg`, `sector-public.jpg`.
3. Hand the files back so they can be processed into the site's responsive formats (AVIF/WebP/JPEG at multiple sizes) and dropped into `static/assets/images/`.
4. Every image must still go through `docs/image-rights-register.md` — recording its source, licence, and approval — before it can go live on the production site. AI-generated images need their generation tool and date recorded there, and the leadership portrait should be replaced with a real photograph before launch.
