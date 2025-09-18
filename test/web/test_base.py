# pip install playwright
# playwright install

from playwright.sync_api import sync_playwright

class WebBase:
    def setup_method(self):
        self.app_url = 'http://localhost:8080'
        
        # ---- Playwright startup
        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(headless=True, args=["--disable-search-engine-choice-screen"])
        self._context = self._browser.new_context(viewport={"width": 1920, "height": 1080})
        self.page = self._context.new_page()
        
        # Set default timeouts
        self.page.set_default_navigation_timeout(15000) 
        self.page.set_default_timeout(15000)           

        # Go to application
        self.page.goto(self.app_url)

    def teardown_method(self):
        # Close the browser
        self._context.close()
        self._browser.close()
        self._pw.stop()
