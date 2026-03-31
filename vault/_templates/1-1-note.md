<%*
// ── 1-1 Note: person picker + file routing ────────────────────────────────────
const peopleRoot = "40-people";

// Get all direct children of 40-people that are folders
// (checking .children is reliable; TFolder has it, TFile does not)
const rootFolder = app.vault.getAbstractFileByPath(peopleRoot);
if (!rootFolder) {
  new Notice("Could not find 40-people folder.");
  return;
}

const personFolders = rootFolder.children
  .filter(f => f.children !== undefined)   // TFolder check (works in minified builds)
  .map(f => f.name)
  .sort();

if (personFolders.length === 0) {
  new Notice("No person folders found in 40-people.");
  return;
}

// Display names from slugs: "jorge-quintero" → "Jorge Quintero"
const displayNames = personFolders.map(slug =>
  slug.split("-").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ")
);

// Suggester: show display names, return slug
const selectedSlug = await tp.system.suggester(displayNames, personFolders);
if (!selectedSlug) return; // user cancelled

const personDisplay = displayNames[personFolders.indexOf(selectedSlug)];

// Build target path
const today = tp.date.now("YYYY-MM-DD");
const year  = tp.date.now("YYYY");
const month = tp.date.now("MM-MMM");   // e.g. "03-Mar"
const filename = `${today}-${selectedSlug}-1-1`;
const targetFolder = `${peopleRoot}/${selectedSlug}/1-1s/${year}/${month}`;

// Create the folder if it doesn't exist
try { await app.vault.createFolder(targetFolder); } catch(e) { /* already exists */ }

// Move this note into the right place
await tp.file.move(`${targetFolder}/${filename}`);
-%>
---
type: 1-1
date: <% tp.date.now("YYYY-MM-DD") %>
person: <% selectedSlug %>
---

# 1:1 — <% personDisplay %> — <% tp.date.now("YYYY-MM-DD") %>

---

## Carry-forward
*Open tracking items for <% personDisplay %> — updates live as items are completed*

```dataview
TASK FROM "40-people/<% selectedSlug %>/1-1s" OR "00-daily" OR "90-meeting-notes"
WHERE !completed AND contains(tags, "#tracking")
  AND (person = "<% selectedSlug %>" OR contains(file.path, "40-people/<% selectedSlug %>/1-1s"))
SORT file.mtime DESC
```

---

## Their agenda
<!-- What they want to cover — capture before or at start of meeting -->

## My agenda
<!-- Coaching focus, delegation check, capability push for this session -->

---

## Discussion Notes
<!-- Raw capture — don't over-format in real time, just get it down -->

---

## Decisions & Actions

| Action | Owner | By When |
|--------|-------|---------|
| | | |

<!-- Inline tracking tasks — tag with #tracking so they surface on the hub -->
<!-- Example: - [ ] Jorge to update BI report filter by Friday #tracking [person::<% selectedSlug %>] -->

---

## Capability Observation
<!-- One line: what did this meeting show about their growth or gaps? Be specific. -->

## Next session focus
<!-- One sentence on what to prioritize next time -->
