# -*- coding:utf-8 -*-
import time
import jenkins as pythonjenkins




class jenkins_job_build(object):
    # def __init__(self,jenkins_server_url,user_id,api_token):
    def __init__(self):

        # 初始化jenkins对象，连接远程的jenkins master server
        # self.jenkins_server_url = jenkins_server_url
        # self.user_id = user_id
        # self.api_token = api_token
        self.server = pythonjenkins.Jenkins(jenkins_server_url, username=user_id, password=api_token)

    # 启动任务
    def build_jenkins_job(self, job_name, parameters=None):
        item_number = self.server.build_job(job_name, parameters=parameters)
        # print(item_number)
        return item_number  # 返回的是启动任务列队号，不是构建号，下面这个方法才是获取构建编号

    # 获取启动任务对应的构建编号
    def build_number(self, item_number):
        while True:
            time.sleep(1)
            build_info = self.server.get_queue_item(int(item_number))
            print('build', build_info)
            if 'executable' in build_info:
                build_number = build_info['executable']["number"]
                return build_number

    # 获取jenkins任务最后次构建号
    def get_job_lastBuild_number(self, job_name):
        lastBuild_number = self.server.get_job_info(job_name)['lastBuild']['number']
        return lastBuild_number

    # 判断任务是否构建完成，正在构建返回的是True
    def job_is_building(self, job_name, build_number):
        is_building = self.server.get_build_info(job_name, build_number)['building']
        return is_building

    # 获取构建完成后的结果
    def get_job_build_status(self, job_name, build_number):
        job_status = self.server.get_build_info(job_name, build_number)['result']
        return job_status

    # 获取所有正在构建中的jenkins任务
    def get_all_building_jobs(self):
        building_jobs = self.server.get_running_builds()
        return building_jobs

    # 获取所有jenkins任务
    def get_all_jobs(self):
        jobs = self.server.get_jobs()
        return jobs

    # 获取jenkins构建时控制台输出的日志
    def get_build_job_log(self, job_name, job_number):
        return self.server.get_build_console_output(job_name, job_number)

if __name__ == '__main__':
    # jenkins地址
    jenkins_server_url = 'http://192.168.3.98:8999/'
    # 登陆jenkins的用户名
    user_id = 'master'
    # 登陆jenkins后，在用户名>设置>API Token，下可以生成一个token
    api_token = '11f71f0bf99b41231123fa379b788e8670'
    example_jenkins = jenkins_job_build()
    # # 启动任务
    begin = example_jenkins.build_jenkins_job("test")
    print(begin)
    # 获取启动任务对应的构建编号
    buld_number = example_jenkins.build_number(begin)
    print(buld_number)
    # 获取jenkins任务最后次构建号
    # num = example_jenkins.get_job_lastBuild_number("自动化测试")
    # print(num)
    # # 判断任务是否构建完成，正在构建返回的是True
    # result1 = example_jenkins.job_is_building("自动化测试",num)
    # print(result1)
    # # 获取构建完成后的结果
    # result = example_jenkins.get_job_build_status("自动化测试",num)
    # print(result)
    # # 获取所有jenkins任务
    # all_task = example_jenkins.get_all_jobs()
    # print(all_task)
    # # 获取jenkins构建时控制台输出的日志
    # console = example_jenkins.get_build_job_log("自动化测试",num)
    # print(console)