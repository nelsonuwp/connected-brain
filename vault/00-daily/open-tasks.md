# Open Tasks

## My Actions
```tasks
not done
description includes #action
path includes 00-daily
sort by path reverse
```

```tasks
not done
description includes #action
path includes 90-meeting-notes
sort by path reverse
```

## Waiting On Others
*Pulls open #tracking items from daily digest, meeting notes, and 1:1s. Grouped by person where attributed.*

```dataviewjs
const sources = ["00-daily", "90-meeting-notes", "40-people"];
const allPages = dv.pages('"00-daily" OR "90-meeting-notes" OR "40-people"');

const byPerson = {};
const unattributed = [];

for (const page of allPages) {
  // Task-style tracking items (checkboxes): - [ ] text #tracking [person::slug]
  for (const task of page.file.tasks) {
    if (task.completed) continue;
    const tags = task.tags || [];
    if (!tags.includes("#tracking")) continue;

    const person = task.person || null;
    const entry = {
      text: task.text.replace(/#tracking/g, "").replace(/\[person::[^\]]+\]/g, "").trim(),
      source: `[[${page.file.path}|${page.file.name}]]`,
      path: page.file.path,
    };

    if (person) {
      if (!byPerson[person]) byPerson[person] = [];
      byPerson[person].push(entry);
    } else {
      unattributed.push(entry);
    }
  }

  // Legacy non-task tracking items (plain list items): - text #tracking
  for (const item of page.file.lists.values) {
    if (item.task) continue; // already handled above
    if (!item.text || !item.text.includes("#tracking")) continue;

    const entry = {
      text: item.text.replace(/#tracking/g, "").trim(),
      source: `[[${page.file.path}|${page.file.name}]]`,
      path: page.file.path,
    };
    unattributed.push(entry);
  }
}

// Sort entries within each group by path descending (most recent first)
const sortByPath = (a, b) => b.path.localeCompare(a.path);

// Render attributed groups
const allSlugs = Object.keys(byPerson).sort();
if (allSlugs.length > 0) {
  for (const slug of allSlugs) {
    const displayName = slug.split("-").map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");
    const personLink = `[[40-people/${slug}/${slug}|${displayName}]]`;
    dv.header(4, personLink);
    const items = byPerson[slug].sort(sortByPath);
    for (const item of items) {
      dv.el("div", `• ${item.text} — ${item.source}`, { cls: "tracking-item" });
    }
  }
}

// Render unattributed
if (unattributed.length > 0) {
  dv.header(4, "Unattributed");
  for (const item of unattributed.sort(sortByPath)) {
    dv.el("div", `• ${item.text} — ${item.source}`, { cls: "tracking-item" });
  }
}

if (allSlugs.length === 0 && unattributed.length === 0) {
  dv.paragraph("*Nothing tracked right now.*");
}
```
