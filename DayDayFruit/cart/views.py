# coding:utf-8

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from models import *
from Users import user_decorator
from df_goods.models import *


# Create your views here.
@user_decorator.login
def display(request):
    # 获取购物车中有多少件商品
    user_id = request.session.get('user_id')
    cart_list = CartInfo.objects.filter(user_id=user_id).filter(is_buy=0)

    context = {'count': cart_list.count, 'cart_list': cart_list, 'page_num': 1, 'title': '购物车'}
    return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request):
    user_id = request.session.get('user_id')
    gid = request.GET.get('gid', 0)
    num = int(request.GET.get('num', 0))
    cart = CartInfo.objects.filter(good_id=int(gid)).filter(user_id=int(user_id))
    good = GoodsInfo.objects.filter(id=int(gid))
    kucun = good[0].gkucun

    # 如果购物车中有相同的商品了，则在该商品上＋１；否则直接新建商品信息
    if cart.count() and num < kucun:
        cart_add = cart[0]
        cart_add.count += num

        # 更新库存
        num = kucun - num
        good.update(gkucun=num)
    elif cart.count() < 1:
        cart_add = CartInfo()
        cart_add.count = num
        cart_add.user_id = user_id
        cart_add.good_id = gid
        cart_add.is_buy = 0

        # 更新库存
        num = kucun - num
        good.update(gkucun=num)

    cart_add.save()
    good[0].save()

    if request.is_ajax():
        cart = CartInfo.objects.filter(is_buy=0).filter(user_id=int(user_id))
        return JsonResponse({'count': cart.count(), 'kucun': good[0].gkucun})
    else:
        return redirect('/cart/display/')


# 返回购物车商品的数量
def cart_count(request):
    user_id = request.session.get('user_id')

    if user_id is None:
        return JsonResponse({'count': 0})
    else:
        num = CartInfo.objects.filter(user_id=int(user_id)).filter(is_buy=0).count()
        return JsonResponse({'count': num})


# 修改购物车中商品的数量
def modify_num(request):
    user_id = int(request.session.get('user_id'))
    gid = request.GET.get('gid', 0)
    num = int(request.GET.get('num', 0))

    if user_id is None:
        return JsonResponse({'count': 0})
    else:
        cart = CartInfo.objects.filter(user_id=user_id).filter(good_id=gid)
        good = GoodsInfo.objects.filter(id=gid)
        kucun = good[0].gkucun
        int_count = cart[0].count

        # 更新数据库中的值
        if num < 0 and int_count > 1:
            int_count -= 1
            cart.update(count=int_count)
            good.update(gkucun=kucun+1)
        elif num > 0:
            int_count += 1
            cart.update(count=int_count)
            good.update(gkucun=kucun-1)

    # 将更新后的数据返回出来
    cart = CartInfo.objects.filter(user_id=user_id).filter(good_id=gid)
    return JsonResponse({'count': cart[0].count, 'kucun': good[0].gkucun})


# 手动更新购物车的数量
def modify(request):
    user_id = int(request.session.get('user_id'))
    gid = request.GET.get('gid', 0)
    old_count = int(request.GET.get('old_count', 0))
    new_count = int(request.GET.get('new_count', 0))

    if user_id is None:
        return JsonResponse({'count': 0})
    else:
        cart = CartInfo.objects.filter(user_id=user_id).filter(good_id=gid)
        good = GoodsInfo.objects.filter(id=gid)
        kucun = good[0].gkucun

        # 更新数据库中的值
        if new_count >= 1 and kucun+old_count-new_count >= 1:
            cart.update(count=new_count)
            good.update(gkucun=kucun+old_count-new_count)

    # 将更新后的数据返回出来
    cart = CartInfo.objects.filter(user_id=user_id).filter(good_id=gid)
    return JsonResponse({'count': cart[0].count, 'kucun': good[0].gkucun})


def delete_cart(request, gid, count):
    """
        根据good_id和user_id删除购物车中的记录，并返回一个JsonResponse
    """
    user_id = int(request.session.get('user_id'))
    gid = int(gid)
    num = int(count)

    try:
        cart = CartInfo.objects.filter(user_id=user_id).filter(good_id=gid)
        good = GoodsInfo.objects.filter(id=gid)
        kucun = good[0].gkucun
        if cart.count():
            cart.delete()
            good.update(gkucun=kucun+num)
            flag = True
        else:
            flag = False
    except Exception, e:
        print e
        flag = False
    finally:
        return JsonResponse({'flag': flag})