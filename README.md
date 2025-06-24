# EthioMart Amharic E-commerce Data Extractor for FinTech Insights

## Overview

This project tackles the challenge of decentralized e-commerce activities on Telegram in Ethiopia. Many independent e-commerce channels operate in silos, creating inefficiencies for vendors and customers. EthioMart aims to centralize this by building a unified platform that consolidates **real-time data** from various Telegram channels.

The core of this solution is an **Amharic Named Entity Recognition (NER) system**. This system automatically extracts crucial business entities like product names, prices, and locations from unstructured Amharic text, images, and documents found in Telegram posts. The extracted structured data will populate EthioMart's centralized database, transforming it into a comprehensive e-commerce hub and a powerful FinTech engine to identify promising vendors for micro-lending opportunities.

This repository contains the code and documentation for the end-to-end workflow, from data ingestion and preprocessing to LLM fine-tuning and conceptual vendor analysis.

## Key Features & Components

The project is structured into distinct tasks, each contributing to the overall solution:

1.  **Data Ingestion & Preprocessing:**
    * **Dual-strategy scraping** of over **8 active Ethiopian e-commerce Telegram channels** for both historical data (30,000+ messages) and real-time message ingestion.
    * Robust **preprocessing pipeline** for Amharic text, including emoji removal, punctuation normalization, and **Amharic-aware subword tokenization** using `Davlan/bert-base-multilingual-cased-finetuned-amharic` tokenizer.
    * Separation and storage of metadata (sender, timestamp) from message content.

2.  **Dataset Labeling for NER (CoNLL Format):**
    * Manual labeling of a subset of preprocessed Amharic messages (currently **2500 samples**) in the standardized CoNLL format.
    * Entities include: `Product`, `Price`, `Location`.
    * Interactive Python script for context-aware, token-by-token labeling.

3.  **Fine-Tuning an NER Model (PEFT/LoRA):**
    * Utilized **Parameter-Efficient Fine-Tuning (PEFT)** with the **LoRA (Low-Rank Adaptation)** methodology for efficient LLM adaptation.
    * Fine-tuned on the labeled Amharic dataset using the Hugging Face `Trainer` API.

4.  **Model Comparison & Selection:**
    * Compared the performance of `XLM-RoBERTa`, `BERT`, and `AFROMXLM` (`masakhane/afroxlmr-large-ner-masakhaner-1.0_2.0`).
    * **AFROMXLM** emerged as the best-performing model with an **F1-score of ~55.1%**, significantly outperforming generic multilingual models (0% F1-score). This highlights the importance of domain and language-specific pre-training.

5.  **Model Interpretability (Conceptual):**
    * Explored the conceptual application of **SHAP** and **LIME** to understand model predictions, emphasizing their role in building trust and debugging. (Practical implementation for this submission was limited due to time).

6.  **FinTech Vendor Scorecard for Micro-Lending:**
    * Developed a conceptual "Vendor Analytics Engine" to process vendor posts.
    * Calculated key performance metrics: **Posting Frequency**, **Average Views per Post** (simulated), and **Average Price Point** (simulated).
    * Designed a simple, weighted **"Lending Score"** to rank vendors.

## Technical Stack & Tools

* **Language:** Python 3.8+
* **Telegram Interaction:** `telethon`
* **Environment Management:** `python-dotenv`
* **Data Manipulation:** `pandas`
* **NLP & LLM Fine-tuning:** `transformers`, `peft`, `datasets`, `accelerate`
* **Evaluation Metrics:** `evaluate`, `seqeval`
* **Model Interpretability:** `shap`, `lime` (conceptual usage)
* **Computing Environment:** Google Colab (recommended for GPU access), Local Machine with GPU.
* **Version Control:** Git, GitHub

### Prerequisites

* Python 3.8+
* Access to a GPU (recommended for fine-tuning)
* **Telegram API Credentials:** Obtain `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).
* **Hugging Face Account & Token:** Create an account on [huggingface.co](https://huggingface.co/) and generate a `read` access token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).