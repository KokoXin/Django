# myobject/myweb/urls.py

from django.conf.urls import url

from . import views
from . import viewsorders

urlpatterns = [
	#=================商品展示=========================	
	url(r'^$', views.index, name="index"),#网站首页
	url(r'^list$', views.list, name="list"),#商品列表页
	url(r'^detail/(?P<gid>[0-9]+)$', views.detail, name="detail"),#商品详情页


	#=============会员模块===========================
	#会员登录
	url(r'^login$',views.login,name="login"),
	url(r'^dologin$', views.dologin, name="myweb_dologin"),
	url(r'^logout$', views.logout, name="myweb_logout"),
	url(r'^verifycode$', views.verifycode, name="verifycode"),
	#会员注册
	url(r'^regist$',views.regist,name="regist"),
	url(r'^doregist$',views.doregist,name="doregist"),
	url(r'^ajax$',views.ajax,name="ajax"),


	#==============购物车模块=============================
	url(r'^shopcart$',views.shopcart,name="shopcart"),#浏览购物车
	url(r'^shopcartadd/(?P<sid>[0-9]+)$',views.shopcartadd,name="shopcartadd"),#浏览购物车
	url(r'^shopcartdel/(?P<sid>[0-9]+)$',views.shopcartdel,name="shopcartdel"),#浏览购物车
	url(r'^shopcartclear$',views.shopcartclear,name="shopcartclear"),#浏览购物车
	url(r'^shopcartchange$',views.shopcartchange,name="shopcartchange"),#浏览购物车



	#===============订单模块=================================
	#个人中心
	url(r'^personal$',views.personal,name="personal"),
	url(r'^personaledict$',views.personaledict,name="personaledict"),#个人中心
	url(r'^personalinsert$',views.personalinsert,name="personalinsert"),#个人中心
	url(r'^personalorders$',views.personalorders,name="personalorders"),#个人中心
	url(r'^personalordersdetail/(?P<oid>[0-9]+)$',views.ordersdetail,name="ordersdetail"),#浏览购物车
	url(r'^personalordersdelete/(?P<oid>[0-9]+)$',views.ordersdelete,name="ordersdelete"),#浏览购物车
	url(r'^personalorderschange/(?P<oid>[0-9]+)$',views.orderschange,name="orderschange"),#浏览购物车
	
	#订单中心
	url(r'^ordersindex$',viewsorders.ordersindex,name="ordersindex"),#个人中心
	url(r'^ordersconfirm$',viewsorders.ordersconfirm,name="ordersconfirm"),#个人中心
	url(r'^ordersinsert$',viewsorders.ordersinsert,name="ordersinsert"),#个人中心


]