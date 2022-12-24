from seleniumwire import webdriver  # Import from seleniumwire

# Set headless
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(options=chrome_options)
chrome_options.headless = True

# Go to the Google home page
driver.get('https://www2.kickassanime.ro/anime/chainsaw-man-799659/episode-11-222087')

# Access requests via the `requests` attribute
for request in driver.requests:
    if request.response:
        print(
            request.url,
            request.response.status_code,
            request.response.headers['Content-Type']
        )