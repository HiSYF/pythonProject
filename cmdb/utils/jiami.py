import base64
import datetime
import json
import os
import execjs
import requests
os.environ['NO_PROXY'] = '124.128.64.179'


curr_time = datetime.datetime.now()
time_str = curr_time.strftime("%Y-%m-%d")

# 加密方法
def sm2encode(text):
    url = 'https://tysfrz.isdapp.shandong.gov.cn/api-gateway/jpaas-jis-peruser-server/front/login/get-pubk'
    res = requests.get(url).json()
    # 获取公钥
    publicKey = res['data']['pubk']

    os.environ["NODE_PATH"] = os.getcwd()+"/node_modules"
    # print(os.environ["NODE_PATH"] )
    parser = execjs.compile("""
        const sm2 = require('sm-crypto').sm2
        var cipherMode = 1
        function sm2encode(msgString,publicKey){
            publicKey = publicKey;
            encryptData = sm2.doEncrypt(msgString, publicKey, cipherMode); // 加密结果
            console.log(encryptData);
            return encryptData
        }
    """)
    # print(parser.call('sm2encode',text))
    return parser.call('sm2encode',text,publicKey)

# 验证码识别
def dowimg():
    # 下载验证码图片
    img_url = 'https://tysfrz.isdapp.shandong.gov.cn/api-gateway/common-captcha-server/interface/code/imageCode?token=129e71b146d04405a06725c7a53366e1'
    img_res = requests.get(url=img_url)
    with open('code.png',mode='wb') as f:
        f.write(img_res.content)
    # 识别验证码
    with open('code.png', 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": 'sunyf', "password": 'a123456', "typeid": '1003', "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        code = result["data"]["result"]
        # 携带验证码请求验证接口，成功返回token 失败则重新识别并重试
        imgtoken_url = 'https://tysfrz.isdapp.shandong.gov.cn/api-gateway/common-captcha-server/interface/code/checkCode?inputcode=' + code + '&token=129e71b146d04405a06725c7a53366e1'
        imgtoken = requests.get(imgtoken_url).json()
        if imgtoken['success']:
            return imgtoken['data']['token']
        else:
            dowimg()
    else:
        #！！！！！！！注意：返回 人工不足等 错误情况 请加逻辑处理防止脚本卡死 继续重新 识别
        return result["message"]
    return ""

# 登录接口，传参：用户名、密码
def login(userName,password):
    login_url = 'https://tysfrz.isdapp.shandong.gov.cn/api-gateway/jpaas-jis-peruser-server/front/login/usernamepwd-login'
    login_data = {
        'userName':sm2encode(userName),
        'password':sm2encode(password),
        'token':dowimg()
        }
    login_info = requests.post(url=login_url,data=login_data).json()
    print(login_info)
    accessToken = login_info['data']['accessToken']

    header = {
        'Cookie':'accessToken='+accessToken
    }
    location_url = 'https://tysfrz.isdapp.shandong.gov.cn/jpaas-jis-sso-server/sso/entrance/auth-center?appMark=l9wjke6ijdm&gbTrust=false'
    # location_url = 'https://tysfrz.isdapp.shandong.gov.cn/api-gateway/jpaas-jis-sso-server/sso/entrance/auth-center?appMark=l9wjke6ijdm' # 2023-09-19，url失效
    location = requests.get(url=location_url,headers=header,allow_redirects=False).headers['location']
    # spt_url = requests.get(url=location,headers=header,allow_redirects=False).headers['location']
    return location


if __name__ == "__main__":
    print(login('371312198106035328','qsh123456@'))
    # getPubk()