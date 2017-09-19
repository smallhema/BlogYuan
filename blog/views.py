from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from  blog import models
from BlogYuan import settings
import json
from django.contrib.auth import authenticate,login,logout

from blog import forms
from blog.models import *
from django.db.models import F,Q

def func_class(request):

    return {"func":settings.FUNCTION}



def index(request,**kwargs):

    type_choices=Article.type_choices
    print("kwargs",kwargs)
    current_type_choices_id = int(kwargs.get("article_type_id",0))

    #方式1：
    # current_type_choices_id = int(kwargs.get("type_id"))
    # article_list = models.Article.objects.all()
    #
    # if current_type_choices_id:
    #
    #     article_list=models.Article.objects.filter(article_type_id=current_type_choices_id)
    # 方式2：

    article_list=Article.objects.filter(**kwargs)
    article_list=Article.objects.all()
    lasted_article=article_list[0:5]
    author_recommand=UserInfo.objects.all()[0:3]
    dateRet=Article.objects.archive()


    return render(request,"index.html",{
        "type_choices":type_choices,
        "article_list":article_list,
        "current_type_choices_id":current_type_choices_id,
        "lasted_article":lasted_article,
        "author_recommand":author_recommand,
        "dateRet":dateRet,
    })





def log_in(request):
    # print(request.path)
    real_path=request.path.replace("/login","")
    # print(real_path)
    if request.is_ajax():

        username=request.POST.get("username")
        password=request.POST.get("password")
        valid_code=request.POST.get("valid_code")
        ajax_response={"user":None,"errors":""}

        if valid_code.upper()== request.session.get("valid_code").upper():

            user=authenticate(username=username,password=password)


            if user:
                login(request, user)
                ajax_response["user"]=user.username
            else:
                ajax_response["errors"]="用户名或者密码错误！"

        else:
            ajax_response["errors"]="验证码错误！"



        return HttpResponse(json.dumps(ajax_response))


    return render(request,"login.html",locals())








def reg(request):

    if request.method=="POST":
        form_obj=forms.RegForm(request,request.POST)   # 实例form对象
        response={"flag":False,"errors":""}


        if form_obj.is_valid():
            #操作
            print(form_obj.cleaned_data) # {"username":"ffdsgfds","password":2134szdf,...}
            username=form_obj.cleaned_data["username"]
            password=form_obj.cleaned_data["password"]
            email=form_obj.cleaned_data["email"]
            file_obj=request.FILES.get("img")

            print("file_OBJ",file_obj)
            UserInfo.objects.create_user(username=username,password=password,email=email,avatar=file_obj)
            response["flag"]=True

        else:
            errors=form_obj.errors       #  ERRORdict:  {"username":[],"password":[],....}
            response["errors"]=errors
            print("errors:-----",errors)
        return HttpResponse(json.dumps(response))

    form_obj=forms.RegForm(request)
    return render(request,"reg.html",{"form_obj":form_obj})

def valid_code(request):

    # 方式1：

    # with open("blog/static/img/valid.png","rb") as f:
    #     data=f.read()
    # return HttpResponse(data)


    # 方式2：
    # from PIL import Image
    #
    # # 创建图片对象
    # img = Image.new(mode='RGB', size=(120, 30), color=(50, 120, 255))
    #
    # #保存图像
    # with open('code.png', 'wb') as f:
    #     img.save(f, format='png')
    #
    # # 读文件
    # with open("code.png","rb") as f_read:
    #     data=f_read.read()


    #  # 方式三：
    # from PIL import Image
    # from io import BytesIO
    # f=BytesIO()
    # img = Image.new(mode='RGB', size=(120, 30), color=(120, 120, 255))
    #
    # img.save(f,"png")


    #方式三：
    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO
    import random
    f=BytesIO()
    img = Image.new(mode='RGB', size=(120, 30), color=(random.randint(0,255), random.randint(0,255),random.randint(0,255)))

    draw = ImageDraw.Draw(img, mode='RGB')

    font=ImageFont.truetype("blog/static/bootstrap/fonts/kumo.ttf",28)

    code_list = []
    for i in range(5):
        char = random.choice([chr(random.randint(65, 90)), str(random.randint(1, 9))])
        code_list.append(char)
        draw.text([i * 24, 0], char, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                  font=font)

    img.save(f,"png")

    valid_code=''.join(code_list)

    request.session["valid_code"]=valid_code


    return HttpResponse(f.getvalue())


######################################homeSite=============




def homeSite(request,user_site,**kwargs):
    # 一对多的正反向查询

    # article = Article.objects.filter(nid=3).first()
    # print(article.category)  # 当前这篇文章的类别（一个对象）
    #
    # category_obj = Category.objects.filter(title="java").first()
    # print(category_obj.article_set.all())


    # http://127.0.0.1:9999/blog/yuan
    # user_site:  "yuan"

    # 一对一查询
    # 获取用户对象


    # blog_obj=Blog.objects.filter(nid=1).first()
    # print(blog_obj.user.username)

    user=UserInfo.objects.filter(username=user_site).first()



    # if not user:
    #     return render(request,"NotFound.html")

    # 1 获取当前站点对象


    # print(user.blog.title) # egon的个人博客

    currentBlog=Blog.objects.filter(user=user).first()

    # 2 获取当前站点文章

    #print(currentBlog.article_set.all())

    article_list=Article.objects.filter(blog=currentBlog)
    print(article_list)

    # 3 获取当前站点的所有分类：
    # print(currentBlog.category_set.all())

    category_list=Category.objects.filter(blog=currentBlog)
    # print(category_list)

    # 4 查询 每一个分类下的名称以及对应的文章个数

    # ret=[]
    # for category in category_list:
    #     temp=[]
    #     temp.append(category.title)
    #     temp.append(category.article_set.all().count())
    #     ret.append(temp)
    #
    # print(ret) # [['python', 2], ['java', 2], ['ui', 1]]


    from django.db.models import Avg, Sum, Min, Max, Count

    categoryRet=Article.objects.filter(blog=currentBlog).values_list("category__title","category__nid").annotate(Count("nid"))
    print(categoryRet) #<QuerySet [('java', 2), ('python', 1), ('ui', 1)]>


    # 5 查询每一个标签以及对应的文章个数

    #tag_list=Tag.objects.filter(blog=currentBlog)

    # ret=[]
    # for tag in tag_list:
    #     temp=[]
    #
    #     temp.append(tag.title)
    #     count=Article.objects.filter(blog=currentBlog).filter(tags__title=tag.title).count()
    #     temp.append(count)
    #     ret.append(temp) #
    # print(ret) # [['函数', 2], ['作用域', 3], ['对象', 2]]



    tagRet=Article.objects.filter(blog=currentBlog).values_list("tags__title","tags__nid").annotate(Count("nid"))
    print(tagRet) # <QuerySet [('作用域', 3), ('函数', 2), ('对象', 2)]>


     # 查询 文章日期 ： 2012-12-12

    # ret=Article.objects.filter(blog=currentBlog).values("create_time")
    #
    # l=[]
    # for i in ret:
    #     #print(i["create_time"])
    #     date=i["create_time"]
    #
    #     t=date.strftime("%Y-%m-%d")
    #     print(t)
    #
    #     if t not in l:
    #         l.append(t)
    #
    # print(l)


    dateRet=Article.objects.archive(blog=currentBlog)
    # mysql格式
    # dateRet=Article.objects.filter(blog=currentBlog).extra(select={"c":"data_format(create_time,'%%Y-%%m')"}).values("c").annotate(ct=Count("nid"))
    # sqlite格式
    # dateRet=Article.objects.filter(blog=currentBlog).extra(select={"c":"strftime('%%Y-%%m',create_time)"}).values("c").annotate(ct=Count("nid"))


    print("++++++++++",dateRet)


    print(kwargs)
    if kwargs.get("condition"):
        con=kwargs.get("condition")
        if con=="category":
            article_list=Article.objects.filter(blog=currentBlog,category__nid=kwargs.get("para"))
        elif con=="tag":
            article_list=Article.objects.filter(blog=currentBlog,tags__nid=kwargs.get("para"))
        else:
            article_list=[]
            for i in Article.objects.filter(blog=currentBlog):
                if kwargs.get("para")==i.create_time.strftime("%Y-%m"):
                    # print(i)
                    article_list.append(i)
    return render(request,"homeSite.html",locals())


def articleDetail(request,user_site,article_id):
    article_obj=Article.objects.filter(nid=article_id).first()
    comment_list=Comment.objects.filter(article_id=article_id)
    # msg_list=[]
    # comment_dict={}
    # result=[]
    # for i in comment_list:
    #     msg_dict = {}
    #     msg_dict["id"]=i.nid
    #     msg_dict["content"]=i.content
    #     if i.parent_id:
    #         msg_dict["parent_id"] = i.parent_id.nid
    #     else:
    #         msg_dict["parent_id"] = None
    #     msg_dict["child"]=[]
    #     # print(msg_dict)
    #     msg_list.append(msg_dict)
    #
    # for item in msg_list:
    #     comment_dict[item["id"]]=item
    #
    # for item in msg_list:
    #     pid=item["parent_id"]
    #     if pid:
    #         comment_dict[pid]["child"].append(item)
    #     else:
    #         result.append(item)
    #
    # from comment import comment_tree
    # comment_str=comment_tree(result)

    return render(request,"articleDetail.html",locals())

def log_out(request):
    logout(request)
    return redirect("/index/")

def poll(request):
    print('poll 开始')
    user_id=request.user.nid
    article_id=request.POST.get("article_id")
    if ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id):
        response={"flag":False}
    else:
        ArticleUpDown.objects.create(
            user_id=user_id,
            article_id=article_id
        )
        Article.objects.filter(nid=article_id).update(up_count=F("up_count")+1)
        response={"flag":True}
    return HttpResponse(json.dumps(response))

def comment(request):
    print('comment 开始')
    user_id=request.user.nid
    article_id=request.POST.get("article_id")
    comment_content=request.POST.get("comment_content")
    print(comment_content)
    Comment.objects.create(
        user_id=user_id,
        article_id=article_id,
        content=comment_content,
    )
    Article.objects.filter(nid=article_id).update(comment_count=F("comment_count")+1)
    return HttpResponse("ok")

