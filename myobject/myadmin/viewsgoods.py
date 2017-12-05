from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import Types,Goods
from  myweb.models import Orders,Detail
from PIL import Image
import time,os,json
from django.core.paginator import Paginator

#==========================后台商品类别管理===========================
#浏览后台商品类别
def typesindex(request):
	# 执行数据查询，并放置到模板中
	list = Types.objects.extra(select = {'_has':'concat(path,id)'}).order_by('_has')
	# 遍历查询结果，为每个结果对象追加一个pname属性，目的用于缩进标题
	print(list) #[<Types: Types object>, <Types: Types object>, <Types: Types object>]
	for ob in list:
		ob.pname ='. . . '*(ob.path.count(',')-1)
	context = {"typeslist":list}
	return render(request,'myadmin/type/index.html',context)
#添加商品子类别信息
def typesadd(request,tid):
	# 获取父类别信息，若没有则默认为根类别信息
	if tid == '0':
		context = {'pid':0,'path':'0,','name':'根类别'}
	else:
		ob = Types.objects.get(id=tid)
		context = {'pid':ob.id,'path':ob.path+str(ob.id)+',','name':ob.name}
	return render(request,'myadmin/type/add.html',context)

#执行商品类别信息添加操作
def typesinsert(request):
	# try:
		ob=Types()
		ob.name=request.POST['name']
		print(ob.name)
		ob.pid=request.POST['pid']
		ob.path=request.POST['path']
		ob.save()
		context = {'info':'添加成功！'}
	# except:
	# 	context = {'info':'添加失败！'}
		return render(request,"myadmin/info.html",context)
# 执行类别信息删除
def typesdel(request,tid):
	try:
		#获取被删除商品类别的子类别信息量,如果有数据,就禁止删除
		row=Types.objects.filter(pid=tid).count()
		if row>0:
			context={'info':'删除失败:此类别下还有子类别'}
			return render(request,'myadmin/info.html',context)
		ob = Types.objects.get(id=tid)
		ob.delete()
		context = {'info':'删除成功！'}
	except:
		context = {'info':'删除失败！'}
	return render(request,"myadmin/info.html",context)
# 打开类别信息编辑表单
def typesedit(request,tid):
	try:
		ob = Types.objects.get(id=tid)
		context = {'types':ob}
		return render(request,"myadmin/type/edit.html",context)
	except:
		context = {'info':'没有找到要修改的信息！'}
	return render(request,"myadmin/info.html",context)

# 执行类别信息编辑
def typesupdate(request,tid):
	try:
		ob = Types.objects.get(id=tid)
		ob.name = request.POST['name']
		ob.save()
		context = {'info':'修改成功！'}
	except:
		context = {'info':'修改失败！'}
	return render(request,"myadmin/info.html",context)

#=================后台商品信息管理===========================
#浏览商品信息
#分页
def goodsindex(request,pIndex=1):
	#执行数据查询,并放置到模板
	list=Goods.objects.all()
	#判断并封装搜索条件
	where = [] #定义一个用于维持搜索条件的变量
	if request.GET.get('name','') != '':
		list = list.filter(goods__contains=request.GET.get('name'))
		where.append('goods='+request.GET.get('name'))
	if request.GET.get('company','') != '':
		list = list.filter(company__contains=request.GET['company'])
		where.append('company='+request.GET.get('company'))
	for ob in list:
		ty=Types.objects.get(id=ob.typeid)
		ob.typename=ty.name
	#传入数据和页大小来创建分页对象
	p=Paginator(list,5)
	#判断页号没有值时初始化为1
	if pIndex == '':
		pIndex = 1
	pIndex=int(pIndex) #类型转换
	list2=p.page(pIndex)#获取当前页数据
	plist=p.page_range#获取页码信息
	#封装分页信息
	context={'goodslist':list2,'plist':plist,'pIndex':pIndex}
	return render(request,'myadmin/goods/index.html',context)
# #搜索
# def goodssearch(request,pIndex=1):
# 	#获取商品信息
# 	list=Goods.objects.filter()
# 	#判断并封装搜索条件
# 	where = [] #定义一个用于维持搜索条件的变量
# 	if request.GET.get('name','') != '':
#         list = list.filter(name__contains=request.GET.get('name'))
#         where.append('name='+request.GET.get('name'))
#     if request.GET.get('type','') != '':
#         list = list.filter(type=request.GET['type'])
#         where.append('type='+request.GET.get('type'))

#添加商品信息
def goodsadd(request):
	#获取商品的类别信息
	list=Types.objects.extra(select={'_has':'concat(path,id)'}).order_by('_has')
	context={"typeslist":list}
	#加载商品信息添加表单
	return render(request,'myadmin/goods/add.html',context)
#执行商品信息的添加
def goodsinsert(request):
	# try:
		#执行图片的上传
		myfile = request.FILES.get("picname",None)
		if not myfile:
			return HttpResponse('没有图片上传信息')
		#为上传的图片取名
		filename=str(time.time())+"."+myfile.name.split('.').pop()
		#将图片保存到static中
		destination=open("./static/myadmin/img/"+filename,"wb+")
		#写入图片
		for chunk in myfile.chunks():
			destination.write(chunk)
		destination.close()

		#执行图片的缩放
		im=Image.open("./static/myadmin/img/"+filename)
		# 缩放到375*375:
		im.thumbnail((375, 375))
		# 把缩放后的图像用jpeg格式保存:
		im.save("./static/myadmin/img/"+filename, 'jpeg')
		# 缩放到220*220:
		im.thumbnail((220, 220))
		# 把缩放后的图像用jpeg格式保存:
		im.save("./static/myadmin/img/m_"+filename, 'jpeg')
		# 缩放到220*220:
		im.thumbnail((100, 100))
		# 把缩放后的图像用jpeg格式保存:
		im.save("./static/myadmin/img/s_"+filename, 'jpeg')

		# #缩放到75*75
		# im.thumbnail((75,75))
		# #把所放后的图像用jpeg格式保存
		# im.save("./static/myadmin/img/s_"+filename,'jpeg')

		#执行信息的添加
		ob=Goods()
		ob.typeid=request.POST['typeid']
		ob.goods=request.POST['goods']
		ob.company=request.POST['company']
		ob.descr=request.POST['descr']
		ob.price=request.POST['price']
		ob.picname=filename
		ob.state=1
		ob.store=request.POST['store']
		ob.addtime=time.time()
		ob.save()
		context={'info':'添加成功'}
	# except:
	# 	context={'info':'添加失败'}
		return render(request,'myadmin/info.html',context)
#删除商品信息
def goodsdel(request,uid):
	# try:
		#获取被删除商品信息,先删除图片
		ob=Goods.objects.get(id=uid)
		if ob.state != 1:
			context={'info':'该商品禁止删除'}
			return render(request,'myadmin/info.html',context)
		#执行图片的删除
		os.remove("./static/myadmin/img/"+ob.picname)
		os.remove("./static/myadmin/img/s_"+ob.picname)
		#执行商品信息的删除
		ob.delete()
		context={'info':'删除成功'}
	# except:
	# 	context={'info':'删除失败'}
		return render(request,'myadmin/info.html',context)
#编辑商品信息
def goodsedit(request,uid):
	# try:
		#获取要编辑的信息
		ob=Goods.objects.get(id=uid)
		#获取商品的类别信息
		list=Types.objects.extra(select={"_has":'concat(path,id)'}).order_by('_has')
		#放置信息,加载模板
		context={'goods':ob,'typeslist':list}
		return render(request,'myadmin/goods/edit.html',context)
	# except:
	# 	context={'info':'获取商品信息失败'}
		return render(request,'myadmin/info.html',context)
#执行商品信息的编辑
def goodsupdate(request,uid):
	try:
		#获取原图片名
		oldpicname=request.POST['oldpicname']
		#判断是否有文件上传
		myfile=request.FILES.get("picname",None)
		if not myfile :
			filename=oldpicname
		else:
			#执行上传处理
			filename=str(time.time())+"."+myfile.name.split('.').pop()
			destination=open("./static/myadmin/img/"+filename,"wb+")
			#分块写入文件
			for chunk in myfile.chunks():
				destination.write(chunk)
			destination.close()
			#执行图片的缩放
			im=Image.open("./static/myadmin/img/"+filename)
			# 缩放到375*375:
			im.thumbnail((375, 375))
			# 把缩放后的图像用jpeg格式保存:
			im.save("./static/myadmin/img/"+filename, 'jpeg')
			# 缩放到220*220:
			im.thumbnail((220, 220))
			# 把缩放后的图像用jpeg格式保存:
			im.save("./static/myadmin/img/m_"+filename, 'jpeg')
			# 缩放到220*220:
			im.thumbnail((100, 100))
			# 把缩放后的图像用jpeg格式保存:
			im.save("./static/myadmin/img/s_"+filename, 'jpeg')



		ob=Goods.objects.get(id=uid)
		ob.typeid=request.POST['typeid']
		ob.goods=request.POST['goods']
		ob.company=request.POST['company']
		ob.descr=request.POST['descr']
		ob.price=request.POST['price']
		ob.picname=filename
		ob.state=request.POST['state']
		ob.store=request.POST['store']
		ob.save()
		
		context={'info':'编辑成功'}
		print('ok2')
		#判断删除老图片
		if myfile:
			os.remove("./static/myadmin/img/"+oldpicname)
			os.remove("./static/myadmin/img/s_"+oldpicname)
	except:
		context={'info':'编辑失败'}
		os.remove("./static/myadmin/img/"+picname)
		os.remove("./static/myadmin/img/s_"+picname)
	return render(request,'myadmin/info.html',context)

#后台订单管理页
def orders(request):
	list=Orders.objects.all()
	context={'orderlist':list}
	return render(request,'myadmin/orders/ordersindex.html',context)
#加载订单详情表单
def ordersdetail(request,oid):
	list=Detail.objects.filter(orderid=oid)
	context={'detaillist':list}
	return render(request,'myadmin/orders/ordersdetail.html',context)
#加载订单状态编辑表单
def ordersedict(request,oid):
	ob=Orders.objects.get(id=oid)
	print(ob.status)
	print('=======')
	context={'status':ob}
	return render(request,'myadmin/orders/ordersedict.html',context)
#执行订单信息的编辑
def ordersinsert(request,oid):
	ob=Orders.objects.get(id=oid)
	ob.status=request.POST['status']
	ob.save()
	context={'info':'状态修改成功!'}
	return render(request,'myadmin/info.html',context)
