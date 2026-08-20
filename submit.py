import json
import urllib.request
import urllib.error

def submit():
    # Fetch data from the local container endpoint
    print("Fetching local generation metrics...")
    local_req = urllib.request.Request("http://localhost:8000/generate")
    try:
        with urllib.request.urlopen(local_req) as response:
            local_data = json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        print(f"Error connecting to local server: {e}")
        print("Make sure your docker container is running on port 8000.")
        return

    # Build the exact payload required by the board
    payload = {
        "team": "15",
        "by": "Abdullah Almithn", 
        "model": local_data["model"],
        "image": "ghcr.io/thamercoe/aidc-15-w1d5:latest",
        "tokens_per_sec": local_data["tokens_per_sec"],
        "sample": local_data["sample"]
    }
    
    data = json.dumps(payload).encode("utf-8")

    # POST to the submission board with a custom User-Agent
    url = "https://aidc.nadir.sh/model"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AIDC-Submission-Script"
    }
    
    board_req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    print(f"Submitting payload to {url}...")
    try:
        with urllib.request.urlopen(board_req) as response:
            print(f"Success! Status Code: {response.status}")
            print(f"Response: {response.read().decode('utf-8')}")
    except urllib.error.URLError as e:
        print(f"Failed to submit to board: {e}")
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))

if __name__ == "__main__":
    submit()
