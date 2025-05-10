# 🥗 Diet Maker App

## Overview

**Diet Maker** is an intelligent and customizable web application built with AI and LLM integration. Designed for nutritionists or individual users, this app helps create personalized diet plans based on user input, medical conditions, and blood report analysis. It also features PDF generation and history tracking to streamline health management.

## Features

- 📋 **Dynamic Diet Planning**
- 💉 **Blood Report Parsing (PDF & Manual Input)**
- 🧠 **LLM Integration for Recommendations**
- 📂 **RAG-based Document Querying**
- 🗂️ **Patient Data Storage**
- 🖨️ **PDF Export with Markdown Support**
- 🔍 **Food Item Search with Category Filter**
- 🧾 **Chat-based Interaction with Context History**

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python, LangChain, OpenAI/Groq/Google Gemini
- **PDF Handling**: `reportlab`, `markdown2`
- **RAG (Retrieval-Augmented Generation)**: LangChain + local file store

## Setup Instructions

### 🔧 Requirements

- Python 3.10+
- pip
- Recommended: 8GB+ RAM

### 📦 Installation

```bash
git clone https://github.com/yourusername/diet-maker.git
cd diet-maker

python -m venv venv
venv\Scripts\activate  # On Windows

pip install -r requirements.txt

Keys:
GROQ_API_KEY=your_key
GOOGLE_API_KEY=your_key

Built with ❤️ by Achal.