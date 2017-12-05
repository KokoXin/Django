from django.db import models
#用户信息模型
class Users(models.Model):
    username = models.CharField(max_length=32)
    name = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    sex = models.IntegerField(default=1)
    address = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=50)
    state = models.IntegerField(default=1)
    addtime = models.IntegerField()

    class Meta:
        db_table = "users"  # 更改表名
    def toUsers(self):
        return {'id':self.id,'code':self.code,'name':self.name,'address':self.address,'phone':self.phone,'email':self.email,'sex':self.sex}


#商品类别模型
class Types(models.Model):
    
    name = models.CharField(max_length=32)
    pid = models.IntegerField()
    path = models.CharField(max_length=255)


    class Meta:
        db_table = "type"


#商品信息模型
class Goods(models.Model):
    typeid = models.IntegerField()
    goods = models.CharField(max_length = 32)
    company = models.CharField(max_length = 50)
    descr = models.TextField()
    price = models.FloatField()
    picname = models.CharField(max_length = 255)
    state = models.IntegerField(default = 1)
    store = models.IntegerField(default = 0)
    num = models.IntegerField(default = 0)
    clicknum = models.IntegerField(default = 0)
    addtime = models.IntegerField()

    class Meta:
        db_table = "goods" 
    def toDict(self):
        return {'id':self.id,'goods':self.goods,'picname':self.picname,'price':self.price}

#订单表
class Orders(models.Model):
    uid = models.IntegerField()
    linkman = models.CharField(max_length = 32)
    address = models.CharField(max_length = 255)
    code = models.CharField(max_length = 6)
    phone = models.CharField(max_length = 16)
    addtime = models.IntegerField()
    total = models.FloatField()
    status = models.IntegerField()
    class Meta:
        db_table = 'orders'  #更改表名
    def doOrders(self):
        orders = {'id':self.id,'uid':self.uid,'linkman':self.linkman,'address':self.address,'code':self.code,'phone':self.phone,'addtime':self.addtime,'total':self.total,'status':self.status}
        return orders
        
#订单详情表
class Detail(models.Model):
    orderid = models.IntegerField()
    goodsid = models.IntegerField()
    name = models.CharField(max_length = 32)
    price = models.FloatField()
    num = models.IntegerField()

    class Meta:
        db_table = 'detail'  #更改表名
    def doDetail(self):
        detail = {'id':self.id,'orderid':self.orderid,'goodsid':self.goodsid,'name':self.name,'price':self.price,'num':self.num}
        return detail
