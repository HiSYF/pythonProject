from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .jenkinsUtil import jenkins_job_build
from .models import *
from .serializers import *


class JenkinsApiview(APIView):
    def get(self,request):
        Jenkins_data = JkBase.objects.all()

        # 分页
        page = PageNumberPagination()  # 产生一个分页器对象
        page.page_size = 10  # 默认每页显示的多少条记录
        page.page_query_param = 'page'  # 默认查询参数名为 page
        page.page_size_query_param = 'size'  # 前台控制每页显示的最大条数
        page.max_page_size = 10  # 后台控制显示的最大记录条数，防止用户输入的查询条数过大
        ret = page.paginate_queryset(Jenkins_data, request)

        # 实例化序列化器，得到序列化器对象
        ser = JenkinsSerializer(instance=ret, many=True)
        # 调用序列化器对象的data属性方法获取转换后的数据
        data = ser.data
        # 获取总记录数和总页数
        total_articles = Jenkins_data.count()
        total_pages = page.page.paginator.num_pages
        return Response({
            'total_articles': total_articles,
            'total_pages': total_pages,
            'data': data  # 分页后的数据
        })
    def post(self, request):
        # 反序列化数据
        jenkins = JenkinsSerializer(data=request.data)
        # 校验不通过
        if not jenkins.is_valid():
            # 返回错误信息
            return Response(jenkins.errors)
        # 校验通过，保存数据
        jenkins.save()
        # 响应数据
        return Response(jenkins.data)

class JenkinsDerailApiview(APIView):
    # 获取信息
    def get(self, request, pk):
        jenkins = JkBase.objects.get(pk=pk)
        # print("*******")
        # print(request.data['data'])
        ser = JenkinsSerializer(instance=jenkins)
        return Response(ser.data)

    # 修改
    def put(self, request, pk):
        instance = JkBase.objects.get(pk=pk)

        ser = JenkinsSerializer(instance=instance, data=request.data)
        print(request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    # 删除
    def delete(self, request, pk):
        JkBase.objects.get(pk=pk).delete()
        return Response({'detail': '删除成功！！'})

# 初始化jenkins的任务
@api_view(['GET'])
def initJob(request):
    # print(request.data['jenkinsJob'])
    jenkins = JkBase.objects.get(pk=request.data['jenkins'])
    jenkins_server = JenkinsSerializer(instance=jenkins)

    jenkins_server_url = jenkins_server.data['jenkinsurl']
    # 登陆jenkins的用户名
    user_id = jenkins_server.data['username']
    # 登陆jenkins后，在用户名>设置>API Token，下可以生成一个token
    api_token = jenkins_server.data['token']

    example_jenkins = jenkins_job_build(jenkins_server_url,user_id,api_token)
    all_task = example_jenkins.get_all_jobs()
    print(jenkins_server.data['id'])
    jenkinsbase_id = jenkins_server.data['id']
    for i in all_task:

        jobname = i['name']
        joburl = i['url']
        jenkinsbase_id = jenkinsbase_id
        task = Jkjob.objects.create(jobname=jobname,joburl=joburl)
        task.JkId.add(jenkins)
        # task.save()
        # print(serializer.is_valid)


    return Response(task.objects,all())
# 获取jenkins的任务
class JkjobApiview(APIView):
    def get(self, request):
        # 获取数据集（学生模型对象）
        Jkjobs = Jkjob.objects.all()
        # 分页
        page = PageNumberPagination()  # 产生一个分页器对象
        page.page_size = 10  # 默认每页显示的多少条记录
        page.page_query_param = 'page'  # 默认查询参数名为 page
        page.page_size_query_param = 'size'  # 前台控制每页显示的最大条数
        page.max_page_size = 10  # 后台控制显示的最大记录条数，防止用户输入的查询条数过大
        ret = page.paginate_queryset(Jkjobs, request)

        # 实例化序列化器，得到序列化器对象
        ser = jobSerializer(instance=ret, many=True)
        # 调用序列化器对象的data属性方法获取转换后的数据
        data = ser.data

        # 获取总记录数和总页数
        total_articles = Jkjobs.count()
        total_pages = page.page.paginator.num_pages
        return Response({
            'total_articles': total_articles,
            'total_pages': total_pages,
            'data': data  # 分页后的数据
        })


def post(self, request):
    # 反序列化数据
    student = jobSerializer(data=request.data)
    # 校验不通过
    if not student.is_valid():
        # 返回错误信息
        return Response(student.errors)
    # 校验通过，保存数据
    student.save()
    # 响应数据
    return Response(student.data)

# @api_view(['GET'])
# def getJob(request):

    pass