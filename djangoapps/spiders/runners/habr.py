import time
import os
import logging

from dateutil.parser import parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from django.core.management.base import BaseCommand
from django.conf import settings

from main.models import (
    Skill, AdvHabr, Company,
    WORK_TYPE_ANY, WORK_TYPE_PART, WORK_TYPE_FULL)

logger = logging.getLogger(__name__)


class GetAdvHabr():
    """
    Обновление данных с Хабр.Карьера
    """
    driver = None
    cities = []

    def getCities(self):
        cities = []
        path = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(path, 'cities.csv')
        with open(filename) as f:
            for line in f:
                cities.append(line.strip())
        return cities

    def run(self, *args, **options):
        chrome_options = Options()
        if not settings.LOCAL_RUN:
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument('--headless')

        self.cities = self.getCities()
        print ("settings.CHROMEDRIVER_PATH", settings.CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(settings.CHROMEDRIVER_PATH, chrome_options=chrome_options)
        try:
            for page in range(1, 20):
                site_url = f'https://career.habr.com/vacancies?page={page}&type=all'
                logger.info(f"Get list adv: {site_url}")
                self.driver.get(site_url)
                self.parseRequest()
        except Exception as e:
            logger.exception(f"{e}")
            logger.error(f"Exception: {e}")
        self.driver.quit()
        self.clean()

    def parseRequest(self):
        if not self.driver:
            return

        time.sleep(5)

        for searchResults in self.driver.find_elements_by_class_name('search-results'):
            skipThisAdv = False

            for listItem in searchResults.find_elements_by_class_name('card-list__item'):

                advHabrObj = None
                dt = None

                for cardDate in listItem.find_elements_by_class_name('vacancy-card__date'):
                    for img in cardDate.find_elements_by_css_selector('time'):
                        dt_raw = img.get_attribute('datetime')
                        dt = parse(dt_raw)

                for cardTitle in listItem.find_elements_by_class_name('vacancy-card__title'):
                    for a in cardTitle.find_elements_by_css_selector('a'):
                        url = a.get_attribute('href')
                        title = a.text
                        advHabrObj = AdvHabr.objects.filter(url=url).first()
                        if advHabrObj:
                            skipThisAdv = True
                            if advHabrObj.last_update is None or \
                                    advHabrObj.last_update.strftime('%Y-%m-%d') != dt.strftime('%Y-%m-%d'):
                                advHabrObj.last_update = dt
                                history_update = advHabrObj.history_update
                                if dt_raw not in history_update:
                                    history_update.append(dt_raw)
                                    advHabrObj.history_update = history_update
                                    advHabrObj.save()
                        else:
                            skipThisAdv = False
                            advHabrObj = AdvHabr.objects.create(
                                title=title,
                                url=url,
                                last_update=dt,
                                history_update=[dt_raw])
                            logger.info(f"Created new adv: {advHabrObj.id}")

                if skipThisAdv is False:
                    self.getSalaryFromListItem(listItem, advHabrObj)
                    self.getSkillsFromListItem(listItem, advHabrObj)
                    self.getMetaFromListItem(listItem, advHabrObj)

                    self.getAdvData(url, advHabrObj)

    def getSalaryFromListItem(self, listItem, advHabrObj):
        for salary in listItem.find_elements_by_class_name('basic-salary'):
            s = salary.text
            if not advHabrObj.salary or advHabrObj.salary != s:
                advHabrObj.salary = s
                advHabrObj.save()

    def getSkillsFromListItem(self, listItem, advHabrObj):
        for skills in listItem.find_elements_by_class_name('vacancy-card__skills'):
            for comp in skills.find_elements_by_class_name('link-comp'):
                skill = comp.text
                skillObj, created = Skill.objects.get_or_create(title=skill)
                if not advHabrObj.skills.filter(pk=skillObj.pk):
                    advHabrObj.skills.add(skillObj)
                    advHabrObj.save()

    def getMetaFromListItem(self, listItem, advHabrObj):
        for cardTitle in listItem.find_elements_by_class_name('vacancy-card__meta'):
            for pl in cardTitle.find_elements_by_class_name('preserve-line'):
                for span in pl.find_elements_by_css_selector('span'):
                    text = span.text
                    if text == u'Любой':
                        if advHabrObj.work_type != WORK_TYPE_ANY:
                            advHabrObj.work_type = WORK_TYPE_ANY
                            advHabrObj.save()
                    if text == u'Полный рабочий день':
                        if advHabrObj.work_type != WORK_TYPE_FULL:
                            advHabrObj.work_type = WORK_TYPE_FULL
                            advHabrObj.save()
                    if text == u'Неполный рабочий день':
                        if advHabrObj.work_type != WORK_TYPE_PART:
                            advHabrObj.work_type = WORK_TYPE_PART
                            advHabrObj.save()
                    if text == u'Можно удалённо':
                        if advHabrObj.remote is not True:
                            advHabrObj.remote = True
                            advHabrObj.save()
                    if text in self.cities:
                        if advHabrObj.city != text:
                            advHabrObj.city = text
                            advHabrObj.save()

    def getAdvData(self, url, advHabrObj):
        logger.info(f"Get selected url: {url}")
        chrome_options = Options()
        if not settings.LOCAL_RUN:
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(settings.CHROMEDRIVER_PATH, chrome_options=chrome_options)
        driver.get(url)

        time.sleep(3)
        companyObj = None
        count = 0
        for companyInfo in driver.find_elements_by_class_name('company_info'):
            for companyName in companyInfo.find_elements_by_class_name('company_name'):
                if count == 0:
                    for a in companyName.find_elements_by_css_selector('a'):
                        companyTitle = a.text
                        companyUrl = a.get_attribute('href')
                        companyObj, created = Company.objects.get_or_create(title=companyTitle)
                        if created:
                            companyObj.url = companyUrl
                            companyObj.save()

                        advHabrObj.company = companyObj
                        advHabrObj.save()
                count += 1

        if companyObj:
            for companyInfo in driver.find_elements_by_class_name('company_info'):
                for a in companyInfo.find_elements_by_css_selector('a'):
                    for img in a.find_elements_by_css_selector('img'):
                        imgSrc = img.get_attribute('src')
                        if companyObj and not companyObj.logo:
                            companyObj.logo = imgSrc
                            companyObj.save()

            for companyAbout in driver.find_elements_by_class_name('company_about'):
                if companyObj and not companyObj.about:
                    companyObj.about = companyAbout.text
                    companyObj.save()

            for companySite in driver.find_elements_by_class_name('company_site'):
                for a in companySite.find_elements_by_css_selector('a'):
                    if companyObj and not companyObj.url:
                        companyObj.url = a.get_attribute('href')
                        companyObj.save()

        for descriptionBody in driver.find_elements_by_class_name('job_show_description__vacancy_description'):
            for sanitize in descriptionBody.find_elements_by_class_name('sanitize-ugc'):
                if advHabrObj and not advHabrObj.description:
                    advHabrObj.description = sanitize.text
                    advHabrObj.save()

        driver.quit()

    def clean(self):
        try:
            os.system(
                "export pid=`ps aux | grep {} | awk 'NR==1{print $2}' | cut -d' ' -f1`;kill -9 $pid".format(
                    "chromium"))
            os.system(
                "export pid=`ps aux | grep {} | awk 'NR==1{print $2}' | cut -d' ' -f1`;kill -9 $pid".format(
                    "chromedriver"))
            os.system(
                "export pid=`ps aux | grep {} | awk 'NR==1{print $2}' | cut -d' ' -f1`;kill -9 $pid".format(
                    "xvfb"))
        except Exception:
            pass