from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import scrape
import tiktoken


dictionary = {
    "Organizations": [
        "Santa Clara County Homlessness Prevention System",
        "The Emergency Assistance Network",
        "HIF’s Emergency Housing Fund",
        "Chronicle Season of Sharing Fund",
        "St. Vincent de Paul Society of San Francisco",
        "Los Gatos Anti-Racism Coalition",
        ],
    "General Information": [],
    "Website": [
        "https://preventhomelessness.org/",
        "https://uwba.org/what-we-do/emergency-assistance-network-ean/",
        "https://www.hifinfo.org/programs/emergency-housing-fund/",
        "https://seasonofsharing.org/get-help/",
        "https://www.svdp.org/if-you-need-help/parish-conferences/",
        "https://lgarc.org/rental-assistance/"
        ],
    "Published Eligibility Requirements": [],

}

model = OllamaLLM(model="gemma3:4b", streaming=True, temperature=0.2)

tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(tokenizer.encode(text))



def extract_relevant_sections(content):
    """Extract sections likely to contain eligibility info with token limit awareness"""
    MAX_TOKENS = 3500  # Below LLM's 4000 token limit
    patterns = [
        r"eligibility.*?requirements(.+?)(?=\.\s{2,}|$)",
        r"qualify.*?assistance(.+?)(?=\.\s{2,}|$)",
        r"apply.*?program(.+?)(?=\.\s{2,}|$)",
        r"criteria.*?help(.+?)(?=\.\s{2,}|$)"
    ]
    
    sections = []
    total_tokens = 0
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        for match in matches:
            match_tokens = count_tokens(match)
            if total_tokens + match_tokens <= MAX_TOKENS:
                sections.append(match)
                total_tokens += match_tokens
            else:
                break
    
    return "\n\n".join(sections) if sections else content[:MAX_TOKENS]


def get_website_content(url):
    html_content = scrape.scraper(url)
    body_content = scrape.extract_body_content(html_content)
    cleaned_content = scrape.clean_body_content(body_content)
    return cleaned_content  


def get_eligibility_requirements(content):
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
            "You are a housing policy analyst specializing in rental assistance programs. "
            "Your task is to precisely identify and extract published eligibility criteria from program documentation."
        ),
        ("user",
            "**Extraction Task:** Analyze the provided content for RENTAL ASSISTANCE ELIGIBILITY REQUIREMENTS\n\n"
            "{content}\n\n"
            "**Extraction Rules:**\n"
            "1. Extract ONLY: Income thresholds, residency conditions, documentation requirements, "
            "household composition rules, and qualification criteria\n"
            "2. EXCLUDE: Application procedures, benefit amounts, program descriptions, "
            "contact information, and non-eligibility content\n"
            "3. Specificity: Include exact numbers/ranges when available (e.g., 'Income below 50% AMI')\n"
            "4. Scope: Include all published requirements (both mandatory and optional)\n"
            "**Output Instructions:**\n"
            "- If no requirements found: 'None published'\n"
        )
    ])
    
    chain = prompt | model
    return chain.invoke({"content": content}).strip()


def get_general_info(content):
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
            "You are an information extraction expert. Analyze the provided website content and "
            "identify ONLY general organizational information. Focus exclusively on permanent "
            "attributes and fundamental characteristics of the organization."
        ),
        ("user",
            "Content Analysis Task:\n"
            "Extract the organization's general information from this content:\n\n"
            "{content}\n\n"
            "Extraction Guidelines:\n"
            "1. Include ONLY: Mission, overview, history, core values, founding principles, "
            "and permanent activities\n"
            "2. EXCLUDE ALL: Requirements, eligibility criteria, application processes, "
            "deadlines, fees, dates, and time-sensitive information\n"
            "3. Formatting: Use plain text only (no markdown, bullets, or special formatting)\n"
            "4. Output: Return a concise paragraph (3-5 sentences maximum)\n\n"
            "Output Requirement: If no relevant information is found, return 'No general information available'"
        )
    ])

    chain = prompt | model
    return chain.invoke({"content": content}).strip()



def process_data(website):
    try:
        website_content = get_website_content(website)
        token_count = count_tokens(website_content)        
        if token_count > 3500:
            # Use intelligent splitting
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=3000,
                chunk_overlap=200,
                length_function=count_tokens
            )
            chunks = text_splitter.split_text(website_content)
            
            # Process chunks sequentially
            requirements = []
            for chunk in chunks:
                result = get_eligibility_requirements(chunk)
                if "none published" not in result.lower():
                    requirements.append(result)

            general_info = []
            for chunk in chunks:
                result = get_general_info(chunk)
                general_info.append(result)
            
            eligibility_requirements = "\n\n".join(requirements) or "None published"
            general_information = "\n\n".join(general_info) or "No general information found"

        else:
            # Process in single call
            eligibility_requirements = get_eligibility_requirements(website_content)
            general_information = get_general_info(website_content)

        dictionary["Published Eligibility Requirements"].append(clean_eligibility_data(eligibility_requirements))
        dictionary["General Information"].append(general_information)

        return True
        
    except Exception as e:
        print(f"Error processing {website}: {str(e)}")
        dictionary["Published Eligibility Requirements"].append("Error: " + str(e))
        dictionary["General Information"].append("Error: " + str(e))
        return False
    

def clean_eligibility_data(text):
    """
    Cleans eligibility criteria text by:
    1. Removing all asterisk (*) characters
    2. Trimming leading/trailing whitespace from each line
    3. Preserving the original line structure
    """
    lines = text.splitlines()
    cleaned_lines = []
    
    for line in lines:
        # Remove all asterisks and trim whitespace
        clean_line = line.replace('*', '').strip()
        # Only keep non-empty lines
        if clean_line:
            cleaned_lines.append(clean_line)
    
    return '\n'.join(cleaned_lines)

def get_data():
    dictionary["General Information"].clear()
    dictionary["Published Eligibility Requirements"].clear()
    for website in dictionary["Website"]:
        if not process_data(website):
            print(f"Failed to process requirements for {website}")
    return dictionary
