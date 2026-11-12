---
framework_version: 1.1.0
---

# Job Evaluation Framework

<!-- SETUP: Skill match areas and career goals are personalized by running /setup -->

## Eligibility Gate — run before scoring

UK work authorisation is confirmed. Canadian visa approval is targeted for February 2027 and remains pending. In Australia the candidate seeks employer sponsorship. For each role, read its specific hiring-country, residency, right-to-work, sponsorship and clearance requirements. Check where the employer allows the work to be performed, both before and after the planned move to Canada. Check the candidate's authorisation for each relevant period separately. Use the posting's exact wording and source.

- **Compatible:** The employer allows the relevant work location and the candidate has confirmed they meet the role's requirements.
- **Verify:** The posting is silent or ambiguous, authorisation or timing is unconfirmed, or a move would need employer approval. Keep the opportunity visible with the specific open question.
- **Incompatible:** A stated requirement conflicts with a confirmed fact. Explain the mismatch. Treat a UK-only or Canada-only role according to the period it could cover.

An employer's headquarters, a general international hiring statement and the word “remote” are insufficient to establish eligibility for a particular opening.

## Scoring Dimensions

Evaluate each job posting against these five dimensions:

### 1. Technical Skills Match (0-100)
How well do the required/preferred skills align with the candidate's capabilities?

| Score | Meaning |
|-------|---------|
| 80-100 | Core requirements are primary skills |
| 60-79 | Most requirements match, 1-2 gaps that are learnable |
| 40-59 | Partial match, significant upskilling needed |
| 0-39 | Fundamental mismatch |

**Strong match areas:** Proteomics data analysis, applied statistics and ML, Python, SQL, analytics, dashboards, biomedical AI evaluation and client-facing analysis.
**Transferable skills:** Scientific writing and editing, GCP training, participant coordination, research documentation, account growth and sales negotiation.
**Check against each posting:** Independent clinical trial management, regulatory submission writing, formal journal review, pharmaceutical territory sales, advanced SAS or production bioinformatics pipeline ownership. These are not documented in the master CV.

### 2. Experience Match (0-100)
Does work history align with what they're looking for?

| Score | Meaning |
|-------|---------|
| 80-100 | Direct experience in the same domain and role type |
| 60-79 | Related experience, transferable skills clear |
| 40-59 | Adjacent experience, would need to make the case |
| 0-39 | Unrelated experience |

**Direct experience:** Bioinformatics research on chronic pain, ML research, biomedical AI evaluation, data analysis, automation, client training and account management.
**Adjacent experience:** Medical communications and clinical research support draw on manuscript contributions, scientific accuracy review, GCP training and participant research. Pharma sales draws on client acquisition and contract negotiation.
**Level:** Prefer entry to mid level. Compare required independence and qualifications with actual experience, including for titles without a level.

### 3. Behavioral/Culture Fit (0-100)
Does the role and company culture match the behavioral profile?

| Score | Meaning |
|-------|---------|
| 80-100 | Culture strongly matches behavioral preferences |
| 60-79 | Mixed signals but mostly compatible |
| 40-59 | Some friction areas |
| 0-39 | Significant culture mismatch |

**Red flags to research:** Department disorganization, work dominated by maintenance over development, poor chemistry with leadership, culture mismatches. Check reviews, media coverage, LinkedIn connections, and network contacts for insider perspective.

### 4. Location & Logistics (Pass/Fail + Notes)
- Fully remote is the primary search scope. In Australia, also consider in-person or hybrid roles with employer sponsorship for the specific vacancy. Record the country or countries from which the employer permits work.
- Prefer roles compatible with the UK-to-Canada move. Include single-country options with the applicable period and flag occasional travel.
- Time zones and irregular hours are acceptable. Field sales and regular office or site attendance fall outside the remote search. They can fit the Australian sponsorship search.

### 5. Career Alignment & Motivation (0-100)
Does this role advance career goals and contain tasks that energize?

| Score | Meaning |
|-------|---------|
| 80-100 | Strongly aligned with career direction, clear growth path |
| 60-79 | Good role but only partially aligned with long-term goals |
| 40-59 | Decent job but doesn't build toward career goals |
| 0-39 | Dead end or backwards step |

**Career goals:** Remote bioinformatics is the first choice. Other medical research and pharmaceutical work is a priority, including clinical trials, biostatistics, medical writing, content editing, publication review and sales. After the three medical and pharmaceutical priorities, prefer remote ML and AI, then remote marketing, then general Python development and broader data work. For ML roles, look for evidence from applied modelling, NLP and biomedical AI evaluation. For marketing, match the channel and duties to experience in programmatic campaigns, tracking, client analytics, SEO, PPC, content or email.

Use those stated priorities when assessing motivation. Salary expectations, management preferences and specific draining tasks are unspecified.

### 6. Salary Benchmark (Optional)

If the salary lookup tool is configured (`salary_data.json` exists), look up the company:
```
python salary_lookup.py "<Company Name>" --json
```

If a city is known from the posting, add `--city "<City>"` to narrow results.

Present findings as:
```
### Salary Benchmark
| Metric | Value |
|--------|-------|
| [Category] index | XX.X (+/-X.X% vs baseline) |
| Overall index | XX.X (+/-X.X% vs baseline) |
```

Interpret results relative to the baseline defined in the data file's metadata. For index-based data, higher typically means above-market compensation.

If the salary tool is not configured, skip this section.

## Output Format

Present the evaluation as:

```
## Job Fit Evaluation: [Role] at [Company]

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical Skills | XX/100 | [brief note] |
| Experience Match | XX/100 | [brief note] |
| Behavioral Fit | XX/100 | [brief note] |
| Location | PASS/FAIL | [brief note] |
| Career Alignment | XX/100 | [brief note] |

**Overall Score: XX/100** (weighted average of scored dimensions)

### Verdict: [Strong Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit]

### Key Strengths for This Role
- [bullet points]

### Gaps to Address
- [bullet points]

### Recommendation
[1-2 sentences: apply/skip/apply with caveats]

### Company Research Checklist
- [ ] Checked company website (mission, values, recent news)
- [ ] Checked review sites (Glassdoor, Jobindex, etc.)
- [ ] Checked LinkedIn for team size, recent hires, connections
- [ ] Checked media for restructuring, growth, or workplace issues
- [ ] Identified network contacts who may know the team/manager
```

## Weighting
- Technical Skills: 30%
- Experience Match: 25%
- Behavioral Fit: 15%
- Career Alignment: 30%

(Location is pass/fail, not weighted)

## Thresholds
- **Strong Fit** (75+): Definitely apply, tailor everything
- **Good Fit** (60-74): Apply, address gaps in cover letter
- **Moderate Fit** (45-59): Consider carefully, discuss with user
- **Weak Fit** (30-44): Probably skip unless strategic reasons
- **Poor Fit** (<30): Skip

## Pre-Application: Call the Employer (Best Practice)

Before writing the application, consider whether the candidate should call the contact person listed in the posting. **Only call if there are substantive questions** - never call just to "be remembered."

### When to Suggest Calling
- The posting has unclear or ambiguous requirements
- It's unclear which competencies are essential vs. nice-to-have
- The role description is vague about day-to-day tasks
- There's a named contact person who invites questions

### Good Questions to Ask
- "What are the primary challenges in this role?"
- "How is time typically divided across the listed responsibilities?"
- "Which competencies are most critical for success in this position?"
- "What does success look like in the first 6-12 months?"

### Rules for the Call
- Prepare a 30-second "elevator pitch" about your background in case they ask
- The call's purpose is **gathering information**, not delivering a pitch
- Take notes - use what you learn to tailor the application
- Reference the conversation naturally in the cover letter ("After speaking with [name], I was especially drawn to...")
