
from flask import Flask, request, render_template, jsonify
import random
import datetime
import openai
import os

app = Flask(__name__)

# Azure OpenAI configuration
openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")  # e.g., https://your-resource-name.openai.azure.com/
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("AZURE_OPENAI_KEY")

# Simulated metrics and logic
def simulate_metrics():
    return {
        "cpu": random.randint(10, 95),
        "memory": random.randint(20, 95),
        "disk": random.randint(30, 98),
        "timestamp": datetime.datetime.now().isoformat()
    }

def check_for_incident(metrics):
    incidents = []
    if metrics['cpu'] > 85:
        incidents.append("High CPU usage")
    if metrics['memory'] > 90:
        incidents.append("Memory usage critical")
    if metrics['disk'] > 90:
        incidents.append("Disk space low")
    return incidents

def auto_remediate(incidents):
    actions = []
    for incident in incidents:
        if "CPU" in incident:
            actions.append("Scaled up additional compute instances")
        elif "Memory" in incident:
            actions.append("Restarted memory-intensive services")
        elif "Disk" in incident:
            actions.append("Cleared temp/log files")
    return actions

def generate_chat_response(message):
    prompt = f"You are an AI Ops assistant. Respond to: '{message}'"
    response = openai.ChatCompletion.create(
        engine="gpt-4",  # Replace with your Azure deployment name
        messages=[
            {"role": "system", "content": "You monitor and manage production infrastructure with AI."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content']

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    metrics = simulate_metrics()
    incidents = check_for_incident(metrics)
    actions = auto_remediate(incidents)
    response = ""
    user_message = ""

    if request.method == 'POST':
        user_message = request.form.get('message')
        response = generate_chat_response(user_message)

    return render_template('dashboard.html', metrics=metrics, incidents=incidents, actions=actions, ai_response=response, user_message=user_message)

if __name__ == '__main__':
    app.run(debug=True)
