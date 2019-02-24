# -*- encoding=UTF-8 -*-

from nowstagram import app,db
from flask_script import Manager
from sqlalchemy import or_,and_
from nowstagram.models import User,Image,Comment
#from nowstagram.models import User
import random
import unittest

manager = Manager(app)

def get_image_url():
    return 'http://images.nowcoder.com/head/'+str(random.randint(0,1000))+'m.png'

@manager.command
def run_test():
    db.drop_all()
    db.create_all()
    tests=unittest.TestLoader().discover('./')
    unittest.TextTestRunner().run(tests)
    pass

@manager.command
def init_database():
    #数据库清空
    db.drop_all()
    #数据库创建
    db.create_all()
    #数据库添加数据：用户名和密码（这个顺序见nowstagram.models里面User类的初始化顺序）
    for i in range(0,100):
        db.session.add(User('User'+str(i),'a'+str(i)))
        for j in range(0,10):
            db.session.add(Image(get_image_url(),i+1))
            for k in range(0,3):
                db.session.add(Comment('This is a comment '+str(k),1+10*i+j,i+1))
    #提交事务,如果不提交的话等于没做
    db.session.commit()

    #更新User表的username属性
    for i in range(50,100,2):
        user=User.query.get(i)
        user.username='[New1]'+user.username
    #for i in range(51, 100, 2):
        #User.query.filter_by(id=i).update({'username':'[New2]'})
    User.query.filter_by(id=51).update({'username': '[New2]'})
    db.session.commit()

    #删除评论
    for i in range(50,100,2):
        comment=Comment.query.get(i+1)
        db.session.delete(comment)
    db.session.commit()

    #查询数据
    print 1,User.query.all()
    print 2,User.query.get(3)
    print 3,User.query.filter_by(id=5).first()
    print 4,User.query.order_by(User.id.desc()).offset(1).limit(2).all()
    print 32, User.query.filter_by(id=5)
    print 42, User.query.order_by('id desc').limit(2)
    print 5,User.query.filter(User.username.endswith('0')).limit(3).all()
    print 6,User.query.filter(or_(User.id==88,User.id==99)).all()
    print 7, User.query.filter(and_(User.id > 88, User.id < 93)).all()
    print 8, User.query.filter(and_(User.id > 88, User.id < 93)).first_or_404()#有的话就输出第一个没有的话就输出404
    print 9,User.query.paginate(page=1,per_page=10).items
    print 9, User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items
    user=User.query.get(1)
    print 10,user.images
    image=Image.query.get(1)
    print 11,image.user




if __name__=='__main__':
    manager.run()

