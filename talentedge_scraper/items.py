# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TalentedgeScraperItem(scrapy.Item):
    course_name = scrapy.Field()
    course_url = scrapy.Field()
    descriptions = scrapy.Field()
    duration = scrapy.Field()
    what_you_will_learn = scrapy.Field()
    skills = scrapy.Field()
    target_students =scrapy.Field()
    eligibility =scrapy.Field()
    content =scrapy.Field()
    faculty_1_name =scrapy.Field()
    faculty_1_designation =scrapy.Field()
    faculty_1_description =scrapy.Field()
    faculty_2_name =scrapy.Field()
    faculty_2_designation = scrapy.Field()
    faculty_2_description = scrapy.Field()
    faculty_3_name =scrapy.Field()
    faculty_3_designation = scrapy.Field()
    faculty_3_description = scrapy.Field()
    institute_name = scrapy.Field()
    fee_in_INR = scrapy.Field()
    fee_in_USD = scrapy.Field()
    start_date = scrapy.Field()


