# coding:utf-8
from django.shortcuts import render
from django.http import JsonResponse
from models import *
from django.core.paginator import Paginator
from Users.models import *

# Create your views here.
def index(request):
    # 获取新鲜水果信息: id=1
    t1_links = GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[0:3]
    t1_news = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[0:4]

    # 获取猪牛羊肉
    t3_links = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[0:3]
    t3_news = GoodsInfo.objects.filter(gtype_id=3).order_by('-id')[0:4]

    # 获取禽类蛋品
    t4_links = GoodsInfo.objects.filter(gtype_id=4).order_by('-gclick')[0:3]
    t4_news = GoodsInfo.objects.filter(gtype_id=4).order_by('-id')[0:4]

    # 新鲜蔬菜
    t5_links = GoodsInfo.objects.filter(gtype_id=5).order_by('-gclick')[0:3]
    t5_news = GoodsInfo.objects.filter(gtype_id=5).order_by('-id')[0:4]

    # 速冻食品
    t6_links = GoodsInfo.objects.filter(gtype_id=6).order_by('-gclick')[0:3]
    t6_news = GoodsInfo.objects.filter(gtype_id=6).order_by('-id')[0:4]

    context = \
        {
            't1_links': t1_links,
            't1_news': t1_news,
            't3_links': t3_links,
            't3_news': t3_news,
            't4_links': t4_links,
            't4_news': t4_news,
            't5_links': t5_links,
            't5_news': t5_news,
            't6_links': t6_links,
            't6_news': t6_news,
        }
    return render(request, 'df_goods/index.html', context)


def index_handle(request, gid):
    # 获取海鲜水产
    t2_links = GoodsInfo.objects.filter(gtype_id=gid).order_by('-gclick')[0:3]
    t2_news = GoodsInfo.objects.filter(gtype_id=gid).order_by('-id')[0:4]

    links_list = []
    for link in t2_links:
        links_list.append({'id': link.id, 'title': link.gtitle, 'gtype_id':link.gtype_id})

    new_list = []
    for new in t2_news:
        new_list.append({'id': new.id, 'title': new.gtitle, 'pic': new.gpic.name, 'price': new.gprice, 'gtype_id':new.gtype_id})

    context = {'link_list': links_list, 'new_list': new_list}
    return JsonResponse(context)


def list(request, tid, pindex, sid):
    try:
        # 根据tid来获取分类
        type_info = TypeInfo.objects.get(id=int(tid))

        # 新品推荐
        new_goods = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')[0:2]

        # 获取商品信息并排序
        if sid == "":
            good_info = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
            sid = 0
        elif int(sid) == 1:
            good_info = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
            sid = 1
        else:
            good_info = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
            sid = 2

        p = Paginator(good_info, 10)
        if pindex == '':
            pindex = 1
        else:
            pindex = int(pindex)

        good_info_2 = p.page(pindex)
        p_list = p.page_range

        context = \
            {
                'type_info': type_info,
                'good_info': good_info,
                'flag': 'true',
                'new_goods': new_goods,
                'good_info_2': good_info_2,
                'p_list': p_list,
                'p_index': pindex,
                'tid': tid,
                'sid': sid,
            }
    except Exception, e:
        print e
        context = {'type_info': '没有获取到分类', 'good_info': '<h1>没有获取到信息，请确认搜索条件是否正确</h1>', 'flag': 'false'}

    return render(request, 'df_goods/list.html', context)


# 展示订单详细信息
def detail(request, tid, sid):
    try:
        tid = int(tid)
        sid = int(sid)

        good_detail = GoodsInfo.objects.get(gtype_id=tid, id=sid)
        good_type = TypeInfo.objects.get(id=tid)
        new_list = GoodsInfo.objects.filter(gtype_id=tid).order_by('-id')[0:2]
        context = {'good_detail': good_detail, 'good_type': good_type, 'new_list': new_list}

        # 将用户访问信息写入数据库
        if request.session.has_key('user_id'):
            user_id = request.session.get('user_id')
            visited_info = VisitInfo()

            visited_count = VisitInfo.objects.filter(vusers_id=user_id, vtitle=good_detail.gtitle).count()

            if visited_count:
                visited = VisitInfo.objects.get(vusers_id=user_id, vtitle=good_detail.gtitle)
                visited.vclick = int(visited.vclick)+1
                visited.save()
            else:
                visited_info.vpic = good_detail.gpic
                visited_info.vtitle = good_detail.gtitle
                visited_info.vprice = good_detail.gprice
                visited_info.vunit = good_detail.gunit
                visited_info.vusers_id = user_id
                visited_info.vtype = tid
                visited_info.vindex = sid
                visited_info.save()


    except Exception, e:
        print e
        context = {'flag': False}

    return render(request, 'df_goods/detail.html', context)