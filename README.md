# Requirements_For_Rental_Assistant

> This project was created during my volunteer internship at [Havensafe](https://havensafe.org)

## 🏢 About This Project
**Our Purpose:**  
*"Streamline access to critical housing resources by automatically gathering and organizing rental assistance eligibility requirements from multiple service providers, enabling faster connections between at-risk communities and life-saving support."*

This system helps prevent homelessness by maintaining up-to-date information on rental assistance programs, their requirements, and contact information.

---

This repository contains an automated pipeline that collects and organizes rental assistance program information from multiple Bay Area organizations. The system extracts eligibility requirements and general information, then updates a Google Sheet with formatted results.

## ✨ Features
- AI-powered content extraction using Gemma3 LLM
- Web scraping with dynamic content handling
- Google Sheets formatting with hyperlinks
- Timezone-aware timestamps (PST/PDT)
- Token-aware content processing
- Error handling and fallback mechanisms

## ⚙️ How It Works
1. **Scraping**: The `scrape.py` script:
   - Uses headless Chrome to render dynamic content
   - Waits for page elements to load
   - Scrolls to trigger lazy-loaded content
   - Cleans and extracts relevant HTML

2. **AI Processing**: The `parse.py` script:
   - Splits content using token-aware chunking
   - Uses Gemma3 model to extract:
     - Eligibility requirements
     - General organization information
   - Cleans and formats extracted data

3. **Google Sheets Update**: The `main.py` script:
   - Connects to Google Sheets API
   - Formats headers with custom colors
   - Updates organization data with hyperlinks
   - Adds last updated timestamp (California time)
   - Applies consistent cell formatting

4. **Content Extraction Logic**:
   - Token counting with tiktoken
   - Intelligent content chunking
   - Prompt engineering for precise extraction
   - Fallback processing for large content

## 🛠️ Technical Requirements
- Python 3.10+
- Packages in `requirements.txt`
- Ollama with Gemma3 model (`gemma3:4b`)
- Google Service Account credentials
- ChromeDriver (automatically installed)

## 🔒 Security
- Google credentials stored in `credentials.json` (excluded via `.gitignore`)
- The service account has limited Google Sheets access
- No personal data collection or processing

## ⏱️ Update Schedule
The system can be configured to run:
- On-demand via manual execution
- Scheduled via cron job or GitHub Actions
- Triggered by data changes

## Data Protection

This repository does not handle personal user data. All automation interacts only with:
- Public websites (via web scraping)
- Google Sheets API (using service account credentials)

## 🚀 Getting Started
1. Clone repository:
   ```bash
   git clone https://github.com/your-username/rental-assistance-tracker.git
