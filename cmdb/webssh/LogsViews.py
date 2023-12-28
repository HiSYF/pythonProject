# from channels.generic.websocket import AsyncWebsocketConsumer
from django.http import HttpResponse

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .common import execute_linux, write_log, get_log_list, ssh3,cleanup_log,get_search_log_list
from .models import Host
from .serilizers import HostModelSerializers
import os,asyncio,paramiko
from rest_framework.decorators import api_view
from urllib.parse import parse_qs
class lmtApiview(APIView):

    def get(self, request):
        # 获取数据集（学生模型对象）
        lmt_data = Host.objects.all()
        # 分页
        page = PageNumberPagination()  # 产生一个分页器对象
        page.page_size = 10  # 默认每页显示的多少条记录
        page.page_query_param = 'page'  # 默认查询参数名为 page
        page.page_size_query_param = 'size'  # 前台控制每页显示的最大条数
        page.max_page_size = 10  # 后台控制显示的最大记录条数，防止用户输入的查询条数过大
        ret = page.paginate_queryset(lmt_data, request)


        # 实例化序列化器，得到序列化器对象
        ser = HostModelSerializers(instance=ret, many=True)
        # 调用序列化器对象的data属性方法获取转换后的数据
        data = ser.data

        # 获取总记录数和总页数
        total_articles = lmt_data.count()
        total_pages = page.page.paginator.num_pages
        return Response({
            'total_articles': total_articles,
            'total_pages': total_pages,
            'data': data  # 分页后的数据
        })

    def post(self, request):
        # 反序列化数据
        student = HostModelSerializers(data=request.data)
        # 校验不通过
        if not student.is_valid():
            # 返回错误信息
            return Response(student.errors)
        # 校验通过，保存数据
        student.save()
        # 响应数据
        return Response(student.data)
class StudentDerailApiview(APIView):
    # 获取信息
    def get(self, request, pk):
        student = Host.objects.get(pk=pk)
        ser = HostModelSerializers(instance=student)
        return Response(ser.data)

    # 修改
    def put(self, request, pk):
        instance = Host.objects.get(pk=pk)

        ser = HostModelSerializers(instance=instance, data=request.data)
        print(request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    # 删除
    def delete(self, request, pk):
        Host.objects.get(pk=pk).delete()
        return Response({'detail': '删除成功！！'})

LOG_BASE_DIR = "/data/logs"


@api_view(['GET', 'POST'])
def view_dir(request):
    """
    查看目录列表
    :param request:
    :return:
    """
    ip = request.GET.get('ip')
    if not ip:
        return HttpResponse("主机不能为空")

    # 判断主机是否存活
    cmd = "whoami"
    result = ssh3(ip, cmd)
    # print("result", result,type(result))

    if not result or result['status'] != 0:
        return HttpResponse("错误，主机: {}，ssh连接失败！".format(ip))

    dir = request.GET.get('dir')
    if not dir:
        dir = ''

    # 搜索关键字
    key = request.GET.get('search')
    # print("key",key)
    # 判断关键字是否存在
    if key:
        # print(1)
        log_list = get_search_log_list(ip, dir,key)

    else:
        log_list = get_log_list(ip, dir)
        # 分页a标签的herf前缀

    # print("log_list",log_list)
    # log_list = get_log_list(ip, dir)
    if log_list is False:
        return Response("获取目录列表失败")
    elif log_list == []:
        return Response("目录列表为空")
    elif log_list == {}:
        return Response("搜索结果为空")
    else:
        pass

    dir_path = os.path.join(LOG_BASE_DIR, dir)

    data = {
        "ip": ip,
        "dir_path": dir_path,
        "dir": dir,
        "log_list": log_list,
        # "host_all": host_all
    }
    # next_dir_path = os.path.join(dir_path,dir)

    return Response(data)
@api_view(['GET', 'POST'])
def view_log(request):
    """
    查看实时日志
    :param request:
    :return:
    """
    ip = request.GET.get('ip')
    # port = settings.SSH_PORT
    dir = request.GET.get('dir')
    # 日志文件
    file_name = request.GET.get('file_name')
    LOG_BASE_DIR = "/data/logs"
    log_file = os.path.join(LOG_BASE_DIR, dir, file_name)
    data = {
        "ip": ip,
        "dir": dir,
        "file_name": file_name,
        "log_file": log_file
    }
    print(data)
    return Response( data)
