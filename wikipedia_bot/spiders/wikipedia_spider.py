import scrapy

class QuotesSpider(scrapy.Spider):
    name = "wiki"
    count = 0
    maxCount = 5
    historyHeadings = []
    historyUrls = []
    currentUrl = 'https://en.wikipedia.org/wiki/Athletics_at_the_2000_Summer_Olympics_%E2%80%93_Men%27s_20_kilometres_walk'
    goalUrl = 'https://en.wikipedia.org/wiki/Adolf_Hitler'

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/Athletics_at_the_2000_Summer_Olympics_%E2%80%93_Men%27s_20_kilometres_walk',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):  # Recursive pathfinder

        # If the goal is reached, yields number of clicks and history.
        if self.currentUrl == self.goalUrl:
            self.maxCount = self.count
            yield {
                'Clicks': self.count,
                'History': self.historyHeadings
            }
            self.count -= 1
            del self.historyHeadings[-1]
            del self.historyUrls[-1]

        # Update tracking, then end recursive branch.
        elif self.count == self.maxCount:
            self.count -= 1
            del self.historyHeadings[-1]
            del self.historyUrls[-1]

        elif self.count > self.maxCount:
            yield 'MaxCount error'

        # Updates count and history, generates a list then iterates through it.
        else:
            self.count += 1
            self.historyHeadings.append(response.css('h1::text').get())
            self.historyUrls.append(self.currentUrl)

            for a in response.css('a'):
                if self.currentUrl not in a:
                    self.currentUrl = a
                    yield response.follow(a, callback=self.parse)
