# FoodHole (ตั้งหลัก)

> The repository and branch remain named `foothold`; `FoodHole` is the project name used for this portfolio presentation.

A Thai-language prototype that helps people organise next steps when a bank account has been restricted or associated with a suspected mule-account investigation.

> **Scope:** This is a concept and demonstration project. It does not claim real users, revenue, legal outcomes, or production adoption. It is not legal advice and should not replace a qualified lawyer or official guidance.

## Project Overview

Foothold converts a stressful, complex situation into a guided, browser-based workflow. A user can identify a situation, organise facts and a timeline, prepare evidence, review practical checklists, and draft documents for a conversation with a bank or investigator.

The current implementation is a static HTML/CSS/JavaScript prototype. It is designed to run without a backend database so that entered information stays in the browser during the demonstration.

## Business Problem

People affected by account restrictions may not know:

- what their reported status means;
- which documents or evidence to gather;
- how to explain events in chronological order;
- which organisation to contact next; or
- how to prepare a clear first draft without sharing sensitive information with a third-party server.

This creates avoidable confusion and makes coordination with banks, investigators, or legal support more difficult.

## Solution

Foothold provides a structured self-guidance experience:

1. Select the situation that best matches the user's information.
2. Follow a status-specific route toward a bank, investigator, or support channel.
3. Record facts and build a chronological timeline.
4. Prepare evidence and an appointment checklist.
5. Generate a draft document from the information entered in the browser.
6. Print or download the draft for review by an appropriate professional.

The prototype is intentionally rule-based and content-led. It does not make a legal determination or submit information to an authority.

## Key Features

- Situation assessment and route selection.
- Timeline builder for chronological event summaries.
- Evidence-preservation and appointment-preparation checklists.
- Thai-language document drafting with multiple communication tones.
- Generated statement-of-facts text based on user-entered information.
- Print-to-PDF and downloadable document-template flows.
- Responsive layout with Thai typefaces and contrast-conscious styling.
- Static, dependency-light implementation with no application backend.

## My Role

My contribution to this prototype included:

- Requirement analysis: translated a complex user problem into a guided self-service flow.
- User-flow design: mapped situation selection, status routing, evidence preparation, drafting, and download steps.
- UX/UI planning: structured the information hierarchy, progressive disclosure, alerts, checklists, and document screens.
- Front-end development: implemented the static HTML, CSS, JavaScript state model, rule-based routing, forms, and document generation.
- Testing and validation: reviewed content flows, form states, download paths, responsive layout considerations, and accessibility-related contrast changes.
- Product improvement: iterated on sub-case routing, prep-kit guidance, evidence preservation, document downloads, and multiple drafting tones.

These statements describe work visible in the repository history and source code. No claim is made about production deployment, user adoption, or measured business impact.

## Tech Stack

- HTML5
- CSS3
- Vanilla JavaScript
- Browser APIs for printing and downloading
- Google Fonts: IBM Plex Sans Thai, Noto Serif Thai, and Sarabun
- Static DOCX and PDF templates

## Demo Link

- **Repository:** https://github.com/sakunthaina-collab/foothold
- **Live demo:** No separate live-demo URL was confirmed in the repository. Run the prototype locally using the Installation instructions.

## Screenshots

No screenshot files are currently committed. Do not add broken image links to the README.

Planned files for visual QA:

- `docs/screenshots/homepage.png` — homepage / situation introduction
- `docs/screenshots/status-result.png` — status or route-result screen; the repository does not contain a separate search-results page
- `docs/screenshots/mobile-view.png` — mobile-width view of the main flow

## Installation

### Prerequisites

- A modern web browser
- Python 3, Node.js, or another static-file server

### Run locally

~~~bash
git clone https://github.com/sakunthaina-collab/foothold.git
cd foothold

# Option A: Python
python -m http.server 8000

# Option B: Node.js
npx serve .
~~~

Open http://localhost:8000.

A local HTTP server is recommended so relative document downloads behave consistently.

## Privacy and Sensitive Data

- Do not enter real national ID numbers, bank account numbers, addresses, phone numbers, case IDs, or personal documents during demonstrations.
- The application currently has no documented backend submission flow; this should not be treated as a complete privacy or security guarantee.
- Official contact information embedded in the prototype should be verified against current official sources before public use.
- Do not commit credentials, API keys, tokens, private documents, real customer data, or screenshots containing personal information.

## Future Improvements

- Add automated tests for route selection, form state, and document generation.
- Add a content-review and source-verification process for legal and government information.
- Add a synthetic-data demo mode for presentations and screenshots.
- Add automated HTML, JavaScript, link, accessibility, and secret scanning in CI.
- Separate content, rules, and UI into maintainable modules.
- Add a reviewed English-language content layer.
- Add visual regression checks for desktop and mobile layouts.
- Add a formal privacy notice and threat model before introducing any backend.
- Confirm and document an approved live-demo deployment before publishing a production link.

## License

No explicit license was confirmed during the repository review. Add a license before presenting this as reusable open-source software.