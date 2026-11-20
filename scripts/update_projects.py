#!/usr/bin/env python3
"""
Update latest repositories list in GitHub Profile README for Mukilan-s18.
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

START_MARKER = "<!-- PROJECTS:START -->"
END_MARKER = "<!-- PROJECTS:END -->"

REPO_REGISTRY = {
    "Industrial-Operations-Brain": {
        "description": "Agentic AI system for industrial knowledge intelligence - RAG + Knowledge Graph + Live IoT fusion with LangGraph, Gemini, and Next.js.",
        "language": "Python, TypeScript",
    },
    "TierGuard-Entitlements-Engine": {
        "description": "Ultra low latency SaaS entitlements and usage metering engine built with Go, Redis, and HTMX.",
        "language": "Go, HTML",
    },
    "UC-04-Configuration-comparison-SaaS": {
        "description": "Configuration Comparison SaaS (ConfigGuard) with Azure Container Apps, atomic locking, and A01-A12 compliance.",
        "language": "HTML, Python, Go",
    },
    "Deep-Learning": {
        "description": "Deep Learning Laboratory experiments & Mini Project in PyTorch 2.x, accelerated on Apple Silicon MPS (GPU) with NASA telemetry.",
        "language": "Python, PyTorch",
    },
    "Build-and-Deploy-Machine-Learning": {
        "description": "Comprehensive machine learning experiments covering data preprocessing, supervised learning, deep learning, and REST API deployment.",
        "language": "Python, Jupyter",
    },
    "StampedeZero": {
        "description": "Real-time edge AI crowd safety platform with YOLOv8 for density estimation and early stampede detection.",
        "language": "Python, React",
    },
    "CompileAI": {
        "description": "7-stage AI pipeline converting natural language requirements into validated, executable application specifications.",
        "language": "Python, FastAPI",
    },
    "FIFA-2026-WINNER-PREDICTION-MODEL": {
        "description": "Predictive ML pipeline and React web app running 10,000 Monte Carlo simulations for 2026 FIFA World Cup.",
        "language": "Python, React",
    },
    "PumpDiagnosisChallenge": {
        "description": "Industrial pump fault diagnosis system on MANGO Platform using Computer Vision & Transfer Learning (ResNet18) on STFT spectrograms.",
        "language": "Python, PyTorch",
    },
    "Defect-Detection": {
        "description": "State-of-the-art anomaly detection system for industrial manufacturing using PatchCore and WideResNet50.",
        "language": "Python, PyTorch",
    },
    "weather-app": {
        "description": "High-performance AeroWeather dashboard built with React 19 + Vite, integrating live atmospheric analytics and radar.",
        "language": "React, Vite",
    },
    "Ecosphere-Management-Platform": {
        "description": "ESG monitoring and sustainability platform with gamification engine, built on Next.js and Supabase.",
        "language": "TypeScript, Next.js",
    },
    "mnist-ann-classifier": {
        "description": "MNIST digit classifier using fully connected ANN with MLOps pipeline, MLflow tracking, and Gradio browser demo.",
        "language": "Python, Gradio",
    },
    "Mukil-portfolio": {
        "description": "Modern personal portfolio showcasing AI/ML and full-stack software engineering projects.",
        "language": "TypeScript, Next.js",
    },
    "Low-Code-Zoho-Creator": {
        "description": "Comprehensive Zoho Creator Low-Code Application Development Laboratory records and End Semester Mini Project Report.",
        "language": "Deluge",
    },
    "FDVA": {
        "description": "Foundations of Data Visualization and Analysis with exploratory data analysis, cleaning, and visual dashboards.",
        "language": "Python",
    },
    "Computer-Networks-Lab": {
        "description": "Network socket programming, routing protocol simulation, and packet analysis experiments.",
        "language": "Python, C",
    },
    "GraphOne-ai-data-intelligence-pipeline": {
        "description": "High-performance async crawler, LLM structuring, and entity resolution for AI startups and research papers.",
        "language": "Python, FastAPI",
    },
    "POAI-RECORD": {
        "description": "Fundamental Artificial Intelligence algorithms (Search, Logic, Minimax) implemented in Python and Prolog.",
        "language": "Python, Prolog",
    },
    "JAVA-RECORD": {
        "description": "Object-Oriented Programming (OOP) using Java laboratory records, modern collections, and JDBC applications.",
        "language": "Java",
    },
    "DAA-RECORD": {
        "description": "Design and Analysis of Algorithms laboratory experiments, asymptotic analysis, divide and conquer, dynamic programming in C.",
        "language": "C",
    },
    "DBMS-Experiments": {
        "description": "Database Management System lab experiments with Oracle SQL queries, PL/SQL procedures, and triggers.",
        "language": "SQL, PL/SQL",
    },
    "Operating-Systems": {
        "description": "Core OS laboratory implementations covering process scheduling, IPC, and memory management in C.",
        "language": "C, Shell",
    },
    "C-Programming-Lab-record": {
        "description": "Comprehensive C Programming Laboratory records spanning 16 weeks of experiments.",
        "language": "C",
    },
}

def fetch_repositories(username, token=None):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    headers = {"User-Agent": "Mozilla/5.0"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

def generate_markdown(repos, username):
    lines = [
        START_MARKER,
        "| Repository | Description | Primary Language |",
        "| :--- | :--- | :--- |",
    ]
    for r in repos:
        name = r["name"]
        url = r.get("html_url", f"https://github.com/{username}/{name}")
        meta = REPO_REGISTRY.get(name, {})
        desc = meta.get("description") or r.get("description") or "Engineering repository."
        lang = meta.get("language") or r.get("language") or "Code"
        lines.append(f"| [**{name}**]({url}) | {desc} | `{lang}` |")
    lines.append(END_MARKER)
    return "\n".join(lines)

def update_readme(readme_path, new_section):
    content = readme_path.read_text(encoding="utf-8")
    if START_MARKER in content and END_MARKER in content:
        pattern = re.compile(rf"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL)
        content = pattern.sub(new_section, content)
    else:
        target = "## 🎖️ Achievements & Certifications"
        if target in content:
            content = content.replace(target, f"## 📂 All Repositories\n\n{new_section}\n\n---\n\n{target}")
        else:
            content += f"\n\n## 📂 All Repositories\n\n{new_section}\n"
    readme_path.write_text(content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="Mukilan-s18")
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    parser.add_argument("--limit", type=int, default=18)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    try:
        raw_repos = fetch_repositories(args.username, token)
        filtered = [
            r for r in raw_repos
            if not r.get("fork") and not r.get("archived") and r.get("name") != args.username
        ][:args.limit]
    except Exception as e:
        print(f"API fetch error: {e}, falling back to registry")
        filtered = [
            {"name": name, "html_url": f"https://github.com/{args.username}/{name}"}
            for name in list(REPO_REGISTRY.keys())[:args.limit]
        ]

    section = generate_markdown(filtered, args.username)
    update_readme(args.readme, section)
    print("Updated All Repositories section successfully!")

if __name__ == '__main__':
    main()
