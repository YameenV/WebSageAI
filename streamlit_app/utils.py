import requests

def send_query(prompt):
    try:
        response = requests.post("http://localhost:5000/query", json={"query": prompt})
        
        if response.status_code == 200:
            data = response.json()
            assistant_response = data.get("response", "")
            sources = data.get("sources", [])
            return assistant_response, sources
        else:
            return None, None

    except requests.exceptions.RequestException as e:
        return None, None
