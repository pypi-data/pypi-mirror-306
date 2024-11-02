from AUTO_FORM import *
from concurrent.futures import ThreadPoolExecutor
from utils import redirect_stdout,restore_stdout
from typing import List, Union

class AuTotask_TX:
    def __init__(self,url :str,data_path_or_data :str | dict,start_time,is_enable=True,SELECT_LIST=[]) -> None:
        """
        初始化函数，用于设置数据收集和处理的参数。

        参数：
        - url (str): 收集表单的URL地址。 \n
        - data_path_or_data: 数据文件的存储路径或直接提供的数据。\n
        - start_time (str): 开始时间，格式为YYYYMMDDHHMM，例如202405121200（注意月份和日期需要补零）。\n
        - is_enable (bool, optional): 是否启用预输入选择内容的功能，默认为True。\n
        - SELECT_LIST (list, optional): 需要选择的内容列表。格式为[["单选项A"],["单选项B"],["多选项A","多选项B"]]，必须严格按照这个格式提供。\n

        data.txt 文件格式要求（如果data_path_or_data是路径）：\n
        {
            "学号姓名": "value",
            "手机号": "value",
            "邮箱": "value",
            "班级": "value",
            "学院": "value",
            "name": "value"
        }
        
        注意：
        - 确保提供的时间格式正确，否则可能会影响数据收集的准确性。
        - data_path_or_data 参数可以是文件路径或直接的数据对象，根据实际情况选择。
        """
        self.url=url
        self.data_path_or_data=data_path_or_data
        self.start_time=start_time
        self.is_enable=is_enable
        if(is_enable==False):
            self.SELECT_LIST=SELECT_LIST
            
        


    def init(self):
        self.AT1=AUTO_TX_FORM(self.url)
        self.AT1.set_wait_time(input_time=self.start_time)
        if (self.AT1.is_collect==False):
            print("已经暂停收集，任务失败")
            return 
            
        
        
        self.AT1.wait_for_login()
        self.AT1.set_elements()
        self.AT1.set_base_data(self.data_path_or_data)
        if(self.is_enable==False):
            self.AT1.select_list=self.SELECT_LIST

            
        self.AT1.print_all_qus()
        self.AT1.init_the_input_answer_list()
        
        if(self.is_enable):
            self.AT1.init_the_select_answer_list()
            
                        
        current_timestamp = time.time()
        time_tuple = time.strptime(self.start_time, "%Y%m%d%H%M")
        start_timestamp  = time.mktime(time_tuple)
        print("------------------------------任务初始化完成------------------------------")
        if(current_timestamp < start_timestamp-8):
            # print("---------------------")
            print("进入等待时间(5s)，请确认输入结果")
            print("input信息：",self.AT1.answer_list)
            print("select信息：",self.AT1.select_list)            
            print("输入ctrl+c可强制退出")
            time.sleep(5)
    
    
    
    def run(self):
        while(10):
            try:
                self.AT1.wait_for_time()
                self.AT1.set_elements()
                self.AT1.auto_input()
                self.AT1.auto_button()
                self.AT1.auto_submit()
                time.sleep(self.AT1.ping_time)
                if(self.AT1.is_submit()):
                    print("成功抢到")
                return 
            except Exception as e:
                print("任务失败",e)
                continue
            
        print("任务失败")
    
    
    def start(self):
        self.init()
        self.run()    
    
    
    
    
    
    
    
    
    
    
    def thread_run(self):
        while(10):
            try:
                redirect_stdout()
                self.AT1.wait_for_time()
                self.AT1.set_elements()
                self.AT1.auto_input()
                self.AT1.auto_button()
                self.AT1.auto_submit()
                time.sleep(self.AT1.ping_time)
                restore_stdout()
                if(self.AT1.is_submit()):
                    print("成功抢到")
                    redirect_stdout()
                return 
            except Exception as e:
                print("任务失败",e)
                redirect_stdout()
                continue
            
        print("任务失败")    
    

    
    
    
    
    
    





               
class AuTotask_JSJ: 
    """

    """
    def __init__(self,url :str,data_path_or_data :str | dict,start_time: str,is_enable=True,SELECT_LIST=[]) -> None:
        """        
        初始化函数，用于设置数据收集和处理的参数。

        参数：
        - url (str): 收集表单的URL地址。 \n
        - data_path_or_data: 数据文件的存储路径或直接提供的数据。\n
        - start_time (str): 开始时间，格式为YYYYMMDDHHMM，例如202405121200（注意月份和日期需要补零）。\n
        - is_enable (bool, optional): 是否启用预输入选择内容的功能，默认为True。\n
        - SELECT_LIST (list, optional): 需要选择的内容列表。格式为[["单选项A"],["单选项B"],["多选项A","多选项B"]]，必须严格按照这个格式提供。\n

        data.txt 文件格式要求（如果data_path_or_data是路径）：\n
        {
            "学号姓名": "value",
            "手机号": "value",
            "邮箱": "value",
            "班级": "value",
            "学院": "value",
            "name": "value"
        }
        
        注意：
        - 确保提供的时间格式正确，否则可能会影响数据收集的准确性。
        - data_path_or_data 参数可以是文件路径或直接的数据对象，根据实际情况选择。
            
        """
        self.url=url
        self.data_path_or_data=data_path_or_data
        self.start_time=start_time
        self.is_enable=is_enable
        if(is_enable==False):
            self.SELECT_LIST=SELECT_LIST
    def run(self):
        self.AJ1.wait_for_time()
        self.AJ1.auto_input()
        self.AJ1.auto_button()
        self.AJ1.auto_submit()

    
    
    def thread_run(self):
        while(10):
            try:
                redirect_stdout()
                self.AJ1.wait_for_time()
                self.AJ1.auto_input()
                self.AJ1.auto_button()
                self.AJ1.auto_submit()
                restore_stdout()
                return 
            except Exception as e:
                print("任务失败",e)
                continue
    
    
    
    
    
    def init(self):
        self.AJ1=AUTO_JSJ_FORM(self.url)
        time.sleep(1)
        self.AJ1.set_wait_time(input_time=self.start_time)
        self.AJ1.set_base_data(self.data_path_or_data)
        if(self.is_enable==False):
            self.AJ1.select_list+=self.SELECT_LIST
        self.AJ1.print_all_qus()
        self.AJ1.Initializes_the_answer_list()
        if(self.AJ1.get_questions_select()!=[] and self.is_enable):
            self.AJ1.init_the_select_answer_list()
        current_timestamp = time.time()
        time_tuple = time.strptime(self.start_time, "%Y%m%d%H%M")
        start_timestamp  = time.mktime(time_tuple)
        print("----任务初始化完成----")
        if(current_timestamp < start_timestamp-8):
            print("---------------------")
            print("进入等待时间(5s)，请确认输入结果")
            print("input信息：",self.AJ1.answer_list)
            print("select信息：",self.AJ1.select_list)
            time.sleep(5)
    
    
    
    
    def start(self):
        self.init()
        self.run()
    
    





class ATThreadPool:
    def __init__(self, tasks_or_task_info_list: list[dict] | list[tuple] | list[Union[AuTotask_TX, AuTotask_JSJ]],task_type="TX" | "JSJ" ):
        """
            初始化线程池，用于管理多个任务。
            参数：
            - tasks_or_task_info_list: 任务列表，可以是任务对象列表，也可以是包含任务信息的字典列表。
            - task_type: 任务类型，可选值为"TX" 或 "JSJ"。
            
            - tasks_or_task_info_list (list[dict]):[{
                                            "url":"",
                                            "data_path_or_data":""
                                            "start_time":"202410311715",
                                            "is_enable":False,
                                            "SELECT_LIST":[[]],
                                        },...]                        
            - task_dict_list (list[tuple]):[ [("url","",202411021200,False,[[]]),...]              
            - task_type (str, optional): _description_. Defaults to "TX" | "JSJ".
        
        """
        
        if isinstance(tasks_or_task_info_list,list[Union[AuTotask_TX, AuTotask_JSJ]]):
            self.tasks = tasks_or_task_info_list
        else:
            self.init_with_info_dict(tasks_or_task_info_list,task_type)
        
        
    

    
    
    def init_with_info_dict(self,task_info_list: list[dict] | list[tuple],task_type="TX" | "JSJ"):
        """_summary_

        Args:
            task_dict_list (list[dict]):[{
                                            "url":"",
                                            "start_time":"202410311715",
                                            "is_enable":False,
                                            "SELECT_LIST":[[]],
                                        },...]
                                        
            task_dict_list (list[tuple]):[ [("url",202411021200,False,[[]]),...]]
                                        
                            
            task_type (str, optional): _description_. Defaults to "TX" | "JSJ".
        """
        
        if task_type=="TX":
            
            if isinstance(task_info_list,list[dict]):
                self.tasks=[AuTotask_TX(**task_info) for task_info in task_info_list]
                return 

            if isinstance(task_info_list,list[tuple]):
                self.tasks=[ AuTotask_TX(*task_info) for task_info in task_info_list]
                return 
    
        else:
            if isinstance(task_info_list,list[dict]):
                self.tasks=[AuTotask_JSJ(**task_info) for task_info in task_info_list]
                return
            if isinstance(task_info_list,list[tuple]):
                self.tasks=[ AuTotask_JSJ(*task_info) for task_info in task_info_list]
                return 
    
                                
    def init(self):
        if self.tasks==None:
            raise Exception("请先设置任务列表")
        print("-------------------------请确认所有初始化任务的信息-------------------------")    
        for task,i in zip(self.tasks,range(len(self.tasks))):
            print(f"-------------------------任务{i+1} 初始化信息-------------------------")
            task.init()
    def run(self):
        with ThreadPoolExecutor() as executor:
            executor.map(self.execute_task, self.tasks)
            
    def start(self):
        self.init()
        self.run()

    def execute_task(self, task):
        task.thread_run()