from ddgs import DDGS

class WebSearch:

    def search(self, query):

        with DDGS() as ddgs:

            return list(
                ddgs.text(
                    query,
                    max_results=10
                )
            )

web = WebSearch()