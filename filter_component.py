from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

from config import logger


class FilterComponent:

    FILTER_MENU = (By.ID, "filter-menu")
    FILTER_BUTTON = (By.CSS_SELECTOR, "a.ytd-toggle-button-renderer")
    VIEW_COUNT_LINK = (By.CSS_SELECTOR,
        "ytd-search-filter-group-renderer.style-scope:nth-child(5) > \
            ytd-search-filter-renderer:nth-child(6) > a:nth-child(1)")
    RESULTS_CONTAINER = (By.ID, "contents")
    VIDEO_SELECTOR = (By.TAG_NAME, "ytd-video-renderer")

    def __init__(self, driver):

        self.driver = driver
        self.results = []

    def sort_results(self):
        """Sort results by view count"""

        try:
            wait = WebDriverWait(self.driver, timeout=10)
            filter_menu_ready = wait.until(EC.visibility_of_element_located((self.FILTER_MENU)))

            if filter_menu_ready:
                logger.info("Sorting search results by view count...")

                filter_button = self.driver.find_element(*self.FILTER_BUTTON)
                filter_button.click()

                view_count_filter = self.driver.find_element(*self.VIEW_COUNT_LINK)
                view_count_filter.click()

                # move mouse to the right edge to avoid mouse over texts during screenshot
                window_width = self.driver.get_window_size().get("width")

                actions = ActionChains(self.driver)
                actions.move_by_offset(xoffset=window_width/2, yoffset=0)
                actions.perform()

                self._select_video_elements()

        except TimeoutException:
            logger.error("Timed out waiting for filter menu!")
            self.driver.quit()

        return self.results

    def _select_video_elements(self):
        """Select top 3 results"""

        logger.info("Getting video elements to take screenshots...")

        sleep(2)

        videos = self.driver.find_elements(*self.VIDEO_SELECTOR)

        # select top 3 videos
        self.results.extend(videos[:3])
