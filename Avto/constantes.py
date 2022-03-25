INFORMATION = {
                'title': '//h1[@class="head"]/text()',
                'mileage': '//div[@class="mb-10 bold dhide"]/text()',
                'username': '//h4[@class="seller_info_name bold"]/text()',
                'img_url': '//img[@class="outline m-auto"]/@src',
                'car_number': '//span[@class="state-num ua"]/text()',
                'car_vin_code': '//span[@class="vin-code"]/text()',
                'img_total_count': '//span[@class="count"]/span[@class="dhide"]/text()',
                'phone_number': '//span/@data-phone-number',
                'usd_price': '//span[@class="price_value bold"]/text()'
            }

EXCEPT = ['car_number', 'car_vin_code']