import requests

jenkins_url = 'http://192.168.3.98:8999'
jenkins_username = 'master'
jenkins_password = 'master'

# 构建认证头部信息
auth = (jenkins_username, jenkins_password)

# 获取Jenkins信息
def get_jenkins_info():
    api_url = f'{jenkins_url}/api/json'
    response = requests.get(api_url, auth=auth)
    if response.status_code == 200:
        jenkins_info = response.json()
        jenkins_info['crumb']
        print(jenkins_info['crumb'])
    else:
        print("获取Jenkins信息失败")
def reload_crumb():
    reload_url = f'{jenkins_url}/crumbIssuer/reload'
    response = requests.post(reload_url, auth=auth)
    print(response.text)
    if response.status_code == 200:
        print("重新生成crumb成功")
    else:
        print("重新生成crumb失败")

# 示例调用
reload_crumb()
# 触发Jenkins构建
def trigger_build(job_name):
    api_url = f'{jenkins_url}/job/{job_name}/build'
    response = requests.post(api_url, auth=auth)
    print(response.text)
    if response.status_code == 201:
        print(f"触发构建成功: {job_name}")
    else:
        print(f"触发构建失败: {job_name}")

# 获取Jenkins构建日志
def get_build_console_output(job_name, build_number):
    api_url = f'{jenkins_url}/job/{job_name}/{build_number}/consoleText'
    response = requests.get(api_url, auth=auth)
    if response.status_code == 200:
        console_output = response.text
        print(console_output)
    else:
        print("获取构建日志失败")
def get_last_build_console_output(job_name):
    api_url = f'{jenkins_url}/job/{job_name}/lastSuccessfulBuild/api/json'
    response = requests.get(api_url, auth=auth)
    if response.status_code == 200:
        console_output = response.text
        print(console_output)
    else:
        print("获取构建日志失败")
# 示例调用
# get_jenkins_info()
# trigger_build("depots")
# get_last_build_console_output("depots")
