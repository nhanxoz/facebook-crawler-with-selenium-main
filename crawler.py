"""Website crawler for facebook pages"""
"""/*https://m.facebook.com/alihtgnourt/photos*/"""
import selenium
from selenium.webdriver.common.by import By
import selenium.webdriver.remote.webelement as web_element
import time
import datetime
import json
import helper
from typing import Union
from selenium.webdriver.common.action_chains import ActionChains
Post = Union[str, dict, datetime.datetime]
Article = web_element.WebElement
Webdriver = selenium.webdriver.Firefox


def login(url: str, email: str, password: str) -> Webdriver:
    options = selenium.webdriver.FirefoxOptions()
    driver = selenium.webdriver.Firefox(options=options)
    driver.get(url)
    input_username = driver.find_element("id", "m_login_email")
    input_password = driver.find_element("id", "m_login_password")
    submit = driver.find_element("id", "login_password_step_element")
    input_username.send_keys(email)
    input_password.send_keys(password)
    submit.click()
    time.sleep(5)
    return driver


def processing_posts(article: Article, screenshot_path: str) -> dict[str, Post]:
    data: dict[str, Post] = {"description": article.text}

    # Find the element that contains information about the post
    data_ft = article.get_attribute("data-ft")
    if data_ft is None:
        return data
    post_data = json.loads(data_ft)
    data["data_ft"] = post_data

    # Post id
    post_id: str = post_data["mf_story_key"]
    data["post_id"] = post_id

    # Screenshot
    article.screenshot(screenshot_path + post_id + ".png")

    # Number of reaction
    footer = article.find_element(By.TAG_NAME, "footer")
    container_name = '[data-sigil="reactions-sentence-container"]'
    like_element = footer.find_element(By.CSS_SELECTOR, container_name)
    if like_element is not None:
        data["like"] = like_element.text if like_element else "0"

    # Publish_time
    if "page_insights" not in post_data:
        return data
    page_insights = post_data["page_insights"]
    for _, value in page_insights.items():
        if "post_context" in value:
            publish_time = value["post_context"]["publish_time"]
            data["publish_time"] = datetime.datetime.fromtimestamp(publish_time)

    return data


def save_posts(data: list[dict[str, Post]],
               filename: str,
               articles: list[Article],
               screenshot_path: str
               ) -> None:
    for article in articles:
        post = processing_posts(article, screenshot_path)
        data.append(post)
    helper.export_object(filename, data)


def crawl_url(driver: Webdriver,
              post_limit: int,
              target_url: str,
              screenshot_path: str,
              ) -> None:
    filename = target_url.split("/")[-1]
    data: list[dict[str, Post]] = []

    # Visit url
    driver.get(target_url)
    time.sleep(3)
    first_a_tag = driver.find_element(By.CSS_SELECTOR, ".item a.touchable.primary")

    first_a_tag.click()
    time.sleep(1)
    first_photo = driver.find_element(By.CSS_SELECTOR, "a._39pi._1mh-._4dvp")
    first_photo.click()
    modified_url = driver.current_url.replace("m.facebook.com", "www.facebook.com")
    driver.get(modified_url)
    time.sleep(3)
    for i in range(post_limit):
        i_element = driver.find_element(By.CSS_SELECTOR, "img.x85a59c.x193iq5w.x4fas0m.x19kjcj4")

        # Get the value of the "data-store" attribute
        src = i_element.get_attribute("src")

        # Parse the JSON data to extract the "imgsrc" attribute


        print("imgsrc:", src)
        print("Current URL: ", driver.current_url)
        matching_elements = driver.find_elements(By.CSS_SELECTOR, "i.x1b0d499.xep6ejk")
        
        actions = ActionChains(driver)
        actions.move_to_element(matching_elements[1]).perform()
        matching_elements[1].click()
        time.sleep(2)
    # while len(data) < post_limit:
    #     # Scroll to the end of the page
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #     # Wait for the page to finish loading
    #     time.sleep(3)

    #     # Retrieve posts

    #     # articles = driver.find_elements(By.CLASS_NAME, "story_body_container")
    #     # print("---------")
    #     # print(articles)
    #     # save_posts(data, filename, articles, screenshot_path)
    #     first_a_tag = driver.find_element(By.CSS_SELECTOR, ".item a.touchable.primary")

    #     first_a_tag.click()

    #     first_photo = driver.find_element(By.CSS_SELECTOR, "a._39pi._1mh-._4dvp")
    #     first_photo.click()