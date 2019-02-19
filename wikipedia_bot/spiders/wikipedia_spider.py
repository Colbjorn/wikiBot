import scrapy

class QuotesSpider(scrapy.Spider):
    name = "wiki"
    maxCount = 5
    historyHeadings = []
    historyUrls = []
    currentUrl = 'https://en.wikipedia.org/wiki/Athletics_at_the_2000_Summer_Olympics_%E2%80%93_Men%27s_20_kilometres_walk'
    goalUrl = 'https://en.wikipedia.org/wiki/Adolf_Hitler'
    blacklist = [
        'https://en.wikipedia.org/wiki/Portal:Contents',
        'https://en.wikipedia.org/wiki/Help:Category',
        'https://en.wikipedia.org/wiki/Special:MyTalk',
        'https://en.wikipedia.org/wiki/Special:MyContributions',
        'https://donate.wikimedia.org/wiki/Special:FundraiserRedirector?utm_source=donate&utm_medium=sidebar&utm_campaign=C13_en.wikipedia.org&uselang=en',
        'https://en.wikipedia.org/wiki/Wikipedia:Contact_us'
    ]
    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/Athletics_at_the_2000_Summer_Olympics_%E2%80%93_Men%27s_20_kilometres_walk',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):  # Recursive pathfinder
        print('''
        
        
        ''')
        print('Currently at ' + self.currentUrl)
        print()
        print('History: ')
        print(self.historyUrls)

        # If the goal is reached, yields number of clicks and history.
        if self.currentUrl == self.goalUrl:
            self.maxCount = len(self.historyUrls)
            yield {
                'Clicks': len(self.historyUrls),
                'History': self.historyHeadings
            }
            del self.historyHeadings[-1]
            del self.historyUrls[-1]

        # Update tracking, then end recursive branch.
        elif len(self.historyUrls) == self.maxCount:
            del self.historyHeadings[-1]
            del self.historyUrls[-1]

        elif len(self.historyUrls) > self.maxCount:
            yield 'MaxCount error'

        # Updates count and history, generates a list then iterates through it.
        else:
            self.historyHeadings.append(response.css('h1::text').get())
            self.historyUrls.append(self.currentUrl)

            for a in response.css('a').xpath('@href').extract():
                if a is not None:
                    a = response.urljoin(a)
                    if self.currentUrl not in a:
                        if a not in self.blacklist:
                            if 'en.wikipedia.org' in a:
                                self.currentUrl = a
                                yield response.follow(a, callback=self.parse)
