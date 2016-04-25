from flask import Flask
from flask import session
from flask.ext.session import Session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from sqlalchemy import or_
from datetime import *

#sqlurl = 'sqlite:////Users/fangxin/Documents/GEStore/gestore.db'
sqlurl = 'sqlite:////Users/fangxin/Documents/GEStore/gestorebackup.db'
# sqlurl = "mysql://root:@localhost:3306/gestore?charset=utf8"
app =Flask(__name__)
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=sqlurl
app.config['SECRET_KEY'] = 'KEY'
Session(app)
db=SQLAlchemy()
db.init_app(app)


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlurl
    db.init_app(app)
    migrage = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
class OrderTool(db.Model):
    __tablename__='OrderTool'
    order_id = db.Column(db.Integer, db.ForeignKey('OrderTable.OrderID'), primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('ToolTable.ToolID'), primary_key=True)
    timestamp = db.Column(db.DateTime, default = datetime.now)

class StaffTable(db.Model):
    __tablename__  = "StaffTable"
    StaffID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(128), nullable=False)
    HireDate = db.Column(db.DateTime)
    Password = db.Column(db.String(128), nullable=False)
    Picture = db.Column(db.String(128))
    Position = db.Column(db.String(128))
    Remarks = db.Column(db.String(128))
    PhoneNumber = db.Column(db.String(128))

class ToolboxTable(db.Model):
    __tablename__ = "ToolboxTable"
    ToolboxID = db.Column(db.Integer, primary_key=True)
    BoxModel = db.Column(db.String(128))
    PurchaseDate = db.Column(db.DateTime)
    Picture = db.Column(db.String(128))
    ServiceLife = db.Column(db.String(128))
    Status = db.Column(db.String(128))
    Description = db.Column(db.String(128))
    Price = db.Column(db.Float)
    BrokenOrLostDate = db.Column(db.DateTime)

class ToolTable(db.Model):
    __tablename__ = "ToolTable"
    ToolID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(128))
    PurchaseDate = db.Column(db.DateTime)
    Picture = db.Column(db.String(128))
    ServiceLife = db.Column(db.String(128))
    Status = db.Column(db.String(128))
    Description = db.Column(db.String(128))
    ToolCenterID = db.Column(db.Integer)
    MinQuant = db.Column(db.Integer)
    Price = db.Column(db.Float)
    BrokenOrLostDate = db.Column(db.DateTime)
    orders = db.relationship('OrderTool', foreign_keys = [OrderTool.tool_id], backref = db.backref('toolordered', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')

class OnsiteTable(db.Model):
    __tablename__ = "OnsiteTable"
    OnsiteID = db.Column(db.Integer, primary_key = True)
    ToolKeeperID = db.Column(db.Integer, db.ForeignKey('StaffTable.StaffID'))
    ToolboxID = db.Column(db.Integer, db.ForeignKey('ToolboxTable.ToolboxID'))
    EnginnerID = db.Column(db.Integer, db.ForeignKey('StaffTable.StaffID'))
    ToolID = db.Column(db.Integer, db.ForeignKey('ToolTable.ToolID'))
    Address = db.Column(db.String(128))
    LendingTime = db.Column(db.DateTime)
    ReturnTime = db.Column(db.DateTime)
    ReturnStatus = db.Column(db.String(128))
    Remarks = db.Column(db.String(128))
    OrderID = db.Column(db.Integer,db.ForeignKey('OrderTable.OrderID'))


class OrderTable(db.Model):
    __tablename__ = "OrderTable"
    OrderID = db.Column(db.Integer, primary_key=True)
    OnsiteTime = db.Column(db.Date)
    Location = db.Column(db.String(128))
    Description = db.Column(db.String(256))
    Title = db.Column(db.String(128))
    ReservationTime = db.Column(db.DateTime)
    ClientID = db.Column(db.Integer,db.ForeignKey('StaffTable.StaffID'))
    RequestAcceptTime = db.Column(db.DateTime)
    ManagerID = db.Column(db.Integer, db.ForeignKey('StaffTable.StaffID'))
    EngineerConfirmTime = db.Column(db.DateTime)
    DutyEngineerID = db.Column(db.Integer, db.ForeignKey('StaffTable.StaffID'))
    PredictedReturnTime=db.Column(db.Date)
    WhetherExpress=db.Column(db.String(128))
    OtherEngineerID = db.Column(db.Integer, db.ForeignKey('StaffTable.StaffID'))
    ToolsReservationTime = db.Column(db.DateTime)
    ToolsReservationID = db.Column(db.Integer, db.ForeignKey('ToolTable.ToolID'))
    KeeperConfirmTime=db.Column(db.DateTime)
    ToolKeeperID=db.Column(db.Integer, db.ForeignKey('StaffTable.StaffID'))
    TaskBeginTime = db.Column(db.DateTime)
    TaskEndTime = db.Column(db.DateTime)
    TaskStatus = db.Column(db.String(128))
    ClientConfirmTime = db.Column(db.DateTime)
    ClientStatus = db.Column(db.String(128))
    ManagerConfirmTime = db.Column(db.DateTime)
    ManagerStatus = db.Column(db.String(128))
    Remarks = db.Column(db.String(128))
    Value = db.Column(db.String(128))
    tools = db.relationship('OrderTool', foreign_keys = [OrderTool.order_id], backref = db.backref('ordertable', lazy='joined'), lazy='dynamic', cascade = 'all, delete-orphan')

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception,e:
            print e
            db.session.rollback()
            return 2 

    def addtool(self,tool):
        try:
            lp = self.tools.filter_by(tool_id = tool.ToolID).first()
            if lp is None:
                lp = OrderTool(order_id = self.OrderID,  tool_id = tool.ToolID)
                db.session.add(lp)
                db.session.commit()
                return 0
            else:
                return 1
        except Exception, e:
            print e
            db.session.rollback()
            return 






if __name__ == "__main__":
    manager.run()