# 🏦 Enterprise Risk & Adverse Media Copilot

**An Explainable AI-Assisted Compliance & Entity Resolution Engine**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Enterprise-FF4B4B.svg)
![Groq](https://img.shields.io/badge/Groq-LPU_Inference-f55036.svg)
![Compliance](https://img.shields.io/badge/KYC%2FAML-Automation-success.svg)

---

## 🚨 The Problem Statement
In modern financial institutions, **Anti-Money Laundering (AML)** and **Know Your Customer (KYC)** compliance teams spend up to 80% of their time manually reading unstructured web searches and news articles to screen for "Adverse Media" (negative news regarding fraud, sanctions, or corruption). 

This manual process suffers from three critical flaws:
1. **High False Positive Rates:** Analysts waste time reading articles about people with the same name as the target entity (Entity Resolution failures).
2. **Lack of Standardized Scoring:** Human analysts assign risk subjectively, leading to inconsistent audit trails.
3. **Information Overload:** The sheer volume of global news makes it impossible to scale manual screening without massive operational costs.

## 💡 The Solution (High-Level Analysis)
The **Adverse Media Copilot** is a tier-1 compliance workflow automation tool. It replaces subjective human reading with deterministic AI extraction. By leveraging hyper-fast LPU inference via **Groq** and the advanced reasoning capabilities of **Llama 3.3 70B**, the system dynamically queries global media, resolves entity identity, and extracts structured risk vectors. 

Instead of relying on an LLM to "guess" a risk score, our Copilot uses a **Mathematical Risk Engine** to calculate an explainable, auditable risk score based on the raw facts extracted by the AI.

---

## 🏗️ System Architecture & In-Detail Workflow

The application operates on a 4-stage pipeline:

### 1. Dynamic Data Ingestion (OSINT)
The system takes a target entity and jurisdiction, compiling a targeted boolean search query. It connects to live Search APIs (DuckDuckGo/Bing) to scrape unstructured text snippets from global news outlets, legal databases, and financial blogs. *(Note: Includes a robust failover architecture with injected mock data for uninterrupted hackathon demos).*

### 2. LLM Entity Resolution & Vector Extraction
The unstructured text is injected into Groq's API. We utilize strict **JSON Mode** and Prompt Engineering to force the model into the role of a Risk Intelligence Analyst. The LLM extracts four key vectors:
* **Match Confidence:** Percentage certainty that the news article is talking about *our* target, not a namesake.
* **Taxonomy Severity:** The classification of the crime (e.g., Sanctions violations = 10, Localized lawsuits = 4).
* **Temporal Recency:** How active the threat is (e.g., arrested yesterday vs. bankrupt 20 years ago).
* **Source Density:** The number of unique outlets reporting the event.

### 3. Mathematical Weighting Engine
To guarantee regulatory auditability, the LLM does not decide the final score. A deterministic Python engine calculates the composite risk using the AI's extracted vectors:

$\text{Risk Score} = (\text{Taxonomy} \times \text{Recency} \times \frac{\text{Confidence}}{100}) + \text{Corroboration Multiplier}$

### 4. UI/UX Workflow Automation
The Streamlit frontend aggregates the data into an enterprise dashboard, automatically assigning a workflow action based on the mathematical threshold:
* **Score 1-3:** 🟢 Automated Clear & Archive
* **Score 4-7:** 🟡 Trigger Enhanced Due Diligence (EDD)
* **Score 8-10:** 🔴 Immediate Level-2 Compliance Escalation

---

## ✨ Key Features Built
* **Case Metadata Generation:** Auto-generates unique `UUID` audit IDs and UTC timestamps for every query.
* **Explainable AI (XAI):** Provides a plaintext justification for *why* vectors were assigned, mapping back to the original source URLs.
* **Developer Audit Tab:** A built-in JSON payload inspector allowing engineers to view the raw LLM output structure.
* **Stateful Metric Cards:** UI dynamically updates color codes and actionable buttons based on real-time risk calculations.

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/amandeepnayan/adverse-media-copilot.git](https://github.com/amandeepnayan/adverse-media-copilot.git)
   cd adverse-media-copilot

2. **Install dependencies:**
```bash
pip install -r requirements.txt

```
3. **Configure API Keys:**
* Open `app.py`
* Replace `PASTE_YOUR_GROQ_API_KEY_HERE` with your free key from `console.groq.com`.

4. **Launch the Engine:**
```bash
python -m streamlit run app.py

```