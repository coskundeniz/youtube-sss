from config import logger


class ScreenshotManager:

    def take_screenshots_of(self, elements):
        """Take screenshots of given video elements

        For example screenshot is saved with the filename
        "W8KRzm-HUcc.png" for the following video url
        https://www.youtube.com/watch?v=W8KRzm-HUcc

        :type elements: list
        :param elements: List of video elements
        """

        for element in elements:

            video_title = self._get_video_title(element)
            logger.info(f"Taking screenshot of video: {video_title}")

            filename = self._get_unique_video_id(element) + ".png"
            logger.info(f"Saving file as {filename}")

            element.screenshot(filename)

    def _get_video_title(self, element):
        """Get video title

        :type element: WebElement
        :param element: Video element
        :rtype: str
        :returns: Video title
        """

        return element.find_element_by_id("video-title").text

    def _get_unique_video_id(self, element):
        """Get video id

        :type element: WebElement
        :param element: Video element
        :rtype: str
        :returns: Unique video id
        """

        video_href = element.find_element_by_id("video-title").get_attribute("href")
        video_id = video_href.split("=")[1]

        return video_id
