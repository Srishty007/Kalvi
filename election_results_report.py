from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Set up Selenium webdriver
driver = webdriver.Chrome()  # Replace with your preferred browser

# URL of the main page
url = "https://www.bharian.com.my/berita/nasional/2022/11/1028360/keputusan-rasmi-pru15"
driver.get(url)

# Extract content using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract tables with class '_dable-content-wrapper_'
tables = soup.find_all('table', class_='_dable-content-wrapper_')

# Extract data from tables
all_data = []
for table in tables:
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if cells:
            all_data.append([cell.text.strip() for cell in cells])

# Convert data to a DataFrame
columns = ['Constituency', 'Candidate', 'Party', 'Votes', 'Status']
df = pd.DataFrame(all_data, columns=columns)
df['Votes'] = pd.to_numeric(df['Votes'].str.replace(',', ''), errors='coerce')

# Verify the scraped data
print(df.head())

# Perform analysis
party_votes = df.groupby('Party')['Votes'].sum().reset_index()
party_votes = party_votes.sort_values(by='Votes', ascending=False)

# Verify the grouped data
print(party_votes)

# Example visualization
plt.figure(figsize=(12, 8))
plt.bar(party_votes['Party'], party_votes['Votes'])
plt.xlabel('Party')
plt.ylabel('Total Votes')
plt.title('Vote Distribution by Party')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('vote_distribution.png')

# Write the report
with open('election_results_report.md', 'w') as f:
    f.write("# Election Results Report\n")
    f.write("## Key Insights\n")
    insights = [
        "1. The total votes received by each party.",
        "2. The party with the highest number of votes.",
        # Add more insights
    ]
    for insight in insights:
        f.write(insight + "\n")

print("Scraping and analysis complete. Report and visualization saved.")
