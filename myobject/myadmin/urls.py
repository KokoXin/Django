"""myobject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
from . import viewsgoods

urlpatterns = [
    # 后台首页
    url(r'^$', views.index, name="myadmin_index"),

    # 后台用户管理
    url(r'^users$', views.usersindex, name="myadmin_usersindex"),
    url(r'^usersadd$', views.usersadd, name="myadmin_usersadd"),
    url(r'^usersinsert$', views.usersinsert, name="myadmin_usersinsert"),
    url(r'^usersdel/(?P<uid>[0-9]+)$', views.usersdel, name="myadmin_usersdel"),
    url(r'^usersedit/(?P<uid>[0-9]+)$', views.usersedit, name="myadmin_usersedit"),
    url(r'^usersupdate/(?P<uid>[0-9]+)$', views.usersupdate, name="myadmin_usersupdate"),

    # 后台管理员路由
    url(r'^login$', views.login, name="myadmin_login"),
    url(r'^dologin$', views.dologin, name="myadmin_dologin"),
    url(r'^logout$', views.logout, name="myadmin_logout"),
    url(r'^verify$', views.verify, name="myadmin_verify"), #验证码

    #后台商品类别管理路由
    url(r'^types$',viewsgoods.typesindex,name='myadmin_typesindex'),
    url(r'^typesadd(?P<tid>[0-9]+)$', viewsgoods.typesadd, name="myadmin_typesadd"),
    url(r'^typesinsert$', viewsgoods.typesinsert, name="myadmin_typesinsert"),
    url(r'^typesdel/(?P<tid>[0-9]+)$', viewsgoods.typesdel, name="myadmin_typesdel"),
    url(r'^typesedit/(?P<tid>[0-9]+)$', viewsgoods.typesedit, name="myadmin_typesedit"),
    url(r'^typesupdate/(?P<tid>[0-9]+)$', viewsgoods.typesupdate, name="myadmin_typesupdate"),

    #后台商品信息管理路由
    url(r'^goods/(?P<pIndex>[0-9]+)$',viewsgoods.goodsindex,name='myadmin_goodsindex'),
    # url(r'^goodssearch/(?P<pIndex>[0-9]+)$',viewsgoods.goodssearch,name='myadmin_goodssearch'),
    url(r'^goodsadd$',viewsgoods.goodsadd,name='myadmin_goodsadd'),
    url(r'^goodsinsert$',viewsgoods.goodsinsert,name='myadmin_goodsinsert'),
    url(r'^goodsdel/(?P<uid>[0-9]+)$', viewsgoods.goodsdel, name="myadmin_goodsdel"),
    url(r'^goodsedit/(?P<uid>[0-9]+)$', viewsgoods.goodsedit, name="myadmin_goodsedit"),
    url(r'^goodsupdate/(?P<uid>[0-9]+)$', viewsgoods.goodsupdate, name="myadmin_goodsupdate"),

    #后台订单管理页
    url(r'^orders$',viewsgoods.orders,name='myadmin_orders'),
    url(r'^ordersdetail/(?P<oid>[0-9]+)$',viewsgoods.ordersdetail,name='myadmin_ordersdetail'),
    url(r'^ordersedict/(?P<oid>[0-9]+)$',viewsgoods.ordersedict,name='myadmin_ordersedict'),
    url(r'^ordersinsert/(?P<oid>[0-9]+)$',viewsgoods.ordersinsert,name='myadmin_ordersinsert'),

]
