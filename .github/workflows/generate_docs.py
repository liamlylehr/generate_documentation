import os
import requests
from openai import OpenAI

# Load environment variables
github_token = os.getenv("GITHUB_TOKEN")
repo = os.getenv("REPO")
pr_number = os.getenv("PR_NUMBER")
openai_api_key=os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)


# Read the diff
with open("pr_diff.txt", "r") as f:
    diff = f.read()

# Prompt for docs
prompt = f"""
You are a documentation assistant. Generate clear, concise documentation
in Markdown for the following code changes (diff):

{diff}
"""

# Call OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.2,
)

docs = resp.choices[0].message.content

# Post comment on PR
url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
headers = {"Authorization": f"token {github_token}"}
requests.post(url, json={"body": f"📝 Suggested Documentation:\n\n{docs}"}, headers=headers)
