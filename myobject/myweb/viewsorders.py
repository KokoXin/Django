from django.shortcuts import render
from django.http import HttpResponse
from myweb.models import Types,Goods,Users,Orders,Detail
import time,datetime

#=====================商品订单中心=====================
#公共信息加载函数
def loadinfo():
	context={}
	context['type0list']=Types.objects.filter(pid=0)
	return context
#提交订单页
def ordersindex(request):
	context=loadinfo()
	#获取要结账的商品id信息
	ids=request.GET.get('gids','')
	if ids == '':
		return HttpResponse('请选择要结算的商品')
	gids=ids.split(',')
	#获取购物车中的商品信息
	shoplist=request.session['shoplist']
	#封装要结账的商品信息,以及累计总金额
	orderlist={}
	total=0
	for sid in gids:
		orderlist[sid]=shoplist[sid]
		print(orderlist)
		print('=============')
		total+=shoplist[sid]['price']*shoplist[sid]['m']
	request.session['orderlist']=orderlist
	request.session['total']=total
	users=Users.objects.get(username=request.session['adminuser'])
	request.session['vipuser']=users.toUsers()
	# print(request.session['vipuser'])
	return render(request,'myweb/orders/index.html',context)
#确认订单页
def ordersconfirm(request):
	context=loadinfo()
	print(request)
	return render(request,'myweb/orders/ordersconfirm.html',context)
#执行订单添加
def ordersinsert(request):
	context=loadinfo()
	#封装订单信息,并执行添加
	buytime = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S"))
	orders=Orders()
	orders.uid=request.session['vipuser']['id']
	orders.linkman=request.POST['linkman']
	orders.address=request.POST['address']
	orders.code=request.POST['code']
	orders.phone=request.POST['phone']
	orders.addtime=time.time()
	orders.total=request.POST['total']
	orders.status=0
	orders.save()
	#获取订单详情
	orderlist=request.session['orderlist']
	shoplist=request.session['shoplist']
	#遍历购物信息,并添加订单详情信息
	for shop in orderlist.values():
		del shoplist[str(shop['id'])]
		detail=Detail()
		detail.orderid=orders.id
		print(shop['id'])
		detail.goodsid=shop['id']
		detail.name=shop['goods']
		detail.price=shop['price']
		detail.num=shop['m']
		detail.save()
	request.session['shoplist']=shoplist
	context={'buytime':buytime,'ordersid':int(orders.addtime),'orderlist':request.session['orderlist'],'total':request.session['total']}
	del request.session['orderlist']
	del request.session['total']
	return render(request,'myweb/orders/ordersinfo.html',context)



