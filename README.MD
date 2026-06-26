# Karuna's Laboratory Website

This is a static GitHub Pages website for Karuna's Laboratory.

The site is intentionally simple:

- `index.html` contains the full page structure, text, links, and styling.
- `pics/` contains the image assets used by the page.
- No build step is required. GitHub Pages can serve the site directly from the repository root.

## Where to Update Content

Open `index.html` and search for the `CONTENT:` comments.

### Lab Name, Navigation, and Logo

Search for:

```html
<!-- CONTENT: site navigation and lab identity -->
```

Update:

- Lab name
- Faculty/institution subtitle
- Navigation links
- Contact button text
- Logo image path

Logo file:

```text
pics/karuna-logo.png
```

### Homepage Hero

Search for:

```html
<!-- CONTENT: homepage hero -->
```

Update:

- Main headline
- Intro paragraph
- Hero buttons
- Publication/citation/h-index numbers
- Research atlas caption

Research atlas file:

```text
pics/karuna-lab-map.png
```

### About / Principal Investigator

Search for:

```html
<!-- CONTENT: about the PI and lab identity -->
```

Update:

- PI name
- Short biography
- Affiliations
- Lab mission text

Photo file:

```text
pics/IMG_3795.jpg
```

### Research Pillars

Search for:

```html
<!-- CONTENT: research pillars -->
```

Update the four research directions:

- Clinical research
- Basic research
- Collaboration
- Technology

### Publications and Profile Links

Search for:

```html
<!-- CONTENT: publications and profile links -->
```

Update:

- Publication metrics
- Research areas
- Google Scholar link
- ResearchGate link
- ORCID link

Current profile links:

```text
Google Scholar: https://scholar.google.com/citations?user=GNqb7rYAAAAJ&hl=en
ResearchGate: https://www.researchgate.net/profile/Narainrit-Karuna
ORCID: https://orcid.org/0000-0002-4050-7469
```

### Research Projects

Search for:

```html
<!-- CONTENT: research projects -->
```

Each project is an `<article class="project-card">`.

To add a project, copy one existing project card and update:

- Number
- Title
- Description
- Status

### Speaking and Presentations

Search for:

```html
<!-- CONTENT: selected speaking entries -->
```

Each talk is an `<article class="talk">`.

Add newest talks at the top.

### Contact

Search for:

```html
<!-- CONTENT: contact and collaboration -->
```

Update:

- Email
- Department
- Faculty
- Address
- Collaboration message

## Image Files

Current image assets:

```text
pics/karuna-logo.png       Lab logo
pics/karuna-lab-map.png    Translational research atlas
pics/IMG_3795.jpg          PI photo
pics/cardiateam.jpg        Existing project/team photo, not currently displayed
```

## Local Preview

From the repository folder, run:

```bash
python3 -m http.server 8765
```

Then open:

```text
http://127.0.0.1:8765/
```

For GitHub Pages, push changes to the repository and the site will update after GitHub rebuilds Pages.
