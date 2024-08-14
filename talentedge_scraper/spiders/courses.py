import scrapy
from ..items import TalentedgeScraperItem

class CoursesSpider(scrapy.Spider):
    name = 'courses'
    allowed_domains = ['talentedge.com']
    start_urls = [
        "https://talentedge.com/golden-gate-university/doctor-of-business-administration",
        "https://talentedge.com/iim-kozhikode/professional-certificate-programme-in-hr-management-and-analytics",
        "https://talentedge.com/ecornell/certificate-course-data-analytics-360",
        "https://talentedge.com/ecornell/certificate-course-strategic-human-resources-leadership",
        "https://talentedge.com/ecornell/certificate-course-executive-leadership",
        "https://talentedge.com/ecornell/certificate-course-digital-transformation",
        "https://talentedge.com/ecornell/certificate-course-human-resources-management",
        "https://talentedge.com/ecornell/certificate-course-technology-leadership",
        "https://talentedge.com/opjindal-global-business-school/masters-of-business-administration-opj-global-university",
        "https://talentedge.com/esgci-school-of-management-paris/doctorate-of-business-administration-esgci"
    ]

    def parse(self, response):
        item = TalentedgeScraperItem()
        
        # Extracting course name and URL
        item['course_name'] = response.css("h1::text").get(default='').strip()
        item['course_url'] = response.url
        
        # Extracting course description
        item['descriptions'] = response.css(".desc p::text").get(default='').strip()

        # Extracting duration information
        first_li = response.xpath('//div[@class="duration-of-course"]/ul/li[1]')
        if first_li:
            all_text = first_li.xpath('.//text()').getall()
            item['duration'] = ''.join(all_text).strip()
        else:
            item['duration'] = ''

        # Extracting course start date
        course_start_li = response.xpath('//div[@class="duration-of-course"]/ul/li[2]')
        if course_start_li:
            all_text = course_start_li.xpath('.//text()').getall()
            item['start_date'] = ''.join(all_text).strip()
        else:
            item['start_date'] = ''

        # Extracting lists of "what you will learn" and key skills
        what_you_will_learn_list = response.css(".pl-deeper-undstnd li::text").getall()
        item['what_you_will_learn'] = [text.strip() for text in what_you_will_learn_list]

        key_skills = response.css(".key-skills-sec li::text").getall()
        item['skills'] = [text.strip() for text in key_skills]

        # Extracting target students and eligibility
        item['target_students'] = response.css(".cs-content h4::text").get(default='').strip()
        item['eligibility'] = response.css(".eligible-right-top-list p::text").get(default='').strip()

        # Extracting course content
        sections = response.css(".tab-pane")
        all_li_items = []
        for section in sections:
            li_items = section.css('ul li::text').getall()
            all_li_items.extend(li_items)
        item["content"] = [text.strip() for text in all_li_items]

        # Extracting faculty details
        faculty_details = response.css(".best-fdetail")
        faculty_info = {}
        for i, faculty in enumerate(faculty_details[:3]):
            faculty_info[f"faculty_{i+1}_name"] = faculty.css('h4::text').get(default='').strip()
            faculty_info[f"faculty_{i+1}_designation"] = faculty.css('p::text').get(default='').strip()
            faculty_info[f"faculty_{i+1}_description"] = faculty.css('a.showFacultyDescription::attr(data-description)').get(default='').strip()

        item.update(faculty_info)
        item['institute_name'] = response.css(".plc-institute h4::text").get(default='').strip()

        # Extracting fee information
        divs = response.css('div.program-details-total-pay-amt-right')
        if len(divs) > 0:
            first_div = divs[0]
            fee_in_INR = first_div.xpath('.//text()').get(default='').strip()
            item['fee_in_INR'] = fee_in_INR
        else:
            item['fee_in_INR'] = ''

        if len(divs) > 1:
            second_div = divs[1]
            second_div_text = second_div.xpath('.//text()').getall()
            fee_in_USD = ''.join(second_div_text).strip()
            item['fee_in_USD'] = fee_in_USD
        else:
            item['fee_in_USD'] = ''

        yield item























