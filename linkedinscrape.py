from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import xlsxwriter


driver = webdriver.Chrome(executable_path=r'C:\Users\gkhat\Documents\chromedriver.exe')


def linkedin_login():
    try:
        driver.get('https://www.linkedin.com/login')

        username = 'username'
        password = 'password'

        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'username'))).send_keys(username)
        time.sleep(3)
        driver.find_element_by_id('password').send_keys(password)
        time.sleep(3)
        driver.find_element_by_class_name('btn__primary--large.from__button--floating').click()
        time.sleep(8)
    except ImportError:
        print('Closing')


linkedin_login()

post_text = []
post_like = []
post_comment = []
media_links = []
media_type = []

def profile():
    url = "https://www.linkedin.com/in/andrewyng/detail/recent-activity/shares/"
    driver.get(url)
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    posts = driver.find_elements_by_class_name('occludable-update.ember-view')
    for post in posts:
        try:

            caption = post.find_element_by_class_name('break-words').text
            caption = caption.strip('')
            post_text.append(caption)
            likes = post.find_element_by_class_name('v-align-middle.social-details-social-counts__reactions-count').text
            post_like.append(likes)

            time.sleep(3)

            comments = post.find_element_by_class_name('social-details-social-counts__comments.social-details-social-counts__item ').text
            post_comment.append(comments)

            time.sleep(3)

            try:
                video_tag = post.find_element_by_class_name('vjs-tech')
                video_link = video_tag.get_attribute('src')
                media_links.append(video_link)
                media_type.append("Video")
            except:
                try:
                    img_tag = post.find_element_by_xpath('.//img[contains(@class,"image__image")]')
                    img_link = img_tag.get_attribute("src")
                    media_links.append(img_link)
                    media_type.append("Image")
                except:
                    try:
                            article_tag = post.find_element_by_class_name('app-aware-link.feed-shared-article__image-link.tap-target')
                            article_link = article_tag.get_attribute('href')
                            media_links.append(article_link)
                            media_type.append('Article')
                    except:
                        try:
                            yt_video = post.find_element_by_class_name('app-aware-link.tap-target.block.flex-grow-1')
                            yt_link = yt_video.get_attribute('href')
                            media_links.append(yt_link)
                            media_type.append('Youtube Video')
                        except:
                            media_links.append("None")
                            media_type.append("Unknown")
        except:
            pass

profile()
data = {
    "Media Type": media_type,
    "Post Text": post_text,
    "Post Likes": post_like,
    "Post Comments": post_comment,
    "Media Links": media_links
}

df = pd.DataFrame(data)
print(df.head(30))

# df.to_csv("posts.csv", encoding='utf-8', index=False)

writer = pd.ExcelWriter("posts.xlsx", engine='xlsxwriter')
df.to_excel(writer, index =False)
writer.save()
