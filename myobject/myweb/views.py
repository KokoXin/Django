from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myweb.models import Types,Goods,Users,Orders,Detail

from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import time
from django.views.decorators.csrf import csrf_exempt



#公共信息加载函数
def loadinfo():
	context={}
	context['type0list']=Types.objects.filter(pid=0)
	return context

#网站首页
def index(request):
	context = loadinfo()
	return render(request,'myweb/index.html',context)

#商品列表页
def list(request):
	context = loadinfo()
	list = Goods.objects.filter()
	if request.GET.get('tid','') != '':
		tid = str(request.GET.get('tid',''))
		list = list.filter(typeid__in=Types.objects.only('id').filter(path__contains=','+tid+','))
		#select * from goods where typeid in(select id from type where path like '%,1,%')
	context['goodslist']=list
	return render(request,'myweb/list.html',context)

#商品详情页
def detail(request,gid):
	context=loadinfo()
	ob=Goods.objects.get(id=gid)
	ob.clicknum+=1
	ob.save()
	context['goods']=ob
	return render(request,'myweb/detail.html',context)

#==========================会员登录页=========================================
def login(request):
	context = loadinfo()
	return render(request,'myweb/users/login.html',context)

# 会员执行登录
def dologin(request):
	#校验证码
	verifycode=request.session['verifycode']
	code=request.POST['code']
	print(code)
	if code!=verifycode:
		context={'info':'验证码错误!','num':6}
		print(context['info'])
		print('啦啦啦')
		return render(request,"myweb/users/login.html",context)
		print('啦啦啦2')
	try:
		user = Users.objects.get(username=request.POST['account'])
		#判断当前用户是否是后台管理员用户
		print('lalala3')
		if user.state == 1:
			# 验证密码
			import hashlib
			m = hashlib.md5() 
			m.update(bytes(request.POST['password'],encoding="utf8"))
			if user.password == m.hexdigest():
				# 此处登录成功，将当前登录信息放入到session中，并跳转页面
				request.session['adminuser'] = user.username
				#print(json.dumps(user))
				return redirect(reverse('index'))
			else:
				context = {'info':'登录密码错误','num':6}
		else:
			context = {'info':'没有找到此用户,请先注册！','num':6}
	except:
		context={'info':'账户不存在,请先注册','num':6}
	print(context)


	return render(request,"myweb/users/login.html",context)

# 会员退出
def logout(request):
	# 清除登录的session信息
	del request.session['adminuser']
	# 跳转登录页面（url地址改变）
	return redirect(reverse('index'))
	# 加载登录页面(url地址不变)
	#return render(request,"myadmin/login.html")
 #====================验证码===============================================
def verifycode(request):
	 #引入随机函数模块
	 import random
	 from PIL import Image, ImageDraw, ImageFont
	 #定义变量，用于画面的背景色、宽、高
	 #bgcolor = (random.randrange(20, 100), random.randrange(
	 #    20, 100),100)
	 bgcolor = (242,164,247)
	 width = 100
	 height = 25
	 #创建画面对象
	 im = Image.new('RGB', (width, height), bgcolor)
	 #创建画笔对象
	 draw = ImageDraw.Draw(im)
	 #调用画笔的point()函数绘制噪点
	 for i in range(0, 100):
		 xy = (random.randrange(0, width), random.randrange(0, height))
		 fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
		 draw.point(xy, fill=fill)
	 #定义验证码的备选值
	 str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	 #随机选取4个值作为验证码
	 rand_str = ''
	 for i in range(0, 4):
	     rand_str += str1[random.randrange(0, len(str1))]
	 #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
	 font = ImageFont.truetype('static/DejaVuSansMono_0.ttf', 21)
	 #font = ImageFont.load_default().font
	 #构造字体颜色
	 fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
	 #绘制4个字
	 draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
	 draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
	 draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
	 draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
	 #释放画笔
	 del draw
	 #存入session，用于做进一步验证
	 request.session['verifycode'] = rand_str
	 """
	 python2的为
	 # 内存文件操作
	 import cStringIO
	 buf = cStringIO.StringIO()
	 """
	 # 内存文件操作-->此方法为python3的
	 import io
	 buf = io.BytesIO()
	 #将图片保存在内存中，文件类型为png
	 im.save(buf, 'png')
	 #将内存中的图片数据返回给客户端，MIME类型为图片png
	 return HttpResponse(buf.getvalue(), 'image/png')

#==========================会员注册页=========================================
def regist(request):
	return render(request,'myweb/users/regist.html')

def doregist(request):
	try:
		ob = Users()
		ob.username = request.POST['account']
		ob.name = request.POST['name']
		#获取密码并md5
		import hashlib
		m = hashlib.md5() 
		m.update(bytes(request.POST['password'],encoding="utf8"))
		ob.password = m.hexdigest()
		ob.email = request.POST['email']
		ob.state = 1
		ob.addtime = time.time()
		ob.save()
		context = {'info':'注册成功！'}
	except:
		context = {'info':'注册失败！'}
	return render(request,"myweb/users/login.html",context)

@csrf_exempt
def ajax(request):
	u = request.POST['username']
	if u != '':
		ob = Users.objects.filter(username=u).count()
		if ob == 0:
			context ={'data':0}
		elif ob >= 1:
			context ={'data':1}

	else:
		context ={'data':2}
	return JsonResponse(context)

#=========================购物车================================================
def shopcart(request):
	context=loadinfo()
	if 'shoplist' not in request.session:
		request.session['shoplist']={}
	return render(request,'myweb/cart/shopcart.html',context)

#添加购物车
def shopcartadd(request,sid):
	#获取要放入购物车中的商品信息
	goods=Goods.objects.get(id=sid)
	shop=goods.toDict()
	shop['m']=int(request.POST['m']) #添加一个购买数量属性
	#从session中获取购物车信息
	if 'shoplist' in request.session:
		shoplist=request.session['shoplist']
	else:
		shoplist={}
	#判断此商品是否在购物车中
	if sid in shoplist:
		#商品数量加一
		shoplist[sid]['m']+=shop['m']
	else:
		#新商品添加
		shoplist[sid]=shop
	#将购物车信息放回到session
	request.session['shoplist']=shoplist
	n=len(request.session['shoplist'].keys())
	print(n)
	print('ok3')
	return redirect(reverse('shopcart'))
#删除购物车
def shopcartdel(request,sid):
	shoplist=request.session['shoplist']
	del shoplist[sid]
	request.session['shoplist']=shoplist
	print('ooooo')
	return redirect(reverse('shopcart'))

#清空购物车
def shopcartclear(request):
	context=loadinfo()
	request.session['shoplist']={}
	return render(request,'myweb/cart/shopcart.html',context)

#改变数量
def shopcartchange(request):
	context=loadinfo()
	shoplist=request.session['shoplist']
	#获取信息
	shopid=request.GET['sid']
	num=int(request.GET['num'])
	if num<1:
		num=1
	shoplist[shopid]['m']=num #改变商品数量
	request.session['shoplist']=shoplist
	return redirect(reverse('shopcart'))

#========================个人中心================================
#个人中心
def personal(request):
	loadinfo()
	list2=[]
	list=Orders.objects.filter(status=0)
	list2=Orders.objects.filter(status=1)
	list = list.filter(uid=request.session['vipuser']['id'])
	list2 = list2.filter(uid=request.session['vipuser']['id'])
	m=list.count()
	m2=list2.count()
	print(list)
	
	print(request.session['vipuser']['id'])
	print("======555555====")
	context={'num':m,"num2":m2}
	return render(request,'myweb/cart/personal.html',context)
#编辑个人信息页面
def personaledict(request):
	loadinfo()
	list=Users.objects.get(username=request.session['adminuser'])
	print(list)
	context={'userlist':list}
	return render(request,'myweb/cart/personaledict.html',context)
#执行个人信息编辑
def personalinsert(request):
	ob=Users.objects.get(id=request.POST['id'])
	ob.name=request.POST['name']
	ob.address=request.POST['address']
	ob.code=request.POST['code']
	ob.phone=request.POST['phone']
	ob.email=request.POST['email']
	ob.save()
	return render(request,'myweb/cart/personal.html')
#个人订单管理
#加载个人订单页面
def personalorders(request):
	loadinfo()
	#从数据库获取order信息
	ob=Orders.objects.filter(uid=request.session['vipuser']['id'])
	context={}
	context['orderlist']=ob
	return render(request,'myweb/cart/personalorders.html',context)
#加载订单详情页面
def ordersdetail(request,oid):
	context=loadinfo()
	list=Detail.objects.filter(orderid=oid)
	for ob in list:
		goods=Goods.objects.get(id=ob.goodsid)
		ob.picname = goods.picname
	context={'detaillist':list}
	return render(request,'myweb/cart/ordersdetail.html',context)
#取消订单
def ordersdelete(request,oid):
	ob=Orders.objects.get(id=oid)
	ob.delete()
	return HttpResponse('取消订单完成')
#确认收货
def orderschange(request,oid):
	ob=Orders.objects.get(id=oid)
	ob.status=2
	ob.save()
	return HttpResponse('确认收货完成')
