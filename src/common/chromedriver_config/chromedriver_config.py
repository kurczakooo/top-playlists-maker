from .user_agent_string_config import generate_user_agent_string
from selenium.webdriver.chrome.options import Options

user_agent_string = generate_user_agent_string()
user_agent_string_override_command = user_agent_string.split('=')[1]

chrome_options = Options()

# Headless mode (new version, bardziej stabilna)
chrome_options.add_argument("--headless=new")

# Disable features that reveal automation
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Sandbox and resource handling (ważne dla GHA)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# GPU and rendering stuff
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-webgl")

# Disable some default Chrome UI
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--metrics-recording-only")
chrome_options.add_argument("--disable-default-apps")

# Headless Chrome performance tuning
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--window-size=1920,1080")

# Optional: less "suspicious" networking behavior
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-renderer-backgrounding")

# Set a custom user agent string that mimics a normal desktop user 
# (it's telling the browser the user uses Mozilla on windows 10 with a speciic webKit and KHTML engine, Chrome ver.91, and a ver. of Webkit to render for Safari)
chrome_options.add_argument(user_agent_string)