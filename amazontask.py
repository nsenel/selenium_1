#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      numan
#
# Created:     01.04.2017
# Copyright:   (c) numan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
def setup():
    print "Programin calismasi icin Selenium version 2.53.4, Python 2.7.x ve Chrome web driver gerekmektedir."
    driver = webdriver.Chrome()
    return driver

def load_page_and_login(driver):
    driver.get("https://www.amazon.com")
    #Site acilana kadar bekler belirlenen surede acilmazsa programi sonlandirir
    try:
        element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "nav-link-accountList"))
        )
        print "Amazon.com sayfasina giris basarili"
    except TimeoutException:
        print "Beklenen Surede Sayfa Yuklenemedi Interneti Baglantinizi Kontrol Edin"
        driver.quit()
        return None
    #Uye girisi sayfasina gecme ve formu doldurma
    driver.find_element_by_id("nav-link-accountList").click()
    username = driver.find_element_by_name('email')
    username.send_keys('testsele115@gmail.com')
    password = driver.find_element_by_name('password')
    password.send_keys('1testsele1')
    driver.find_element_by_id("signInSubmit").click()
    print "Uye girisi basarili olarak gerceklesti"


def search_item(driver,urun,sayfa,SirasindakiUrun):
    #search box ile iletisime gecer aranmak icin girisi yapilan urunu yazar ve enter a basar
    search = driver.find_element_by_name('field-keywords')
    search.send_keys(urun)
    search.send_keys(Keys.ENTER)

    # Aramanin gerceklestigini kontrol icin..

    if str(driver.title) == "Amazon.com: {0}".format(urun):
        print "Amazon.com'da '{}' Aramasi Basarili Islem Gerceklestirildi.".format(urun)
    else :
        print "Beklenen Surede Sayfa Yuklenemedi Interneti Baglantinizi Kontrol Edin"
        driver.quit()
        return None
    #Birinci sayfadan ikinci sayfaya gecisi kontrol eder
    try:
        element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "{}".format(sayfa)))
        )
        print "%d. sayfaya giris basarili" %sayfa
    except TimeoutException:
        print "Beklenen Surede Sayfa Yuklenemedi Interneti Baglantinizi Kontrol Edin"
        driver.quit()
        return None
    #ikinci sayfaya gecisi saglar
    driver.find_element_by_link_text('{}'.format(sayfa)).click()

    #ikinci sayfadaki 3. urunu secer
    UcuncuUrun=driver.find_elements_by_css_selector(".s-result-item.celwidget")[SirasindakiUrun-1]
    #Urunun unique item numarasini alir hem dogru urunu favariye eklenmesini saglar hemde favari listesinde urunun varligini kontrol eder.
    item=UcuncuUrun.get_attribute("data-asin")

    #Urunun gercek ismine ulasmamizi saglar
    itemname="Bulunamadi"
    try:
        itemname=driver.find_element_by_xpath("//*[@id='{}']/div/div/div/div[2]/div[1]/div[1]/a/h2".format(UcuncuUrun.get_attribute("id")))
        itemname= (itemname.get_attribute("data-attribute"))
    except:
        pass

    #yuklenme hatasi ihtimaline karsi..
    try:
        driver.find_element_by_css_selector("a[href*='%s']"%item).click()
    except:
        try:
            time.sleep(10)
            driver.find_element_by_css_selector("a[href*='%s']"%item).click()
        except:
            print "beklenmeyen hata olustu lutfen tekrar deneyin"
            driver.quit()

    #fonksiyon secilen urune tiklanarak sonlandirilir ve bu fonksiyondan unique item numarasi ve urunun gercek ismi elde edilmis olur
    return item,itemname


def favorite_item_list_operation(driver,item,itemname):
    #urun favori listesine eklenir.
    driver.find_element_by_id("wishlistButtonStack").click()
    time.sleep(2)
    #favori liste acilir
    driver.find_element_by_link_text("Wish List").click();
    time.sleep(1)
    #Favori listenin icinde birden fazla urun olabilir bu yuzden donguye alinir
    a=driver.find_elements_by_name("submit.deleteItem")
    for i in a:
        try:
            b=i.get_attribute("data-reg-item-delete").encode('utf-8')
            #unique item numarasi favori urunler icinde aranir bulunursa bulundugu belirtir ve urun ismini yazar daha sonra urunu listeden cikarir
            if item in b:
                i.click()
                print "Favori Listenizin Icinde Aramada Eklediginiz Urun Bulundu : %s " %itemname
                return "Basarili Olarak Favari Listesinden Kaldirildi ItemNO:%s " %item
        #urun bir sekilde bulunamazsa hata hakkinda bilgi verir.
        except:
            pass
        return "Belirtilen Urun Favori Listesinde Olmayabilir veya Urun Kodu Degismistir Manuel Olarak Silebilirsiniz"


def main():
    #secilecek_list 'e  farkli urunler girilerek arama sartlari degistirilebilir veya birden fazla urun icin islem gerceklestirile bilir.
    #secilecek_list=[["samsung",2,3],["apple",2,4]]
    secilecek_list=[["samsung",2,3]]
    for urun,sayfa,secilecekurun in secilecek_list:
        driver=setup()
        if driver != None:
            load_page_and_login(driver)
            item,itemname=search_item(driver,urun,sayfa,secilecekurun)
            if item != None:
                print(favorite_item_list_operation(driver,item,itemname))
                time.sleep(5)
                driver.quit()
                print "Program Basariyla Sonlandirildi."

if __name__ == '__main__':
    main()
