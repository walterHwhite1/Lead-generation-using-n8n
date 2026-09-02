import csv
import json
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here"))

ICP_WEIGHTS = {
    "recently_funded": 25,
    "hiring_ai_roles": 25,
    "company_size_fit": 20,
    "industry_match": 20,
    "seniority_match": 10,
}

def score_lead(lead):
    score = 0
    if lead.get("recently_funded", "").lower() == "yes":
        score += ICP_WEIGHTS["recently_funded"]
    if lead.get("hiring_ai_roles", "").lower() == "yes":
        score += ICP_WEIGHTS["hiring_ai_roles"]
    if lead.get("company_size", "") in ["11-50", "51-200"]:
        score += ICP_WEIGHTS["company_size_fit"]
    if lead.get("industry", "").lower() in ["saas", "ai", "fintech"]:
        score += ICP_WEIGHTS["industry_match"]
    if lead.get("seniority", "").lower() in ["founder", "vp", "director", "head"]:
        score += ICP_WEIGHTS["seniority_match"]
    return score

def generate_outreach(lead, score):
    prompt = f"""Write a short, personalized cold outreach email (under 80 words) to this lead.
Name: {lead.get('name')}
Role: {lead.get('role')}
Company: {lead.get('company')}
Industry: {lead.get('industry')}
ICP fit score: {score}/100

Tone: direct, not salesy. Reference something specific about their role or company.
Output only the email body, no subject line."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()

def process_leads(input_csv, output_json, score_threshold=50):
    results = []
    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        for lead in reader:
            score = score_lead(lead)
            entry = {
                "name": lead.get("name"),
                "company": lead.get("company"),
                "score": score,
                "qualified": score >= score_threshold,
            }
            if entry["qualified"]:
                entry["outreach_email"] = generate_outreach(lead, score)
            results.append(entry)

    results.sort(key=lambda x: x["score"], reverse=True)
    with open(output_json, "w") as f:
        json.dump(results, f, indent=2)
    return results

if __name__ == "__main__":
    process_leads("sample_leads.csv", "scored_leads.json")
    print("Done. See scored_leads.json")
