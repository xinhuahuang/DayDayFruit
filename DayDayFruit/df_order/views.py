# coding:utf-8
from django.shortcuts import render, redirect
from django.db import transaction
from cart.models import CartInfo
from df_goods.models import *
from models import *
from datetime import datetime


# Create your views here.
@transaction.atomic
def pay(request):

    if request.method == 'POST':
        user_id = request.session.get('user_id', 0)
        post = request.POST
        g_ids = post.getlist('gid', 0)
        pay_style = post.get('pay_style', 0)
        total_pay = post.get('total_pay', 0)
        address = post.get('address', '')
        oid = datetime.now().strftime('%Y%m%d%H%M%S')+str(user_id)
        odatetime = datetime.now()

        sid = transaction.savepoint()
        try:
            # 在OrderInfo表生成主表信息
            order = OrderInfo()
            order.oid = oid
            order.user_id = user_id
            order.odate = odatetime
            order.oPayType = pay_style
            order.ototal = total_pay
            order.oaddress = address
            order.save()

            # 在OrderDetailInfo表中生成订单详细信息
            for g_id in g_ids:
                cart = CartInfo.objects.filter(good_id=g_id)
                good = GoodsInfo.objects.get(id=g_id)
                price = good.gprice
                c_count = cart[0].count
                g_kucun = good.gkucun

                if c_count < g_kucun:
                    # 更新库存
                    good.gkucun -= c_count
                    good.save()
                    # 删除CartInfo表中的记录
                    cart.delete()
                    # 生成订单详细信息
                    odetail = OrderDetailInfo()
                    odetail.goods_id = g_id
                    odetail.order_id = oid
                    odetail.price = price
                    odetail.count = c_count
                    odetail.save()
                else:
                    raise Exception('update fail')
            # 提交事务
            transaction.savepoint_commit(sid)
        except Exception as e:
            # 回滚事务
            transaction.savepoint_rollback(sid)
            print e
            url = '/cart/place_order/?'
            for gid in g_ids:
                url += 'good_id='+gid+'&'
            return redirect(url[0:len(url)-1])
    return render(request, 'Users/user_center_info.html')


def paymoney(request, oid):
    order = OrderInfo.objects.filter(oid=oid)
    order.update(oIsPay=True)
    return redirect('/user/user_center_order/')