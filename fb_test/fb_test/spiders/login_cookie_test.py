import scrapy

class LoginSpider(scrapy.Spider):
    name = 'login_cookie_test'
    start_urls = ['https://www.facebook.com/login.php']

    def start_requests(self):
        return [scrapy.Request('https://facebook.com/login.php', meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        print 'Preparing login'
        lsd = scrapy.Selector(response).xpath('//input[@name="lsd"]/@value').extract_first()
        print lsd
        lgnrnd = scrapy.Selector(response).xpath('//input[@name="lgnrnd"]/@value').extract_first()
        print lgnrnd
        return scrapy.FormRequest.from_response(
            response,
            meta = {'cookiejar' : response.meta['cookiejar']},
            formdata = {
                'lsd': lsd, 
                'email':'thuxky@gmail.com', 
                'pass':'xky940702',
                'lgnrnd':lgnrnd},
            callback = self.after_login
        )

    def after_login(self, response):
        filename = 'log.txt'
        with open(filename, 'w') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        return
