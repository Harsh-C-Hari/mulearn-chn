# Team audit (Phase 6.1)

Sources: `PROJECT_MASTER_SPEC.md` §7.7, client filenames in `sources/mulearn/Team/`, Phase 6 brief §4. Data: `data/team.js`.

## Roster reconciliation
21 unique members, names and recorded roles identical to the Phase 6 brief table (test: `scripts/test_phase6.py`). No names from older summaries (Abhiram V, Aswin Sreekumar). Four featured (page order): Nithin Jayakumar (Campus Lead), Amanul Farhan (Technical Lead), Govind J S (Creative Lead), Hanin C K (Operational Lead).

## Defect found and fixed
The previous `data/team.js` pointed at two files that do not exist (`karthika-s-native.webp`, `abhiram-j-native.webp`). Real files are `karthika-s-600.webp` and `abhiram-j-600.webp`. All 42 referenced portrait files now exist and the recorded pixel sizes match the files (no upscaling; Geetha S is 377×452 native).

## Role decisions (not silently resolved)
| Member | Recorded role | Public display | Why |
|---|---|---|---|
| Geetha S | Lead Enabler | name only | Meaning unknown (not in the µLearn chapter model); not to be shown as Faculty |
| Divyalakshmi | Campus Co-Lead | name only | Brief flags it unconfirmed; spelling Co-Lead vs Co Lead open |
| Swathy J | IG Lead – Entrepreneurship | name only | "Entrepreneurship" is not an official µLearn Interest Group on mulearn.org (checked 2026-11-20) |
| Hanin C K | Operational Lead | "Operational Lead" | Brief and client filename agree; prototype said "Operations Lead": wording only, recorded |
Held titles stay in the data (`role`, `roleNote`, `roleStatus:"unconfirmed"`); showing one later = set `roleStatus` to `recorded` and `roleLabel` to the text. "IG" is expanded to "Interest Group" in labels. No hierarchy implied.

## Photo pairing
Pairing of face to name rests only on the client's filenames (`<n>_<Name>__<Role>.jpg`). It cannot be checked by comparing faces and was not. The four featured pairings follow the Spec §7.7 mapping (#2, #6, #4, #5). Kill-switch: `photoShown:false` per member renders a neutral monogram instead of the portrait. **Open item for the client: confirm that each file shows the person named in its filename.**

## Structure decisions
`#team` section after Events (stub removed, Memories stub kept). Featured four are also listed in the full roster ("All 21 members"), so the count stays 21. One list in roster order: the spec's group labels (Leadership / Leads / Teams) would imply a hierarchy, so they are not used.

## Side fix (Phase 5 file)
`css/sections/events.css`: compact thumbnails (≥700px) grew by ~115px after lazy images loaded, which moved every section below Events and made the Team nav link land ~115px low. Added `min-height:0; overflow:hidden` to `.event-mini__thumb`. Measured shift is now 0 at 390/768/1024/1440.
