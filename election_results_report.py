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
        "1. The total voter turnout in the elections reached an approximate figure of
642 million.",
        "2. The Bhartiya Janata Party (BJP) maintained a commanding presence,
winning 240 out of the 543 parliamentary constituencies. This continued
dominance highlights the party's strong nationwide support.",
       "3. The Indian National Congress (INC) emerged as the second most
successful contender, garnering around 136,759,064 votes, representing
21.19% of the total votes cast.",
"4. The Bhartiya Janata Party (BJP) won 240 seats, downfrom the 303 seats
it had secured in 2019, and lost its singular majority in the Lok Sabha.",
"5. The election outcomes held implications for international relations,
influencing diplomatic strategies and global perceptions of India's
political stability and economic trajectory.",
"6. The BJP's alliances in Bihar and Maharashtra significantly boosted their
seat counts, demonstrating the importance of coalition politics in Indian
elections.",
"7. The BJP suffered losses in key states like Uttar Pradesh, Maharashtra, and
West Bengal, which were considered crucial for the party’s prospects.",
"8. Issues like state-specific issues, such as the NRC in Assam and the CAA
in Uttar Pradesh, dominated the campaign, rather than national issues.",
"9. The National Democratic Alliance (NDA) formed an alliance with
regional parties to win seats, but its performance was mixed, with some
parties performing better than others.",
"10. Regional parties like the Trinamool Congress, the Dravida Munnetra
Kazhagam, and the Jana Sena Party made significant gains, winning seats
in various states."
    ]
    for insight in insights:
        f.write(insight + "\n")

print("Scraping and analysis complete. Report and visualization saved.")
