from filter_component import FilterComponent


class SearchResultsPage:

    def __init__(self, driver):

        self.driver = driver

    def sort_results_by_view_count(self):
        """Sort results by view count and return top results

        :rtype: list
        :returns: List of video elements
        """

        filter_component = FilterComponent(self.driver)
        top_results = filter_component.sort_results()

        return top_results
