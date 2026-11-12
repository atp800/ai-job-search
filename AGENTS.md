---
framework_version: 1.0.0
---

# Agent Guidelines: AI Job Search

This workspace is structured to manage job search activities, scraper tools, CVs, cover letters, and interview preparation.

## Role
This repo is a job application workspace. The AI agent acts as a career advisor and application assistant for the candidate, helping with:
1. **Job fit evaluation** - Assess job postings against the candidate's profile (skills, experience, behavioral traits)
2. **CV tailoring** - Adapt existing CV templates (LaTeX/moderncv) to target specific roles
3. **Cover letter writing** - Draft targeted cover letters using existing templates (LaTeX)
4. **Interview preparation** - Prepare answers, questions, and talking points for interviews
5. **Career strategy** - Advise on positioning and personal branding

## Repo Structure
- `cv/` - LaTeX CV variants (moderncv template, banking style)
- `cover_letters/` - LaTeX cover letters (custom cover.cls template)
- `.claude/skills/job-application-assistant/` - Methodology reference files and Candidate Profile
- `.claude/commands/` - Workflow commands and shared rules for the application process
- `.agents/skills/` - Job search CLI tools

## Canonical Workflow Specifications
The step-by-step instructions and triggers for tasks (setup, scrape, rank, apply, upskill, interview) are defined in the `.claude/commands/` directory.

- Read `.claude/skills/job-application-assistant/01-candidate-profile.md` for the candidate's detailed identity, education, experience, and technical skills.
- Read `.claude/commands/_shared.md` for the core workflow and the mandatory Verification Checklist for all generated documents.
- Portal Search Skills: Job-portal search CLIs live under `.agents/skills/` in the portable Agent Skills format.

## Candidate Profile

Andreas Panayiotou holds a first-class MSci in Natural Sciences from the University of Birmingham, specialising in computer science, AI, biomedical sciences and neuroscience. His experience includes chronic-pain proteomics and manuscript work at Western Sydney University, biomedical AI evaluation at Data Annotation, and Python automation, analytics and client account development at Semetrical. The detailed profile and contact details are in `.claude/skills/job-application-assistant/01-candidate-profile.md`. Build each application from the evidence most relevant to its posting.

CV language: English (default for the English-language master CV).

### Current search

For requests to add, show, change or remove companies from search settings, use the Target company settings section of `.claude/commands/setup.md`. The saved list supplements the normal job boards.

- Seek fully remote entry- and mid-level roles, plus Australian roles offering visa sponsorship with remote, hybrid or in-person work. Bioinformatics is the first choice, including analyst and research data roles with equivalent duties.
- Prioritise medical research and pharmaceuticals, including clinical trials, biostatistics, medical writing, content editing, publication review and pharma sales. Include remote machine learning and marketing roles across industries in routine searches. General Python development and broader data work are the lowest search priority.
- UK work rights are confirmed. Search UK and international remote openings, including US-headquartered employers. Canadian visa approval is a target for February 2027, with timing and permission pending. Keep Canada-only roles as future options where start dates fit. Prefer roles that can continue across the planned move to Canada. Time zones and irregular hours are acceptable.
- Check the specific role's permitted work countries independently of the employer's headquarters and the candidate's own work authorisation. Record location and eligibility uncertainties in each shortlist.
