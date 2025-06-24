# Amharic E-commerce Data Extractor for FinTech Insights (EthioMart Project)

## Overview

This project aims to address the decentralization of e-commerce activities on Telegram in Ethiopia by building a centralized platform for EthioMart. The core of this platform is a sophisticated data extraction and processing pipeline, culminating in an Amharic Named Entity Recognition (NER) system. This system will identify key business entities from Telegram messages, images, and documents, ultimately enabling FinTech insights, such as identifying promising vendors for loans.

## Business Need

EthioMart envisions becoming the central hub for Telegram-based e-commerce in Ethiopia. Currently, various independent e-commerce channels operate separately, posing challenges for both vendors and customers in product discovery, order placement, and communication. To overcome this, EthioMart plans to consolidate **real-time data** from these channels into a unified platform, offering a seamless experience for customers and providing valuable insights for the business. The extracted data will populate EthioMart's centralized database, making it a comprehensive e-commerce hub.

## Key Objectives (Current Focus & Future Steps)

* **Data Ingestion & Preprocessing:** Set up a robust system to fetch and prepare messages from Ethiopian-based Telegram e-commerce channels.
* **Named Entity Recognition (NER):** Fine-tune a Transformer-based Large Language Model (LLM) to accurately extract key entities like Product Names or Types, Monetary Values or Prices, and Locations from unstructured Amharic text. Optional entities include Delivery Fees and Contact Information (phone numbers, Telegram usernames).
* **Model Evaluation & Interpretation:** Compare multiple model approaches, interpret predictions using tools like SHAP/LIME, and recommend the best model for EthioMart's business case.

## Project Progress: Data Ingestion and Preprocessing (Task 1)

This section details the work completed on setting up the data pipeline to prepare raw Telegram data for the NER task.

### 1. Data Ingestion System

A custom Python scraper utilizing the `telethon` library has been implemented to fetch data from multiple Ethiopian-based Telegram e-commerce channels. The system is designed with two components:

* **Historical Data Scraping:**
    * Fetches existing messages (text, images, documents) from a list of curated channels.
    * Initial scraping has collected over 30,000 messages, providing a solid foundational dataset for LLM fine-tuning.
    * **Technologies Used:** `telethon`, `python-dotenv` for secure API credential management.
    * **Storage:** Scraped data (text in CSV, media files in a 'photos' directory) is persistently stored in Google Drive to ensure availability across computing sessions.

* **Real-Time Message Ingestion:**
    * A real-time component has been designed to continuously collect new messages as they are posted in the target Telegram channels.
    * This system uses event-driven listeners (`@client.on(events.NewMessage)`) to capture new posts instantly.
    * **Purpose:** This is crucial for fulfilling the business need of consolidating "real-time data," keeping the centralized e-commerce hub constantly updated, and providing fresh data for iterative model fine-tuning.
    * **Storage:** Appends newly ingested messages and downloads associated media to the same persistent storage locations as the historical data.

### 2. Data Preprocessing

The raw message data has undergone several preprocessing steps to prepare it for Named Entity Recognition:

* **Data Loading and Initial Cleaning:**
    * Messages are loaded from the CSV, and missing text values (NaNs) are robustly handled by converting them to empty strings to prevent processing errors.
* **Emoji Removal:**
    * A dedicated `emoji` Python library is used to comprehensively remove emojis from message text. This standardizes the text and removes noise that is irrelevant for NER.
* **Amharic Punctuation Normalization:**
    * Amharic-specific punctuation marks (e.g., `።`, `፣`, `፤`, `፧`) are standardized to their common Latin equivalents (e.g., `.`, `,`, `;`, `?`). This ensures consistency and simplifies subsequent processing.
    * Multiple spaces are also reduced to single spaces, and leading/trailing spaces are removed.
* **Tokenization using Hugging Face Transformer Tokenizer:**
    * For accurate NER, text is tokenized into subword units using a pre-trained tokenizer from the Hugging Face `transformers` library.
    * **Model Choice:** The `Davlan/bert-base-multilingual-cased-finetuned-amharic` model's tokenizer was specifically chosen because it has been fine-tuned on Amharic text, enabling it to effectively handle the Amharic script (Fidel) and its morphology (e.g., prefixes, suffixes). This significantly reduces the occurrence of `[UNK]` (unknown) tokens for Amharic words, ensuring the model can learn from the language.
    * The `tokenizer.tokenize()` method is used to obtain lists of subword tokens, which is the required format for the subsequent CoNLL labeling step.
* **Metadata Separation:**
    * During data ingestion, metadata (Channel Title, Username, Message ID, Date, Media Path) is inherently separated from the core `Message` content and stored in distinct columns in the CSV.
* **Storage of Processed Data:**
    * The cleaned and tokenized data (specifically the message ID, cleaned message text, and the list of `raw_tokens`) is saved to a new CSV file (`processed_telegram_messages.csv`) within the Google Drive structure. This ensures reproducibility, modularity, and efficiency for subsequent steps.

## Next Steps: Labeling a Subset of Dataset in CoNLL Format (Task 2)

The immediate next step involves manually labeling a subset of the processed dataset (30-50 messages) in the CoNLL format. This labeled data will serve as the ground truth for fine-tuning the NER model. An interactive script has been developed to assist in this token-by-token labeling process, providing contextual messages for accurate annotation.

---
**Setup & Running Notes:**
* **Python Environment:** Ensure you have Python 3.8+ and a virtual environment set up.
* **Library Installation:** `pip install telethon python-dotenv transformers pandas emoji`
* **Telegram API Credentials:** Create a `.env` file in your project root with `TG_API_ID`, `TG_API_HASH`, and `phone`.
* **Hugging Face Authentication:** Authenticate your local machine by running `huggingface-cli login` in your terminal and pasting your Hugging Face access token (with `read` role). Ensure you've accepted any terms of use on the Hugging Face model page.
* **Google Drive (for Colab Users):** If using Google Colab, ensure Google Drive is mounted, and adjust file paths to `/content/drive/MyDrive/...` for persistent storage of session files and data.
