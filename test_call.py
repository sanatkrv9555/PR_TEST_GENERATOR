import requests

url = "http://127.0.0.1:8000/generate-tests"

payload = {
    "diff": "diff --git a/app.py b/app.py\n+def add(a, b):\n+    return a + b\n",
    "language": "python",
    "framework": "pytest"
}

try:
    resp = requests.post(url, json=payload)
    print("Status:", resp.status_code)

    if resp.status_code == 200:
        data = resp.json()
        print("\n📌 AI Test Suggestions (Markdown):\n")
        print(data["suggestions_markdown"])
    else:
        # If it's not 200, print full error
        print("\n❌ Error Response Text:")
        print(resp.text)

except Exception as e:
    print(f"\n🔥 Request failed: {repr(e)}")
