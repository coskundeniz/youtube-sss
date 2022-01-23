from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import logger
from search_results_page import SearchResultsPage
from screenshot_manager import ScreenshotManager


class SearchPage:

    URL = "https://www.youtube.com/"

    SEARCH_FORM = (By.ID, "search-form")
    SEARCH_INPUT_BOX = (By.ID, "search-input")
    SEARCH_RESULTS = (By.ID, "contents")

    def __init__(self, driver):

        self.driver = driver

        self._load()

    def search_for_query(self, query):
        """Enter query to search box and start the search

        :type query: str
        :param query: Search query
        """

        logger.info(f"Starting search for '{query}'...")
        search_input_box = self.driver.find_element(*self.SEARCH_INPUT_BOX)

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(search_input_box, query + Keys.ENTER)
        actions.perform()

        try:
            wait = WebDriverWait(self.driver, timeout=10)
            results_ready = wait.until(EC.visibility_of_element_located((self.SEARCH_RESULTS)))

            if results_ready:
                logger.info("Search results are ready")
                results_page = SearchResultsPage(self.driver)
                top_results = results_page.sort_results_by_view_count()

                screenshot_manager = ScreenshotManager()
                screenshot_manager.take_screenshots_of(top_results)

        except TimeoutException:
            logger.error("Timed out waiting for results to load!")
            self.driver.quit()

    def _load(self):
        """Load YouTube main page"""

        self.driver.get(self.URL)

        try:
            wait = WebDriverWait(self.driver, timeout=10)
            search_box_ready = wait.until(EC.visibility_of_element_located((self.SEARCH_FORM)))

            if search_box_ready:
                logger.info("Page is ready for starting a search")

        except TimeoutException:
            logger.error("Timed out waiting for page to load!")
            self.driver.quit()
