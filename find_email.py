import random
import requests
from bs4 import BeautifulSoup

# Check if validate_email_address and py3dns are installed
try:
    from validate_email_address import validate_email
    import DNS
except ImportError as e:
    print(f"Required package missing: {e}. Please install the package and try again.")
    exit()

def generate_email_patterns():
    additional_patterns = [
        "{first}@{domain}",
        "{last}@{domain}",
        "{first}{last}@{domain}",
        "{first}.{last}@{domain}",
        "{first}_{last}@{domain}",
        "{first}-{last}@{domain}",
        "{first}{last[0]}@{domain}",
        "{first}.{last[0]}@{domain}",
        "{first}_{last[0]}@{domain}",
        "{first}-{last[0]}@{domain}",
        "{first[0]}{last}@{domain}",
        "{first[0]}.{last}@{domain}",
        "{first[0]}_{last}@{domain}",
        "{first[0]}-{last}@{domain}",
        "{first}{middle}{last}@{domain}",
        "{first}.{middle}.{last}@{domain}",
        "{first}_{middle}_{last}@{domain}",
        "{first}-{middle}-{last}@{domain}",
        "{first}{middle[0]}{last}@{domain}",
        "{first}.{middle[0]}.{last}@{domain}",
        "{first}_{middle[0]}_{last}@{domain}",
        "{first}-{middle[0]}-{last}@{domain}",
        "{first[0]}{middle[0]}{last}@{domain}",
        "{first[0]}.{middle[0]}.{last}@{domain}",
        "{first[0]}_{middle[0]}_{last}@{domain}",
        "{first[0]}-{middle[0]}-{last}@{domain}",
        "{first[0]}{last[0]}@{domain}",
        "{first}.{last[0]}@{domain}",
        "{first}_{last[0]}@{domain}",
        "{first}-{last[0]}@{domain}",
        "{first}{middle[0]}@{domain}",
        "{first}.{middle[0]}@{domain}",
        "{first}_{middle[0]}@{domain}",
        "{first}-{middle[0]}@{domain}",
        "{first[0]}{middle[0]}{last}@{domain}",
        "{first[0]}.{middle[0]}.{last}@{domain}",
        "{first[0]}_{middle[0]}_{last}@{domain}",
        "{first[0]}-{middle[0]}-{last}@{domain}",
        "{first[0]}{last[0]}@{domain}",
        "{first}.{last[0]}@{domain}",
        "{first}_{last[0]}@{domain}",
        "{first}-{last[0]}@{domain}",
        "{first}{middle}@{domain}",
        "{first}.{middle}@{domain}",
        "{first}_{middle}@{domain}",
        "{first}-{middle}@{domain}"
    ]

    return additional_patterns

def parse_name(full_name):
    name_parts = full_name.strip().lower().split()
    if len(name_parts) == 1:
        first_name = name_parts[0]
        middle_name = ""
        last_name = ""
    elif len(name_parts) == 2:
        first_name = name_parts[0]
        middle_name = ""
        last_name = name_parts[1]
    else:
        first_name = name_parts[0]
        middle_name = ' '.join(name_parts[1:-1])
        last_name = name_parts[-1]
    return first_name, middle_name, last_name

def generate_email_addresses(name, company_domain):
    first_name, middle_name, last_name = parse_name(name)
    
    patterns = generate_email_patterns()
    random.shuffle(patterns)
    selected_patterns = patterns[:30]  # Select a subset of patterns

    email_addresses = []
    for pattern in selected_patterns:
        try:
            email = pattern.format(first=first_name, middle=middle_name, last=last_name, domain=company_domain)
            email = email.replace("..", ".").replace("__", "_").replace("--", "-")
            email_addresses.append(email)
        except IndexError:
            continue

    email_addresses = list(set(email_addresses))  # Remove duplicates

    return email_addresses

def validate_emails(emails):
    valid_emails = []
    for email in emails:
        if validate_email(email, verify=True):
            valid_emails.append(email)
    return valid_emails

def scrape_emails_from_website(url):
    emails = set()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for mailto in soup.select('a[href^=mailto]'):
            email = mailto['href'].split(':')[1]
            emails.add(email)
        text = soup.get_text()
        emails.update(set([email for email in text.split() if '@' in email]))
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
    return list(emails)

def main():
    print("Welcome to the Email Address Generator!")
    print("This tool generates possible email addresses based on a person's name and company domain.")
    
    name = input("Enter the person's full name (e.g., John Michael Doe): ").strip()
    company = input("Enter the company domain (e.g., example.com): ").strip()

    if not name or not company:
        print("Name and company domain cannot be empty. Please try again.")
        return

    emails = generate_email_addresses(name, company)

    if emails:
        print("\033[1m\nGenerated email addresses:\033[0m")
        for email in emails:
            print(email)
        
        valid_emails = validate_emails(emails)
        if valid_emails:
            print("\033[1m\nValidated email addresses:\033[0m")
            for email in valid_emails:
                print(email)
        else:
            print("No valid email addresses found.")
    else:
        print("No email addresses generated. Please check the input and try again.")
    
    company_website = input("Enter the company website URL to scrape emails (optional): ").strip()
    if company_website:
        scraped_emails = scrape_emails_from_website(company_website)
        if scraped_emails:
            print("\033[1m\nScraped email addresses:\033[0m")
            for email in scraped_emails:
                print(email)
        else:
            print("No emails found on the website.")

if __name__ == "__main__":
    main()
