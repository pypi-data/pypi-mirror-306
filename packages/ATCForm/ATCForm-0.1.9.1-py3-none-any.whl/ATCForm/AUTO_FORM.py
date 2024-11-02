import time
import re
from ping3 import ping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from utils import download_driver,redirect_stdout,restore_stdout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AUTO_JSJ_FORM:

    
    def __init__(self,url : str ):
        options = webdriver.EdgeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--guest")
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        
        self.info_data={}
        self.select_list=[]
        self.wait_time :str 
        self.answer_list=[]
        
        try:
            self.driver=webdriver.Edge(options)
        except:
            folder_path=download_driver()
            self.driver=webdriver.Edge(options,executable_path=folder_path) 
        self.actions = ActionChains(self.driver)
        try:
            self.driver.get(url)
        except:
            print("打开网页失败")
    
    
    
    def set_base_data(self,data_path_or_data :str | dict):
        if isinstance(data_path_or_data,dict): 
            self.info_data=data_path_or_data
            return
        else:
            with open(data_path_or_data,"r",encoding="utf-8") as f:
                data=f.read()
                data=data.replace("，",",").replace("：",":")
                self.info_data=eval(data)
            
    
    def init_the_select_answer_list(self):
        while(1):
            option=input("请输入你需要的勾选的选项(每个选项以空格分隔开 输入exit：退出)：")
            if(option=="exit"):
                return
            self.select_list.append(option)        
    
    
    def print_all_qus(self):
        print("----问题列表----")
        elements=self.driver.find_elements(By.CSS_SELECTOR, ".ant-col.field-container.field")
        for element in elements:
            class_names = element.get_attribute("class")
            if "MobileField" not in class_names:
                print(element.text.replace("\n","").replace("*",""))
        print("-----------------------------")
        return elements
        

    def is_submit(self):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '提交成功')]")
            return True    
        except:
            return False
    
    def is_collect(self):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '已暂停收集')]")
            return False    
        except:
            return True
    
    
      
    
    
    
    def get_questions_input(self):
        print("----input列表----")
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".ant-col.field-container.field")
        filtered_elements = []
        for element in elements:
            # 检查元素的 class 名称
            class_names = element.get_attribute("class")
            if "MobileField" in class_names:
                print(element.text.replace("\n", "").replace("*", ""))
                filtered_elements.append(element)
            elif "NameField" in class_names:
                print(element.text.replace("\n", "").replace("*", ""))
                filtered_elements.append(element)
            elif "TextField" in class_names:
                print(element.text.replace("\n", "").replace("*", ""))
                filtered_elements.append(element)
        return filtered_elements
    
    
    
    def get_questions_select(self):
        print("----select列表----")
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".ant-col.field-container.field") #ant-col.field-container.field SectionBreak
        filtered_elements = []
        for element in elements:
            class_names = element.get_attribute("class")
            if "MobileField" in class_names:
                pass
            elif "NameField" in class_names: 
                pass
            elif "TextField" in class_names:
                pass
            elif "SectionBreak" in class_names:
                pass
            else:
                print(element.text.replace("\n", "").replace("*", ""))
                filtered_elements.append(element)
        return filtered_elements
    
    
    def set_wait_time(self,input_time : str |None=""):
        if(input_time==""):
            input_time=input("请输入等待时间：")
        while(1):
            if(len(input_time)!=12):
                print("请输入正确的开抢时间")
                input_time=input("请输入等待时间：")
            else:
                break
        self.wait_time=input_time
        

    def wait_for_time(self,input_time : str |None=""): 
        """
        等待开抢
        :param input_time: 请输入正确的时间格式，例如：202405101328"
        :return: True
        """
        if(input_time=="" and self.wait_time=="" ):
            input_time=input("请输入等待时间：")
        elif(input_time=="" and self.wait_time!=""):
            input_time=self.wait_time
        
        try:
            time_tuple = time.strptime(input_time, "%Y%m%d%H%M")
            start_timestamp  = time.mktime(time_tuple)
            if(start_timestamp<time.time()):
                print("收集表已经开始")
                self.refreshdom()
                return 
            
            cnt=0
            while(1):
          
                current_timestamp = time.time()
                if(current_timestamp >= (start_timestamp-self.ping_time/1.2)):
                    self.refreshdom()
                    return
                          
                
                if(cnt%200000==0):
                    current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_timestamp))
                    print("正在等待当前时间为",current_time_str)
                cnt+=1

        except ValueError:
            print("输入时间格式不正确，请输入正确的时间格式，例如：202405101328") 
        
       
            
    def Initializes_the_answer_list(self):
        elements=self.get_questions_input()
        for element in elements:
            question=element.text.replace("\n","").replace(" ","")
            flag=0
            for item_key in self.info_data:
                if(re.search(item_key,question)):
                    self.answer_list.append(self.info_data[item_key])
                    print("依据初始数据输入",question,"data：",self.info_data[item_key])
                    flag=1
                    continue
            if(flag==1):
                continue    
            value=input("请输入简答题 "+question+":")
            self.answer_list.append(value)    
        print("-----------------------------")        
    




    def auto_input(self):
        """自动输入值到具有指定名称的输入框中。

        Args:
            INPUT_NAME (str): 输入框的名称
            val (str): 要输入的值
        """
        try: 
            print("----自动输入-----")
            elements=self.get_questions_input()
            index=0
            for element in elements:
                input_element=element.find_element(By.CSS_SELECTOR, "input")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
                input_element.send_keys(self.answer_list[index])
                input_element.submit()
                index+=1
        except:
            print("填写失败")
            exit()

    def auto_button(self):
        print("----自动选择-----")
        for item in self.select_list:
            buttons = self.driver.find_elements(By.XPATH, f"//span[text()='{item}']")
            print(buttons)
            for button in buttons:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # self.actions.click(button).perform()
                button.click()
            # buttons.click()

    def auto_submit(self):
        print("----自动提交-----")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
        button = self.driver.find_element(By.CSS_SELECTOR,".ant-btn.ant-btn-primary.ant-btn-two-chinese-chars.form-theme--submit-button.published-form__submit.FooterButton_button__vJkWw")
        button.click()
        try:
            print("动作已经全部执行")
            time.sleep(1)
            if(self.is_submit()):
                print("成功抢到")
            else:
                print("没有抢到")
                
        except Exception as e:
            print(e)
            

    def __del__(self):
        self.driver.quit()



class AUTO_TX_FORM:
    def __init__(self,url : str ):
        options = webdriver.EdgeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--guest")
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])   
        self.info_data={}
        self.select_list=[]
        self.wait_time :str 
        self.answer_list=[]
    
        
        try:
            self.driver=webdriver.Edge(options)
        except:
            folder_path=download_driver()
            self.driver=webdriver.Edge(options,executable_path=folder_path) 
            
        self.actions = ActionChains(self.driver)
        
        try:
            self.driver.get(url)
        except:
            print("打开网页失败")
            
        self.set_ping_time()

        
 


    #判断系列
    def is_login(self):
        """
        根据页面是否有"登录后才能填写"文本判断是否登录
        返回True或False
        """
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '登录后才能填写')]")
            return False
        except:
            return True
    
    def is_submit(self):
        """
        根据页面是否有"登录后才能填写"文本判断是否登录
        返回True或False
        """
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '已提交')]")))
            return True    
        except:
            return False

    def is_collect(self):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '已暂停收集')]")
            return False    
        except:
            return True
    
    def is_start(self):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '收集暂未开始')]")
            return False    
        except:
            return  True

    
    #设置自动化内容
    def set_ping_time(self):
        sum=0
        for _ in range(1):
            sum+=ping('docs.qq.com')
        self.ping_time=sum

    def set_elements(self):
        self.input_elements=self.get_questions_input()
        self.select_elements=self.get_questions_select()

    def set_base_data(self,data_path_or_data :str | dict):
        if isinstance(data_path_or_data,dict): 
            self.info_data=data_path_or_data
            return
        else:
            with open(data_path_or_data,"r",encoding="utf-8") as f:
                data=f.read()
                data=data.replace("，",",").replace("：",":")
                self.info_data=eval(data) 
            
    

    
    
    
    def print_all_qus(self):
        print("------------------------------问题列表------------------------------")
        elements=self.driver.find_elements(By.CSS_SELECTOR, ".question")
        for element in elements:
            value=element.text.replace("\n"," ").replace("*","")
            print(value)
        return elements
        
    

    def wait_for_login(self):
        if(self.is_login==True):
            return
        else:
            # os.system("cls")
            input("请登录后按回车键继续...")
            self.refreshdom()
            
    def set_wait_time(self,input_time : str |None=""):
        if(input_time==""):
            input_time=input("请输入等待时间：")
        while(1):
            if(len(input_time)!=12):
                print("请输入正确的开抢时间")
                input_time=input("请输入等待时间：")
            else:
                break
        self.wait_time=input_time
        
    
    def wait_for_time(self,input_time : str |None=""): 
        """
        等待开抢
        :param input_time: 请输入正确的时间格式，例如：202405101328"
        :return: True
        """
        if(input_time=="" and self.wait_time=="" ):
            input_time=input("请输入等待时间：")
        elif(input_time=="" and self.wait_time!=""):
            input_time=self.wait_time
        
        try:
            time_tuple = time.strptime(input_time, "%Y%m%d%H%M")
            start_timestamp  = time.mktime(time_tuple)
            if(start_timestamp<time.time()):
                print("收集表已经开始")
                self.refreshdom()
                return 
            
            cnt=0
            while(1):
          
                current_timestamp = time.time()
                if(current_timestamp >= (start_timestamp-self.ping_time/1.2)):
                    self.refreshdom()
                    return
                          
                
                if(cnt%200000==0):
                    current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_timestamp))
                    print("正在等待当前时间为",current_time_str)
                cnt+=1

        except ValueError:
            print("输入时间格式不正确，请输入正确的时间格式，例如：202405101328") 
        
           
    
    
    
    def get_questions_input(self):
        """
        Args:
            driver (webdriver): selenium的webdriver
        Returns:
        elements
        """
        # print("------------------------------输入列表------------------------------")
        elements=self.driver.find_elements(By.XPATH, "//*[contains(@class, 'question') and  @data-type='simple']")  
        return elements
    
    
    
    def get_questions_select(self):
        """
        Returns:
        elements
        """
        elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'question') and (contains(@data-type, 'radio') or contains(@data-type, 'checkbox'))]")
        return elements
    
    
    def init_the_select_answer_list(self):
        elements=self.select_elements
        for element in elements:
            value=element.text.replace("\n"," ").replace("*","")
            option = input(f"请输入问题 {value} 你需要的勾选的选项(每个选项以空格分隔开 输入exit：退出)：")
            if option.lower() == "exit":
                exit()
            options_list = option.split()
            self.select_list.append(options_list)
            print("用户选择的选项列表：", options_list)        
    
        

    def init_the_input_answer_list(self):
        print("------------------------------初始化答案列表------------------------------")
        elements=self.input_elements
        for element in elements:
            question=element.text.replace("\n","").replace(" ","")
            flag=0
            for item_key in self.info_data:
                if(re.search(item_key,question)):
                    self.answer_list.append(self.info_data[item_key])
                    print("**依据初始数据输入** ：",question,"data：",self.info_data[item_key])
                    flag=1
                    continue
            if(flag==1):
                continue    
            value=input("请输入简答题 "+question+":")
            self.answer_list.append(value)    
         
    
    def auto_input(self):
        """
        自动输入值到具有指定名称的输入框中。
        """
        try: 
            blank_area = self.driver.find_element(By.XPATH, "//div[contains(@class,'form-header-title-content')]")
            # print("------------------------------自动输入------------------------------")
            # index=0
            elements=self.input_elements
            for element,answer in zip(elements,self.answer_list):
                data_qid=element.get_attribute("data-qid")
                textarea = self.driver.find_element(By.CSS_SELECTOR, f'[data-qid="{data_qid}"]  textarea')
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", textarea)
                textarea.send_keys(answer)
                self.actions.move_to_element(blank_area).click().perform()
                # index+=1
            
            
            # print("输入成功",self.answer_list)
            
        except Exception as e:
            print("填写失败",e)
    

    def auto_button(self):
        try: 
            # print("------------------------------自动点击------------------------------")
            # elements = self.get_questions_select()
            elements=self.select_elements
            index=0
            for element in elements:
                for a in self.select_list[index]:
                    button = element.find_element(By.XPATH, f"//span[contains(text(), '{a}') and (contains(@class, 'form-choice-option-text-content form-choice-checkbox-option-text-content') or contains(@class, 'form-choice-option-text-content form-choice-radio-option-text-content') )]")  # 使用"."表示在当前元素下搜索
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    button.click()
                    
                index+=1
        except Exception as e:
            print("填写失败",e)
        
        


    def auto_submit(self):
        blank_area = self.driver.find_element(By.CLASS_NAME, "form-header-title-content")
        self.actions.move_to_element(blank_area).click().perform()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
        button=self.driver.find_element(By.XPATH,"//button[contains(text(), '提交')]")
        button.click()
        
        try:
            # 等待直到指定元素出现，最多等待10秒
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,"//button[contains(@class, 'dui-button dui-modal-footer-ok dui-button-type-primary dui-button-size-default')]"))
            )
            submit_button.click()
            return
            
        except Exception as e:
            print("提交失败",e)
            return 
            

    
    def refreshdom(self):
        self.driver.refresh()
        WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), '提交') or contains(text(), '收集暂未开始')]"))
            )
        
                
            
    def __del__(self):
        self.driver.quit()










        
        


        





        
        
               