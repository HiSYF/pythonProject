from django.http import HttpResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import lmt
from .serilizers import LmtModelSerializers
from . import lmtUtils
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction

import time
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events


class lmtApiview(APIView):

    def get(self, request):
        # 获取数据集（学生模型对象）
        lmt_data = lmt.objects.all()
        # 分页
        page = PageNumberPagination()  # 产生一个分页器对象
        page.page_size = 10  # 默认每页显示的多少条记录
        page.page_query_param = 'page'  # 默认查询参数名为 page
        page.page_size_query_param = 'size'  # 前台控制每页显示的最大条数
        page.max_page_size = 10  # 后台控制显示的最大记录条数，防止用户输入的查询条数过大
        ret = page.paginate_queryset(lmt_data, request)


        # 实例化序列化器，得到序列化器对象
        ser = LmtModelSerializers(instance=ret, many=True)
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
        student = LmtModelSerializers(data=request.data)
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
        student = lmt.objects.get(pk=pk)
        ser = LmtModelSerializers(instance=student)
        return Response(ser.data)

    # 修改
    def put(self, request, pk):
        instance = lmt.objects.get(pk=pk)

        ser = LmtModelSerializers(instance=instance, data=request.data)
        print(request.data)
        if not ser.is_valid():
            return Response(ser.errors)
        ser.save()
        return Response(ser.data)

    # 删除
    def delete(self, request, pk):
        lmt.objects.get(pk=pk).delete()
        return Response({'detail': '删除成功！！'})



# 实例化调度器
scheduler = BackgroundScheduler(timezone='Asia/Shanghai') # 这个地方要加上时间，不然他有时间的警告
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")
def getLmtstsatus(data):
    pk,username, password = data.pk,data.username,data.password
    status = lmtUtils.getdata(username, password)
    # 使用了 transaction.atomic() 来确保更新操作是原子的，即要么全部成功，要么全部回滚
    with transaction.atomic():
        instance = lmt.objects.get(pk=pk)
        instance.sxtZS = status['sxtzs']
        instance.sxtQYS = status['sxtqys']
        instance.sxtZXS = status['sxtzx']
        instance.save()

@register_job(scheduler, "interval", max_instances=100,hours=1,args=['定时任务'], replace_existing=True)
def process_value(request):
    # 定时任务：https://blog.csdn.net/hans99812345/article/details/123926503
    # https: // cloud.tencent.com / developer / article / 1585026
    data = lmt.objects.all()
    # 使用进程池
    with ThreadPoolExecutor() as executor:
        executor.map(getLmtstsatus, data)

    return HttpResponse("ok")
# 监控任务
register_events(scheduler) # 这个event 这个会有已经被废弃的用法删除线，我不知道这个删除了 ，还会不会好用
# 调度器开始运行
scheduler.start()