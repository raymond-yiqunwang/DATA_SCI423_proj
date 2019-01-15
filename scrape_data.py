## /home/raymond/.conda/envs/scrape/bin/python
## Author: Raymond Wang <raymondwang@u.northwestern.edu>
## Challenge project from Citrine Informatics

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from xvfbwrapper import Xvfb
import pandas as pd
import numpy as np
import time
import sys

# setting virtual display, comment these lines for visualization
display = Xvfb()
display.start()

# navigate to target website
driver = webdriver.Chrome()
driver.get("http://www.matweb.com/search/CompositionSearch.aspx")

# unfold "Ferrous Metal"
driver.find_element_by_id("ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewn1").click()
time.sleep(1) # wait for the browser

# choose "Alloy Steel"
driver.find_element_by_id("ctl00_ContentMain_ucMatGroupTree_LODCS1_msTreeViewt6").click()
time.sleep(1)

# choose composition1: Mn
select_fe = Select(driver.find_element_by_id("ctl00_ContentMain_ucPropertyDropdown1_drpPropertyList"))
select_fe.select_by_visible_text("Manganese, Mn")
driver.find_element_by_id("ctl00_ContentMain_ucPropertyEdit1_txtpMin").send_keys("0.0")
time.sleep(1)

# choose composition2: Cr
select_cr = Select(driver.find_element_by_id("ctl00_ContentMain_ucPropertyDropdown2_drpPropertyList"))
select_cr.select_by_visible_text("Chromium, Cr")
driver.find_element_by_id("ctl00_ContentMain_ucPropertyEdit2_txtpMin").send_keys("0.0")
time.sleep(1)

# choose composition3: Ni
select_ni = Select(driver.find_element_by_id("ctl00_ContentMain_ucPropertyDropdown3_drpPropertyList"))
select_ni.select_by_visible_text("Nickel, Ni")
driver.find_element_by_id("ctl00_ContentMain_ucPropertyEdit3_txtpMin").send_keys("0.0")
time.sleep(1)

# lauching search
driver.find_element_by_id("ctl00_ContentMain_btnSubmit").click()
time.sleep(2)

# show 200 per page
instance_per_page = 200
Select(driver.find_element_by_id("ctl00_ContentMain_UcSearchResults1_drpPageSize1")).select_by_visible_text(str(instance_per_page))
time.sleep(2)

file_names = []

# loop over 5 pages of results to collect data
for ipage in range(5):
    print("currently on page " + str(ipage+1))
    sys.stdout.flush()

    # save name of datasets to a list before processing, may not be ideal design but avoids stale element problems
    name_list = []
    for item in driver.find_elements_by_xpath("//td[@style='width:auto; font-weight:bold;']"):
        name_list.append(item.text)
    
    for name in name_list:
        print('  processing: \"' + name + '\"')
        sys.stdout.flush()
        
        # open file
        fname = name
        if len(fname) > 240: fname = fname[:240] # in case length of file name exceeds Linux limit
        f = open("data/" + fname + ".csv", 'w')
        file_names.append(fname)
        
        # navigate into each alloy page
        driver.find_element_by_link_text(name).click()
        time.sleep(2)
        table = driver.find_element_by_xpath("//table[@class='tabledataformat']")
        attrib = []
        for row in table.find_elements_by_xpath("//tr[@class='altrow datarowSeparator']"):
            attrib.append([d.text for d in row.find_elements_by_css_selector('td')])
            time.sleep(0.1)
        for row in table.find_elements_by_xpath("//tr[@class=' datarowSeparator']"):
            attrib.append([d.text for d in row.find_elements_by_css_selector('td')])
            time.sleep(0.1)
        attrib = np.array(attrib)
        
        # write to file
        df = pd.DataFrame(data=attrib[:, 1:], columns=['Metric', 'English', 'Comments'], index=attrib[:, 0] )
        df.to_csv(f)
        f.close()
        driver.back()
        time.sleep(2)

    # navidate to the next page
    driver.find_element_by_id("ctl00_ContentMain_UcSearchResults1_lnkNextPage").click()
    time.sleep(3)

# store file names
dfname = pd.DataFrame(file_names, dtype=str)
dfname.to_csv("data/filenames.csv", header=False, index=False)
driver.quit()

# virtual display off
display.stop()
