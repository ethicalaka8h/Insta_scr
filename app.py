import time
import random
import requests
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from user_agent import generate_user_agent as agent

class InstagramScraper:
    def __init__(self):
        self.console = Console()
        self.session = requests.Session()
        self.logged_in = False
        self.user_id = None
        
    def display_header(self):
        header = Text("Instagram Follower Scraper", style="bold blue")
        panel = Panel(header, border_style="green")
        self.console.print(panel)
        
    def login(self):
        self.display_header()
        
        table = Table(show_header=False, show_edge=False)
        table.add_row("USERNAME:", "[bold cyan]")
        table.add_row("PASSWORD:", "[bold cyan]")
        self.console.print(table)
        
        user = self.console.input("[bold]USERNAME: [/bold]")
        passwd = self.console.input("[bold]PASSWORD: [/bold]", password=True)
        
        headers = {
            'User-Agent': agent(),
            'Referer': 'https://www.instagram.com/accounts/login/'
        }
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Logging in...", total=100)
            
            
            self.session.get("https://www.instagram.com/accounts/login/", headers=headers)
            token = self.session.cookies.get('csrftoken')
            
            headers.update({
                'x-csrftoken': token,
                'X-Requested-With': 'XMLHttpRequest',
                'X-IG-App-ID': '936619743392459'
            })
            
            progress.update(task, advance=30)
            
            
            timestamp = str(int(time.time()))
            data = {
                'username': user,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{passwd}',
                'queryParams': '{}',
                'optIntoOneTap': 'false'
            }
            
            
            response = self.session.post(
                'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                data=data,
                headers=headers
            )
            
            progress.update(task, advance=70)
            
            if '"authenticated":true' in response.text:
                self.logged_in = True
                self.user_id = response.json().get("userId")
                progress.update(task, completed=100)
                self.console.print("[bold green]✓ Login successful![/bold green]")
                return True
            else:
                progress.update(task, completed=100)
                error_msg = response.json().get("message", "Unknown error")
                self.console.print(f"[bold red]✗ Login failed: {error_msg}[/bold red]")
                return False
    
    def get_user_id(self, username):
        headers = {
            'User-Agent': agent(),
            'X-IG-App-ID': '936619743392459'
        }
        
        try:
            response = self.session.get(
                f'https://www.instagram.com/api/v1/web/search/topsearch/?context=blended&query={username}',
                headers=headers
            )
            
            if response.status_code == 200:
                for user in response.json().get('users', []):
                    if user['user']['username'].lower() == username.lower():
                        return user['user']['pk']
        except Exception as e:
            self.console.print(f"[red]Error getting user ID: {str(e)}[/red]")
        
        return None    
    def scrape_followers(self, target_user=None):
        if not self.logged_in:
            self.console.print("[red]You must login first![/red]")
            return            
        target_id = self.user_id  
        if target_user:
            with self.console.status("[cyan]Getting target user ID..."):
                target_id = self.get_user_id(target_user)
                
            if not target_id:
                self.console.print(f"[red]Could not find user: {target_user}[/red]")
                return
                
            self.console.print(f"[green]Found user ID: {target_id} for {target_user}[/green]")
        
        followers = []
        next_max_id = ''
        total_collected = 0
        retry_count = 0
        max_retries = 3
        
        headers = {
            'User-Agent': 'Instagram 155.0.0.37.107 Android',
            'X-IG-App-ID': '936619743392459',
            'Referer': f'https://www.instagram.com/{target_user or user}/'
        }
        
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Scraping followers...", total=None)
            
            while True:
                try:
                    url = f"https://i.instagram.com/api/v1/friendships/{target_id}/followers/?count=200"
                    if next_max_id:
                        url += f"&max_id={next_max_id}"
                        
                    response = self.session.get(url, headers=headers)
                    
                    if response.status_code == 429:
                        self.console.print("[yellow]Rate limit hit, waiting 60 seconds...[/yellow]")
                        time.sleep(60)
                        continue
                        
                    if response.status_code != 200:
                        self.console.print(f"[red]Error: HTTP {response.status_code}[/red]")
                        retry_count += 1
                        if retry_count >= max_retries:
                            break
                        time.sleep(5)
                        continue
                        
                    try:
                        data = response.json()
                    except ValueError:
                        self.console.print("[red]Error parsing JSON response[/red]")
                        retry_count += 1
                        if retry_count >= max_retries:
                            break
                        time.sleep(5)
                        continue
                        
                    for user in data.get("users", []):
                        followers.append(user['username'])
                        
                    total_collected = len(followers)
                    progress.update(task, description=f"[cyan]Scraping followers... [green]{total_collected}[/green] collected")
                    
                    next_max_id = data.get("next_max_id")
                    if not next_max_id:
                        break
                        
                    
                    delay = random.uniform(2.5, 6.0)
                    time.sleep(delay)
                    
                except Exception as e:
                    self.console.print(f"[red]Error: {str(e)}[/red]")
                    retry_count += 1
                    if retry_count >= max_retries:
                        break
                    time.sleep(10)
        
        
        if followers:
            timestamp = int(time.time())
            filename = f"followers_{target_user or 'self'}_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                for username in followers:
                    f.write(username + '\n')
                    
            self.console.print(f"\n[bold green]✓ Successfully saved {len(followers)} followers to {filename}[/bold green]")
        else:
            self.console.print("[red]No followers were collected[/red]")

def main():
    scraper = InstagramScraper()
    
    if scraper.login():
        target_user = scraper.console.input("[bold]Enter target username (leave empty for your own followers): [/bold]")
        scraper.scrape_followers(target_user if target_user else None)

if __name__ == "__main__":
    main()
