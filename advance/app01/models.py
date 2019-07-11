from django.db import models

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=32,null=False)
    price = models.DecimalField(max_digits=5,decimal_places=2,default=50.00)


    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.IntegerField(default=15)
    # 通过through，through_fields来指定使用我创建的第三张表来构建多对多的关系
    books = models.ManyToManyField(to='Book' ,through='Author_Book',through_fields=('author','book'))
    # 第一个字段： 多对多设置在哪一张表里， 第三张表通过什么字段找到这张表 就把这个字段写在前面

# 自己动手 创建作者和书关联的第三张表
# 此时 在ORM层面
class Author_Book(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(to='Author')
    book = models.ForeignKey(to='Book')
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.author

    class Meta:
        # 建立唯一约束
        unique_together = ("author", "book")


class UserInfo(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False)
    pwd = models.CharField(max_length=32, default="doushidsb")
    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=11, null=True)
    city =models.CharField(null=True,max_length=11)
    def __str__(self):
        return self.name



class City(models.Model):
    name = models.CharField(max_length=16, null=False, unique=True)

    def __str__(self):
        return self.name