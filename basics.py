# importing necessary packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def setup_driver():
   chrome_options = Options()
   chrome_options.add_argument('--ignore-certificate-errors')
   chrome_options.add_argument('--allow-insecure-localhost')
   driver = webdriver.Chrome()
   return driver


def scrape_position_stats(driver,position_url):
    driver.get(position_url)
    players = driver.find_elements(By.CSS_SELECTOR, 'body > center > table:nth-child(4) > tbody > tr:nth-child(2) > td.bodycontent > table:nth-child(12) > tbody > tr > td > table > tbody > tr:nth-child(3)')
    
    stats = []

    for player in players:
        name = player.find_element(By.CSS_SELECTOR, 'body > center > table:nth-child(4) > tbody > tr:nth-child(2) > td.bodycontent > table:nth-child(12) > tbody > tr > td > table > tbody > tr:nth-child(3) > td:nth-child(1)').text
        points = player.find_element(By.CSS_SELECTOR, 'body > center > table:nth-child(4) > tbody > tr:nth-child(2) > td.bodycontent > table:nth-child(12) > tbody > tr > td > table > tbody > tr:nth-child(3) > td:nth-child(12)').text
        stats.append((name,float(points)))

    sorted_stats = sorted(stats, key = lambda x: x[1], reverse = True)
    return sorted_stats

def build_best_team(qb_stats, rb_stats, wr_stats):

    best_team = {
        'QB': qb_stats[0],
        'RB': rb_stats[0],
      #  'RB2': rb_stats[1],
        'WR1': wr_stats[0],
        'WR2': wr_stats[1],
    #  'WR3': wr_stats[2],
      #  'TE': te_stats[0],
      #  'K': k_stats[0]
    }
    return best_team

def display_best_team(week, team):
    print(f"Best Possible Fantasy Team for week {week}:\n")
    for position, player in team.items():
        name, points = player
        print(f"{position}: {name} - {points} points")
    
def get_weekly_urls(week):
    base_url = 'https://www.fftoday.com/stats/playerstats.php?Season=2024&GameWeek='

    position_ids = {
        'QB': 10,
        'RB': 20,
        'WR': 30,
      #  'TE': 40,
      #  'K': 80
    }

    urls = {pos: f"{base_url}{week}&PosID={pos_id}&LeagueID=" for pos, pos_id in position_ids.items()}
    return urls

def main():
    driver = setup_driver()

    for week in range(1,2):
        print(f"\nScraping data for week {week}...")

        weekly_urls = get_weekly_urls(week)
        
        qb_stats = scrape_position_stats(driver, weekly_urls['QB'])
        rb_stats = scrape_position_stats(driver, weekly_urls['RB'])
        wr_stats = scrape_position_stats(driver, weekly_urls['WR'])
     #   te_stats = scrape_position_stats(driver, weekly_urls['TE'])
      #  k_stats = scrape_position_stats(driver, weekly_urls['K'])

        best_team = build_best_team(qb_stats,rb_stats,wr_stats)

        display_best_team(week, best_team)


    driver.quit()

if __name__ == "__main__":
    main()