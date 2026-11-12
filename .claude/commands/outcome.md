# /outcome - Record the Result of an Application

You are recording what happened to a job application: progress updates (interview invitations, stages completed, offers) and final resolutions (hired, rejected, no response). The data lands in two places the framework already reads but nothing systematically writes:

- `job_search_tracker.csv` - the status column that `/scrape` and `/rank` use for dedup and exclusion
- `documents/applications/<company>_<role>_<job_id>/` - the per-application archive (posting, submitted drafts, `outcome.md`) that `/setup` Path A mines to calibrate `04-job-evaluation.md` and surface STAR candidates

`/outcome` writes the data; `/setup` interprets it. This command never edits the evaluation framework or profile files itself.

The command also owns the stretch *before* there is an outcome to record: the **follow-up branch** (Step 2b) surfaces open applications that have gone quiet, drafts a brief follow-up note in the user's voice, and logs it - so the chase and the resolution it eventually leads to live in one flow.

Follow these steps **in order**.

---

## Step 0: Parse Input

`$ARGUMENTS` may contain:

- Nothing → list open applications and ask which one to update
- A submission confirmation, company, role or job ID targets an application. For a newly confirmed submission record status `applied`, archive the submitted versions and posting, and initialise the outcome as `in_progress`; there is no need to wait for an employer response.
- `followup` → enter the follow-up branch (Step 2b) over every quiet open application, using the default threshold of **10 days**
- `followup <N>`, e.g. `/outcome followup 14` → follow-up branch with an N-day threshold
- `followup <company>`, e.g. `/outcome followup acme` → draft a follow-up for that application now, regardless of threshold

---

## Step 1: Load State and Identify the Application

When logging a posting, use `.claude/commands/_match-vacancy.md` before matching by name or allocating a generated ID. A distinct employer requisition starts a new row even if company and role already match. A user-supplied local ID can select its existing row for an update.

1. Read `job_search_tracker.csv`. If it does not exist, create it with the standard header. If it exists with the older thirteen-column header (ending at `source`), extend the header line once with `job_id,country,location,industry`; leave every existing row untouched - missing trailing values read as empty. Never reorder columns and never rewrite existing rows:
   ```
   date,company,sector,role,role_type,channel,status,contact_person,fit_rating,notes,cv_file,cover_letter_file,source,job_id,country,location,industry
   ```
2. **With an argument:** match rows case-insensitively on company (and role, if given). An argument containing a row's exact `job_id` matches that row first, which disambiguates two applications to the same company and role. One match → proceed. Several → list them (with their `job_id` values) and ask. None → the application was made outside the workflow; collect company, role, date applied, channel, posting URL, and the `job_id`, `country`, `location` and `industry` values the posting states - generating a `GEN` ID when it states none - then add a tracker row.
3. **Without an argument:** list all rows whose status is not final (not hired / rejected / no response / withdrawn / offer declined) as a numbered table (company, role, date applied, current status, days quiet, follow-ups sent) and ask which to update. The two derived columns come straight from existing data: **days quiet** counts from the row's `date` or the latest dated entry in `notes`, whichever is more recent; **follow-ups sent** counts the `followed up YYYY-MM-DD` markers in `notes`. If any open row is 10+ days quiet with fewer than two follow-ups sent, add one line under the table: "Some of these have gone quiet - want a follow-up draft? (Step 2b)". If every row is resolved, say so and stop.
4. Resolve the exact archive for the selected row. Use the working-document and archive rules in `.claude/commands/_match-vacancy.md`.

---

### Tracker row fields

`job_id`, `country`, `location` and `industry` are the four columns appended after `source` in the header above. They are additive: rows written before they existed stay valid, so read columns by name, never by position.

- **`job_id`** - the employer's own posting/requisition ID, verbatim (`R-12345`, `JR102938`), when the posting states it as an identifier or it is the ID segment of the posting's ATS URL (Greenhouse, Lever, Workday, SmartRecruiters). If several IDs are plausible, pick one: prefer the value labelled as the posting or requisition identifier, then the ATS URL's ID segment, and name the choice in the Step 6 confirmation so the user can correct it. Never derive an ID from a year, salary, deadline, phone number or other incidental digits. **When no obvious ID exists, generate one as `GEN-YYYYMMDD-NN`** - the row's `date` (today's date when it is not a full ISO date) plus the lowest two-digit sequence from `01` to `99` not already used by an archive folder or tracker row from that date. Never leave `job_id` empty on a new row and never reuse a generated ID. In the folder name the rule lowercases it to `gen-`; the tracker keeps `GEN`.
- **`country`** - the country the role is hired in, as the posting states it, not the employer's headquarters. Empty when unstated.
- **`location`** - the city or area as posted, or the work-location designation when no city is given: `Remote`, `Remote (UK)`, `Hybrid - Sydney`, `Sydney, NSW`. Keep the posting's wording; never turn "remote" into a city or invent a city for a remote role.
- **`industry`** - the employer's industry (`pharmaceuticals`, `higher education`, `medical communications`). `sector` remains the broad sector the dashboard charts; when both describe the same thing, write the same value rather than inventing a second taxonomy.

Write these when the row is created, and backfill an empty `country`, `location` or `industry` cell when the posting or its ATS URL plainly states the value. `job_id` is assigned at creation only - never backfilled onto a legacy row (see Step 4). Never overwrite a value already recorded, and never guess to fill a cell: empty is honest, with `job_id` the one exception, which is never empty on a new row.

---

## Step 2: Collect What Happened

Ask the user what happened, then classify:

**Progress updates** (application still open):
- Interview invitation / stage scheduled or completed (phone screen, technical, case, final round)
- Offer received (not yet accepted or declined)

**Resolutions** (application closed) - these map to the status enum in `documents/README.md` that `/setup` parses:
- `hired` - accepted an offer
- `offer_declined` - received an offer, turned it down
- `rejected` - explicit rejection at any stage
- `no_response` - no reply; if the user is unsure whether to call it, note how long it has been since the last contact and let them decide - do not impose a cutoff
- `interview_only` - reached interviews but the process stalled or was abandoned without an explicit rejection

Also collect, without interrogating - one or two open questions are enough:
- Dates for the stages reached
- Any feedback received, verbatim where the user remembers it
- What they'd do differently, and any signal about what the company valued (these feed `/setup`'s calibration and STAR-candidate mining, so concrete beats polished)

---

## Step 2b: Follow-Up Branch (chase a quiet application)

Enter this branch from the `followup` argument (Step 0) or from the offer under the open-pipeline table (Step 1.3). Standard practice is a brief, polite follow-up one to two weeks after applying, at most twice; this branch operationalizes that.

**Candidates.** An application qualifies when its status is not final, the threshold has passed since its `date` (or since the last `followed up` marker in `notes`, if any), and it has fewer than **two** logged follow-ups. Parse dates defensively - skip rows whose dates do not parse and say so rather than guessing. Present qualifying applications as a table (company, role, days quiet, follow-ups sent, channel, contact person) and draft only for the ones the user picks.

**Threshold.** The 10-day default is deliberately earlier than `/outlook-sync`'s 30-day staleness flag: that check is a read-only alarm that a row has been forgotten entirely; this branch is the proactive nudge while a reply is still plausible. The two numbers serve different moments, which is why they differ.

**Drafting.** For each selected application:

1. Read the archive folder: the `job_posting.md`, `cv_draft.tex`, and `cover_letter.tex` that Step 3 maintains are the source of **every claim** the note may make - this is Rule 3 (never fabricate) widened to "no new claims": a follow-up that introduces skills or experience the submitted materials don't contain is a fabrication vector.
2. Apply the writing style rules from `03-writing-style.md` (no cliches, no em-dashes, warm but direct), and match the application's language - draw the register from the archived cover letter.
3. Write roughly **60 to 120 words**: address the `contact_person` from the tracker if present (otherwise the team, in the application's language); one sentence restating interest in the specific role; one concrete value-reminder drawn from the submitted materials; one polite question about the timeline. No pressure, no "just checking in" filler.
4. Shape it for the `channel` column: email (with a subject line reusing the application's headline), LinkedIn message (shorter, no subject), or portal message (plain text).
5. Run `.claude/commands/_validate-application.md` before handing over the follow-up or a revised version. Include the submitted documents as read-only context. Present the checked draft for the user's review.

**Logging.** Once the user confirms they will send it (or have sent it), log it in the same turn - an unlogged follow-up breaks the next run's quiet-days math:

- Append `followed up YYYY-MM-DD` to the row's `notes` column (Step 4's rule applies: append a dated note, never restructure the CSV).
- Save the final note as `followup_YYYY-MM-DD.md` in the application's archive folder. Safe by documented convention: `/setup` reads only the four named archive files and ignores extras (the same rule that covers `/interview`'s prep files), and `documents/applications/**` is gitignored personal data.

If the user decides not to send, log nothing.

**Termination.** When an application hits two follow-ups and stays silent, do not offer a third. This is the moment to continue in this same command's Step 2: note how long it has been since last contact and let the user decide whether to record `no_response` - as ever, no imposed cutoff. And if the user mentions an actual response while in this branch (an interview invitation, a rejection), drop out of the branch and record it through the normal Step 2 flow.

---

## Step 3: Archive the Application Materials

Create or update `documents/applications/<company>_<role>_<job_id>/`. All content here is personal data - the folder is already gitignored (`documents/applications/**`), so nothing needs redacting.

1. Copy the exact submitted CV and letter identified by the tracker paths or the user, preserving the submitted source format and any supplied final PDFs. Use the archive names `cv_draft` and `cover_letter` with their actual extensions. If paths are absent, resolve the exact draft stem for this vacancy and verify the submitted version; ask if ownership or version is uncertain. Never pick a company-wide filename match. Preserve existing archived files.
2. **`job_posting.md`** - if it already exists, leave it. Otherwise try WebFetch on the tracker row's `source` URL and save the posting text. If the URL is dead (postings expire fast - this is exactly why the archive matters), ask the user to paste the posting, or write a stub noting the posting is unavailable. **Never reconstruct a posting from memory.**
3. **`outcome.md`** - write or update it in exactly the format documented in `documents/README.md`, so `/setup` Path A parses it without special cases:

```markdown
# Outcome: <Company> — <Role>

**Status:** in_progress | hired | offer_declined | rejected | no_response | interview_only

**Date resolved:** YYYY-MM-DD   <- only when resolved; omit while in_progress

## Interview stages reached
- [x] Phone screen (YYYY-MM-DD)
- [ ] Technical interview
- [ ] Case interview
- [ ] Final round
- [ ] Offer received

## Notes
<feedback received, what to do differently, signals about what they valued -
appended per update with a date, never overwritten>
```

Update rules: tick stage checkboxes as they are reached (add the date in parentheses), append dated entries to Notes, and only change `Status` from `in_progress` to a final value on resolution. Re-running `/outcome` on the same application is idempotent - it appends new information, never duplicates or rewrites history.

**Thank-you note trigger:** when this step ticks a newly completed interview stage, offer in the same turn: "Want a short thank-you note for the interviewer? A prompt one is standard practice." If accepted, draft it under Step 2b's drafting and logging rules (same voice, same no-new-claims boundary, same `followup_YYYY-MM-DD.md` archive convention). Recording the stage is the trigger - no scanning for recent stages is ever needed.

---

## Step 4: Update the Tracker

Update the matched row's `status` column (e.g. `applied` → `interview` → `offer` → `hired` / `rejected` / `no response` / `offer declined` / `withdrawn`) and append a short dated note to the `notes` column. Write `job_id`, `country`, `location` and `industry` when the row is created; backfill `country`, `location` and `industry` when a cell is still empty and the archived posting or its ATS URL plainly states the value. Do not backfill `job_id` onto a legacy row whose archive folder is still suffixless - the folder is never renamed to match. Never overwrite an existing value, never restructure the CSV, reorder rows, or touch other rows.

---

## Step 5: Calibration Handoff

Count the `outcome.md` files under `documents/applications/` with a **final** status (not `in_progress`).

- If 3 or more are resolved (or 2+ share a pattern - same role type rejected twice, same sector going silent), suggest:
  > "You now have <N> resolved applications on record. Run `/setup` (Path A) to fold them into your evaluation framework - it calibrates fit scoring from what actually got interviews, and mines your interview feedback for STAR examples."
- Do **not** write anything into `04-job-evaluation.md` or other skill files yourself. `/setup` Path A owns that merge - it is read-before-write and idempotent, and duplicating its logic here would race it.

---

## Step 6: Confirm

Summarize what was recorded:

> **Outcome recorded for <Role> at <Company>.**
>
> - `documents/applications/<company>_<role>_<job_id>/outcome.md` - status: <status>, job ID: <job_id>, <what changed>
> - Archived: <which of cv_draft.tex / cover_letter.tex / job_posting.md were copied or fetched, and which were skipped and why>
> - Tracker: status → <new status>
>
> [Calibration suggestion from Step 5, if triggered]

If the update recorded an upcoming or newly scheduled interview stage, also suggest:

> "Interview coming up? `/interview <company>` builds a prep pack for that stage from this application's archive - the posting, the documents you submitted, and any feedback recorded from earlier rounds."

If the recorded status is `hired`, congratulate the user warmly first - this is the moment the whole framework exists for. Then add this single line (once; never on re-runs for the same application, and never for any other status):

> "If this framework helped you get there, consider [buying it a coffee](https://ko-fi.com/madslorentzen) - it keeps this free for the next job-seeker out there. ☕"

---

## Important Rules

1. **Write data, don't interpret it.** The archive and tracker are the outputs; calibration belongs to `/setup`. This command never edits profile or framework files.
2. **The archived version is the submitted version.** Existing files in the application folder are never overwritten by fresher drafts.
3. **Never fabricate.** A dead posting URL gets a user-pasted copy or an explicit "unavailable" stub, not a reconstruction. Feedback is recorded as the user reports it.
4. **Stay schema-compatible.** `outcome.md` follows the format in `documents/README.md` exactly (`in_progress` is the one addition, for open applications); the tracker keeps its columns.
5. **Idempotent updates.** Re-running on the same application appends new stages and notes; it never duplicates folders, rows, or history.
6. **Follow-ups: draft only, never send.** The follow-up branch produces text for the user to send themselves. It never emails, messages, or submits anything, and it must not be wired to tools that do.
7. **Follow-ups: no new claims.** Every substantive statement in a follow-up or thank-you note comes from the archived submitted materials. Rule 3 applies with no exceptions.
8. **Maximum two follow-ups per application.** After the second silent follow-up, the honest move is recording the resolution, not persistence.
