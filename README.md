# Lead-generation-using-n8n
AI-Powered Lead Scoring &amp; Outreach Tool  A lightweight GTM automation tool that scores inbound/outbound leads against an ICP rubric and auto-generates personalized outreach copy for qualified leads using Claude.
Architecture

Core scoring + generation logic — lead_scorer.py

Reads leads from a CSV (or in production, a CRM export / Sheet)
Scores each lead 0-100 against 5 weighted ICP signals (funding status, hiring signals, company size, industry, seniority)
For leads above the qualification threshold, calls the Claude API to generate a short, personalized outreach email
Outputs a ranked JSON file, ready to push into an outreach tool or CRM
n8n Workflow Wrapper

The Python script is wrapped in an n8n workflow so non-technical teammates (or the founders) can trigger it without touching code:

Trigger node — Google Sheets "row added" trigger (new lead comes in from a form, scraper, or manual entry) OR a scheduled Cron trigger to batch-process a lead list daily
Execute Command / HTTP Request node — calls lead_scorer.py (or a small Flask endpoint wrapping it) with the new lead's data
IF node — branches on qualified: true/false
Qualified branch — writes the scored lead + generated email into a "Ready to Send" Google Sheet / Airtable, and optionally posts a Slack notification to the GTM channel
Not-qualified branch — logs to a "Low Priority" sheet for later review

This mirrors the JD's ask directly: "Build tools, workflows and automations that make user acquisition, outreach... more efficient" and "Use APIs, LLMs, AI coding tools and automation platforms to turn GTM processes into scalable systems."

Why this design
Scoring logic is deterministic and cheap (no LLM call needed) — only qualified leads get an LLM call, keeping cost proportional to actual opportunity, not raw volume
Outreach generation is where the LLM adds real leverage — personalized copy at speed, instead of manually writing each email
n8n wrapper makes it usable by non-engineers, matching how a 2-person GTM+eng pod would actually operate at an early-stage startup
