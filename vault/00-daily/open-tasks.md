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
```dataviewjs
const folders = ["00-daily", "90-meeting-notes"];
const items = [];
for (const folder of folders) {
  for (const page of dv.pages(`"${folder}"`)) {
    for (const item of page.file.lists.values) {
      if (item.text && item.text.includes("#tracking") && !item.task) {
        const link = `[[${page.file.path}|${page.file.name}]]`;
        items.push({ text: item.text.replace(/#tracking/g, "").trim(), source: link, path: page.file.path });
      }
    }
  }
}
items.sort((a, b) => b.path.localeCompare(a.path));
if (items.length === 0) {
  dv.paragraph("*Nothing tracked right now.*");
} else {
  for (const item of items) {
    dv.el("div", `• ${item.text} — ${item.source}`, { cls: "tracking-item" });
  }
}
```
