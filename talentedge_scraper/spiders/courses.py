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

        # Extract duration information
        first_li = response.xpath('//div[@class="duration-of-course"]/ul/li[1]')
        if first_li:
            all_text = first_li.xpath('.//text()').getall()
            item['duration'] = ''.join(all_text).strip()
        else:
            item['duration'] = ''

        # Extract course start date
        course_start_li = response.xpath('//div[@class="duration-of-course"]/ul/li[2]')
        if course_start_li:
            all_text = course_start_li.xpath('.//text()').getall()
            item['start_date'] = ''.join(all_text).strip()
        else:
            item['start_date'] = ''

        # Extract lists of "what you will learn" and key skills
        what_you_will_learn_list = response.css(".pl-deeper-undstnd li::text").getall()
        item['what_you_will_learn'] = [text.strip() for text in what_you_will_learn_list]

        key_skills = response.css(".key-skills-sec li::text").getall()
        item['skills'] = [text.strip() for text in key_skills]

        # Extract target students and eligibility
        item['target_students'] = response.css(".cs-content h4::text").get(default='').strip()
        item['eligibility'] = response.css(".eligible-right-top-list p::text").get(default='').strip()

        # Extract course content
        sections = response.css(".tab-pane")
        all_li_items = []
        for section in sections:
            li_items = section.css('ul li::text').getall()
            all_li_items.extend(li_items)
        item["content"] = [text.strip() for text in all_li_items]

        # Extract faculty details
        faculty_details = response.css(".best-fdetail")
        faculty_info = {}
        for i, faculty in enumerate(faculty_details[:3]):
            faculty_info[f"faculty_{i+1}_name"] = faculty.css('h4::text').get(default='').strip()
            faculty_info[f"faculty_{i+1}_designation"] = faculty.css('p::text').get(default='').strip()
            faculty_info[f"faculty_{i+1}_description"] = faculty.css('a.showFacultyDescription::attr(data-description)').get(default='').strip()

        item.update(faculty_info)
        item['institute_name'] = response.css(".plc-institute h4::text").get(default='').strip()

        # Extract fee information
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























# import scrapy
# from ..items import TalentedgeScraperItem

# class CoursesSpider(scrapy.Spider):
#     name = 'courses'
#     allowed_domains = ['talentedge.com']
#     start_urls = [
#         "https://talentedge.com/golden-gate-university/doctor-of-business-administration",
#         "https://talentedge.com/iim-kozhikode/professional-certificate-programme-in-hr-management-and-analytics",
#         "https://talentedge.com/ecornell/certificate-course-data-analytics-360",
#         "https://talentedge.com/ecornell/certificate-course-strategic-human-resources-leadership",
#         "https://talentedge.com/ecornell/certificate-course-executive-leadership",
#         "https://talentedge.com/ecornell/certificate-course-digital-transformation",
#         "https://talentedge.com/ecornell/certificate-course-human-resources-management",
#         "https://talentedge.com/ecornell/certificate-course-technology-leadership",
#         "https://talentedge.com/opjindal-global-business-school/masters-of-business-administration-opj-global-university",
#         "https://talentedge.com/esgci-school-of-management-paris/doctorate-of-business-administration-esgci"

#     ]

#     def parse(self, response):
#         item = TalentedgeScraperItem()
#         item['course_name'] = response.css("h1::text").get(default='').strip()
#         item['course_url'] = response.url
#         item['descriptions'] = response.css(".desc p::text").get(default='').strip()

#         # Extract duration information
#         first_li = response.xpath('//div[@class="duration-of-course"]/ul/li[1]')
#         if first_li:
#             # Extract all text and then strip
#             all_text = first_li.xpath('.//text()').getall()
#             item['duration'] = ''.join(all_text).strip()

#         # course start date
#         course_start_li = response.xpath('//div[@class="duration-of-course"]/ul/li[2]')
#         if course_start_li:
#             all_text = course_start_li.xpath('.//text()').getall()
#             item['start_date'] = ''.join(all_text).strip()


#         # Extract lists
#         what_you_will_learn_list = response.css(".pl-deeper-undstnd li::text").getall()
#         item['what_you_will_learn'] = [text.strip() for text in what_you_will_learn_list]
#         key_skills = response.css(".key-skills-sec li::text").getall()
#         item['skills'] = [text.strip() for text in key_skills]

#         # Extract target students and eligibility
#         item['target_students'] = response.css(".cs-content h4::text").get(default='').strip()
#         item['eligibility'] = response.css(".eligible-right-top-list p::text").get(default='').strip()

#         # Extract course content
#         sections = response.css(".tab-pane")
#         all_li_items = []
#         for section in sections:
#             li_items = section.css('ul li::text').getall()
#             all_li_items.extend(li_items)
#         item["content"] = [text.strip() for text in all_li_items]

#         # Extract faculty details
#         faculty_details = response.css(".best-fdetail")
#         faculty_info = {}
#         for i, faculty in enumerate(faculty_details[:3]):
#             faculty_info[f"faculty_{i+1}_name"] = faculty.css('h4::text').get(default='').strip()
#             faculty_info[f"faculty_{i+1}_designation"] = faculty.css('p::text').get(default='').strip()
#             faculty_info[f"faculty_{i+1}_description"] = faculty.css('a.showFacultyDescription::attr(data-description)').get(default='').strip()

#         item.update(faculty_info)
#         item['institute_name'] = response.css(".plc-institute h4::text").get(default='').strip()

#         # Extract fee information
#         first_div = response.css('div.program-details-total-pay-amt-right')[0]
#         fee_in_INR = first_div.xpath('./text()').get(default='').strip()
#         item['fee_in_INR'] = fee_in_INR
      
#         divs_1 = response.css('div.program-details-total-pay-amt-right')
#         if len(divs_1) > 1:
#             second_div = divs_1[1]
#             second_div_text = second_div.xpath('.//text()').getall()
#             # Join all text nodes and strip whitespace
#             fee_in_USD = ''.join(second_div_text).strip()
#             item['fee_in_USD'] = fee_in_USD
#         else:
#             item['fee_in_USD'] = ''

#         yield item





    #    page = response.url
    #    filename= f"course.html"
    #    coursedetail={}
    #    self.log("saved file")
    #    cards = response.css(".p-collage-name")
    #    print(cards)
    #    for card in cards:
    #       title = card.css("h1::text").get()
    #       print(title)


    #       title = card.css(".pc-name h5::text").get()
    #       print(title)

       
    #     cards = response.css(".duration-of-course")
    #    print(cards)
    #    for card in cards:
    #       duration = card.css("p::text").get()
    #       print(duration)
    # #       title = card.css(".pc-name h5::text").get()
    # #       print(title)
       
    
         
       
        
        
        
        
        # page = response.url
        # filename= f"course.html"
        # Path(filename).write_bytes(response.body)
        # self.log("saved file")
        
        
        
        # for course in courses[:10]:  #() Limit to 10 courses
        #     course_link = response.urljoin(course.css('a::attr(href)').get())
        #     yield response.follow(course_link, callback=self.parse_course_details)












    #     # Handle pagination if needed
    #     next_page = response.css('a.next-page::attr(href)').get()
    #     if next_page:
    #         yield response.follow(next_page, self.parse)

    # def parse_course_details(self, response):
    #     # Extract detailed information from the course page
    #     yield {
    #         'Course Link': response.url,
    #         'Title': response.css('h3>a.courses-name::text').get(default='').strip(),
    #         'Description': response.css('div.course-description::text').get(default='').strip(),
    #         'Duration': response.css('div.course-duration::text').get(default='').strip(),
    #         'Timing': response.css('div.course-timing::text').get(default='').strip(),
    #         'Course Start Date': response.css('div.course-start-date::text').get(default='').strip(),
    #         'What you will learn': response.css('div.what-you-will-learn::text').get(default='').strip(),
    #         'Skills': response.css('div.skills::text').get(default='').strip(),
    #         'Target Students': response.css('div.target-students::text').get(default='').strip(),
    #         'Prerequisites / Eligibility criteria': response.css('div.prerequisites::text').get(default='').strip(),
    #         'Content': response.css('div.course-content::text').get(default='').strip(),
    #         'Faculty 1 Name': response.css('div.faculty-1-name::text').get(default='').strip(),
    #         'Faculty 1 Designation': response.css('div.faculty-1-designation::text').get(default='').strip(),
    #         'Faculty 1 Description': response.css('div.faculty-1-description::text').get(default='').strip(),
    #         'Faculty 2 Name': response.css('div.faculty-2-name::text').get(default='').strip(),
    #         'Faculty 2 Designation': response.css('div.faculty-2-designation::text').get(default='').strip(),
    #         'Faculty 2 Description': response.css('div.faculty-2-description::text').get(default='').strip(),
    #         'Institute Name': response.css('div.institute-name::text').get(default='').strip(),
    #         'Fee in INR': response.css('div.fee-inr::text').get(default='').strip(),
    #         'Fee in USD': response.css('div.fee-usd::text').get(default='').strip(),
    #     }
