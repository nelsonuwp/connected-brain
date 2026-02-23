---
type: thinking
created: 2026-02-23
status: raw
promoted-from: 01-inbox
---

# Untitled

## The Raw Idea
I need to get the service guides in a place that I can use them to drive my LLMs.
Markdown files
Enough IO and interconnects that we can build out a scaffolding.

then get them to the team to review

Right now we have owners as:
Hybrid Service Delivery Management - [[Lacie-Ellen Morley]]
Hybrid Solution Architecture - [[Pat Wolthausen]]
Data Center Operations - [[George Revie]]
Hosting - [[Martin Tessier]]
Network - [[Ben Kennedy]]
Service Desk (L2/L3/NOC) - [[Jason Auer]]
Managed Cloud - [[Andrei Ianouchkevitch]]
Data - [[Jorge Quintero]]

**1. The Actual Problem** You are framing this as a data formatting and technical ingestion problem (converting service guides to Markdown for an LLM). The actual problem is an enterprise architecture and organizational alignment challenge. You are trying to force fragmented, siloed operational functions into a unified, machine-readable ontology to standardize and package your operations for a major organizational milestone next year.

**2. Key Assumptions Baked Into Your Thinking**
- **The documentation is ready for translation:** You are assuming the current service guides actually reflect reality. However, your existing documentation shows inconsistencies—for example, the Network SDET lists Peter Saito as the Service Manager, but your current thought lists Ben Kennedy. The Security, Compliance and Abuse SDET lists Martin Tessier, but you list him under "Hosting".    
- **Markdown is the right connective tissue:** You assume Markdown files can sufficiently capture the complex "IO and interconnects" (dependencies like Data Center relying on Network and Infrastructure ) without a strict underlying graph or relational database model.    
- **Review equals alignment:** You assume that handing this scaffolding to the service owners for "review" will result in a sign-off. In reality, defining inputs and outputs forces turf wars over operational boundaries, SLAs, and handoffs.   
- **The LLM knows what to do with "interconnects":** You assume an LLM can natively parse human-written process handoffs as strict systemic dependencies just because they are in the same directory.    

**3. Most Important Unknowns**
- **The LLM's primary mandate:** What exactly is the LLM supposed to execute once it has this context? (e.g., auto-generating SoWs, identifying operational bottlenecks, routing L2/L3 tickets, or answering customer queries). The format of the "IO" depends entirely on what the machine needs to output.    
- **Definition of "IO and interconnects":** It is unclear if you are mapping technical data flows, human ticket escalation paths, or financial dependencies between these service silos.    
- **Authority to standardize:** If Jason Auer (Service Desk) and Andrei Ianouchkevitch (Managed Cloud) disagree on the handoff mapped in your scaffolding, it is unknown who has the final authority to dictate the operational boundary.    
- **Current vs. Future State:** It is unclear if you are trying to document the messy reality of what currently exists (including archived services ), or the clean, ideal state you need the business to operate under.    

**4. Sharp Questions to Force Clearer Thinking**
- What specific operational outcome fails if the LLM cannot understand the "interconnects" between Hybrid Service Delivery and Data Center Operations?    
- Your current documentation has conflicting owner names and overlapping dependencies. Are you digitizing the reality of your operations as they exist today, or the streamlined version you need to present to the market next year?    
- When the service owners review this and inevitably disagree on where one service ends and another begins, what is the mechanism to force a decision rather than endless revisions?    
- Why use an LLM for this mapping instead of a standard CMDB or enterprise architecture platform that natively handles relational mapping?    

**5. The Framing Issue** You are treating an operational standardization problem as an IT formatting task. Converting bad or misaligned organizational logic into Markdown will just yield a machine-readable mess. The bottleneck isn't the file format; it's defining the strict operational boundaries and forcing the business leaders to adhere to them.


## Why This Matters
<!-- Why are you thinking about this? What triggered it? -->
<!-- CEO asked / customer complained / you noticed a pattern / etc. -->
This matters because there is no source of truth for the services in a "machine readable" format that I can pass as context to help me craft decisions using tools like LLMs


## What I Think I Want
<!-- Best guess at the outcome. It's ok to be wrong here. -->
I _think_ I want the following:
* The Service Guide Template filled out for the services in the delivery service network side:
	- Hybrid Service Delivery Management
	- Hybrid Solution Architecture
	- Data Center Operations
	- Hosting
	- Network
	- Service Desk (L2/L3/NOC)
	- Managed Cloud
	- Data
* All files in Markdown files and living in vault/50-services
* How the services fit together and flow vioa 
* A list of products and services that each team is responsible/accountable for

## What I Don't Know Yet
<!-- The honest list of unknowns. These become the Think mode questions. -->
- We dont have a 100% agreed upon products and services yet
- 
- 

## What I'm Conflating
<!-- Are there two separate things tangled together here? -->
<!-- Common: "build a thing" mixed with "decide if we should build a thing" -->


## Who Else Is Involved
<!-- People, teams, systems that touch this -->


## Ready to Promote?
<!-- A thinking note is ready for 30-initiatives when you can answer YES to all three: -->
- [ ] I know who owns this
- [ ] I can describe a measurable outcome
- [ ] I have a rough timeline

---
## Think Mode Output
<!-- Paste LLM think-mode response here after running it -->


## My Answers
<!-- Answer the questions the LLM raised before promoting to initiative -->

