---
type: thinking
created: 2026-02-22
status: raw
promoted-from: 01-inbox
---

# LLM Bridge

## The Raw Idea
I need a way to use a python script to send my "thoughts" and "ideas" from Obsidian to LLMs and get a response so I don't have to copy and paste into disparate tools.  


## Why This Matters
Tired of copy-pasting vault notes into browser LLM tabs.
Context gets lost between sessions. Want one terminal command
that reads a note, calls OpenRouter, writes output back.


## What I Think I Want
Python script: reads vault note + prompt template from _prompts/,
calls OpenRouter, appends output back into the note with a timestamp.


## What I Don't Know Yet
- Output back into same note, or a new file?
- Does failure mean partial write or nothing written?
- Is the LLM transport (API calls) the same file as vault I/O?
- Does it need to handle RunArtifact data or just notes?

## What I'm Conflating
"The thing that calls OpenRouter" and "the thing that reads/writes 
vault files" are probably two separate files — but I'm thinking 
about them as one script.


## Who Else Is Involved
Just me building it. Will hand off pattern to jr dev later.


## Ready to Promote?
- [x] I know who owns this ✅ 2026-02-22
- [x] I can describe a measurable outcome ✅ 2026-02-22
- [x] I have a rough timeline ✅ 2026-02-22

---
## Think Mode Output
## What You're Actually Trying to Solve

Not a scripting problem. A **workflow friction problem** — specifically, context loss and tool-switching cost when working with LLMs. The script is one possible solution, not the problem itself. Worth holding that distinction.

---

## Assumptions Baked In

**"One terminal command"** assumes CLI is the right interface. You haven't established why not a hotkey, an Obsidian plugin, or a shell alias wrapping an existing tool. Terminal-first may be a preference dressed up as a requirement.

**"Reads vault note + prompt template"** assumes the note _is_ the full context. But you mentioned context gets lost between sessions — a single note read doesn't solve session continuity unless you're also including prior outputs. Are you?

**"Appends output back into the note"** assumes the note is the canonical record. That's a meaningful architectural choice with consequences (note bloat, non-reversibility, breaking Obsidian's graph if structure changes) that you haven't examined.

**"Hand off to jr dev later"** is doing a lot of hidden work. It implies the code needs to be readable, documented, and structured — which changes scope significantly from a personal scratch script.

---

## Most Important Unknowns

**What counts as "context"?** If it's just the current note, you haven't solved the session memory problem you named. If it's the note + linked notes + prior outputs, scope just tripled.

**What's the failure contract?** You listed this yourself but didn't answer it. Partial writes to a vault note can corrupt Obsidian metadata or break frontmatter. This isn't optional to decide — it determines whether you need a temp file + atomic swap pattern or not.

**Is OpenRouter the right abstraction?** You named it specifically. Is that locked in, or is "any LLM API" the real requirement? This changes whether you build a thin wrapper or a provider-agnostic layer.

---

## The Framing Issue

You're treating this as a **build problem** when it might be a **tool selection problem**. Tools like `fabric`, `sgpt`, or `aichat` already do "read stdin/file → call LLM → write output" with OpenRouter support. You may be about to build something that exists. The question you haven't asked: _what does this need to do that existing CLI LLM tools don't?_

If the answer is "Obsidian-specific file I/O and prompt template management," that's a real differentiator. If the answer is "I didn't know those tools exist," that's a different conversation.

---

## Sharp Questions

1. **What does "context gets lost" actually mean?** Are you losing the _note content_, the _conversation history_, or your own _mental state_ about where you left off? Each has a different fix.
    
2. **What happens to the note after the LLM responds?** Do you read it again? Edit it? Feed it back in? If the output just sits there, you haven't solved continuity — you've just moved the copy-paste problem one step left.
    
3. **Why a Python script and not an Obsidian plugin?** A plugin would have direct vault API access, could trigger from a hotkey, and wouldn't require a terminal context switch. What's driving the CLI assumption?
    
4. **Who is the "jr dev handoff" actually for?** If it's for them to _use_ it, that's a UX problem. If it's for them to _extend_ it, that's an architecture problem. These produce very different designs.
    
5. **What's the smallest version of this that would tell you if the approach is right?** You're designing a system. Have you run a single `curl` to OpenRouter piped from a vault note yet? If not, you're specifying before validating.


## My Answers
1. Regarding context. I want to send the "thinking" content and then any context files that accompany them. So for example, if I want to write my problem statement about accessing data ... and then send my database schema along as "context".
2. Well I would LOVE it if it would _automatically_ put it in this file.
3. I can't imagine that an obsidian plugin can do it... but also I run the other half of my life out of cursor, so I'll have access to the raw MD files and a terminal. Python is most likely easier to code than an obsidian plugin.
4. It's me, passing it to cursor... Composer 1.5 most likely or some other coding-specific LLLM.
5. python 

