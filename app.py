#!--*-- coding:utf-8 --*--
from flask import Flask
from flask import session,Session
from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify
from flask import redirect
from flask import url_for
import time
import datetime
from model import *

#from flask.ext.sqlalchemy import SQLAlchemy
# app=Flask(__name__)
#db = SQLAlchemy(app1)
def get_now_time():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

@app.route( '/login',methods=['POST','GET'])
def login():
    return render_template('login.html')

@app.route( '/logout',methods=['POST','GET'])
def logout():
    return jsonify({
        "Result": True
        })

@app.route( '/getordertool',methods=['POST','GET'])
def getordertool():
    ntool = ToolTable.query.filter_by(ToolID = 200005).first()
    a = OrderTable.query.filter_by(OrderID = 86).first()
    a.addtool(ntool)
    b = a.tools.all()
    result = []
    for temp in b:
       result.append(temp.tool_id)
    
    return jsonify({
        "Result": result
        })

@app.route('/whoAmI',methods=['POST','GET'])
def who_am_i():
    userid = session.get('userid')
    print userid
    st = StaffTable.query.filter_by(StaffID=userid).first()
    if st!=None:
        StaffID = st.StaffID if st.StaffID!=None else ""
        Position = st.Position if st.Position!=None else ""
        Name = st.Name if st.Name != None else ""
        Picture = st.Picture if st.Picture!=None else ""
        Remarks= st.Remarks if st.Remarks!=None else ""
        HireDate= st.HireDate if st.HireDate!=None else ""
        PhoneNumber= st.PhoneNumber if st.PhoneNumber!=None else ""
    return jsonify({
        "StaffID": StaffID,
        'Position': Position,
        'Name': Name,
        'Picture': Picture,
        'Remarks': Remarks,
        'HireDate': HireDate,
        'PhoneNumber': PhoneNumber
    })

 
@app.route( '/clientPersonalCenter',methods=['POST','GET'])
def person_center():
    return render_template('clientPersonCenter.html')

@app.route( '/managerPersonalCenter',methods=['POST','GET'])
def manager_personal_center():
    return render_template('managerPersonalCenter.html')

@app.route( '/clientOrderPage',methods=['POST','GET'])
def client_order_page():
    return render_template('clientOrderPage.html')

@app.route('/newRequests', methods=['POST', 'GET'])
def new_requests():
    return render_template('newRequests.html')

@app.route('/managerOrderPage', methods=['POST', 'GET'])
def manager_order_page():
    return render_template('managerOrderPage.html')

@app.route('/engineerPersonalCenter', methods=['POST', 'GET'])
def engineer_personal_center():
    return render_template('engineerPersonalCenter.html')

@app.route('/engineerOrderPage', methods=['POST', 'GET'])
def engineer_order_page():
    return render_template('engineerOrderPage.html')

@app.route( '/MakeAReservation',methods=['POST','GET'])
def make_a_reservation():
    return render_template('MakeAReservation.html')


@app.route( '/enrollOtherEngineers',methods=['POST','GET'])
def enroll_other_engineer():
    return render_template('enrollOtherEngineers.html')

@app.route('/clientReservation', methods=['POST', 'GET'])
def client_reservation():
    try:
        location = request.args.get('Location')
        date = request.args.get('Date') 
        date_part = date.split('-')
        title = request.args.get('Title')
        description = request.args.get('Description')
        #time = get_now_time()
        # print location,title,description #for test
        #newOrder = OrderTable(OrderID=86,Location =location, Title = title,Description=description,Date=date)
        #newOrder.add()
        st = OrderTable.query.filter_by(OrderID=86).first()
        if st!=None:
            st.Location = location
            st.Title = title
            st.Description = description
            st.OnsiteTime = datetime.date(int(date_part[0]), int(date_part[1]), int(date_part[2]))
            st.ReservationTime = datetime.datetime.now()
        st.add()
        print st.ReservationTime #for test
    except Exception, e:
        print e
    return jsonify({
        'Result': True
    })
@app.route('/orderInformation', methods=['POST', 'GET'])
def order_information():
    st = OrderTable.query.filter_by(OrderID=86).first()
    if st!=None:
        OrderID = st.OrderID if st.OrderID!=None else ""
        Title = st.Title if st.Title!=None else ""
    #print OrderID,Title #for test 
    return jsonify({
        "Orders": [{
            'OrderID': OrderID,
            'Title': Title
        }]
    })

@app.route('/searchTools', methods=['POST', 'GET'])
def search_tools():
    key = request.args.get('Key')
    #print key#for test
    st = ToolTable.query.filter(or_(ToolTable.ToolID == key,ToolTable.Name == key)).all()
    if st!=None:
        orderResult = []  
        for temp in st:
            ToolID = temp.ToolID if temp.ToolID!=None else ""
            Name = temp.Name if temp.Name!=None else ""
            Picture = temp.Picture if temp.Picture!=None else ""
            output = {  'ToolID': ToolID,'Name': Name,'Picture':Picture}
            orderResult .append(output)
        return jsonify({
            "Tools":orderResult,
            "Error":""
        })

@app.route('/accurateDescription',methods=['POST','GET'])
def accurate_description():
    inputid = request.args.get('inputID')
    print inputid
    st = ToolTable.query.filter_by(ToolID=inputid).first()
    if st!=None:
        ToolID = st.ToolID if st.ToolID!=None else ""
        Description = st.Description if st.Description != None else "Good"
        Picture = st.Picture if st.Picture!=None else ""
        #Number= st.PhoneNumber if st.PhoneNumber!=None else ""
    return jsonify({
        "ToolID": ToolID,
        'Description': Description,
        'Picture': Picture,
        'Number': '3'
    })


# @app.route('/accurateDescription', methods=['POST', 'GET'])
# def accurate_description():
#     inputid = request.args.get('inputID')
#     st = ToolTable.query.filter_by(ToolID = inputid).first()
#     if st!=None:
#         ToolID = st.ToolID if st.ToolID!=None else ""
#         Name = st.Name if st.Name!=None else ""
#         Picture = st.Picture if st.Picture!=None else ""
#         Status = st.Status if st.Status!=None else ""
#         Description = st.Description if st.Description!=None else ""
#         output = {  'ToolID': ToolID,'Name': Name,'Status':Status,  'Picture':Picture,'Description':Description}
#         return jsonify({
#             "Orders":output
#         })

@app.route('/confirmReservingTools', methods=['POST', 'GET'])
def confirm_reserving_tools():
    inputid = request.args.get('inputID')
    st = ToolTable.query.filter_by(ToolID = inputid).all()
    if st!=None:
        return jsonify({
            'Result': True
        })   

@app.route('/otherEngineerSearch', methods=['POST', 'GET'])
def other_engineer_search():
    name = request.args.get('Name')
    st = StaffTable.query.filter_by(Name = name).all()
    if st!=None:
        orderResult = []  
        for temp in st:
            StaffID = temp.StaffID if temp.StaffID!=None else ""
            Name = temp.Name if temp.Name!=None else ""
            Picture = temp.Picture if temp.Picture!=None else ""
            output = {  'StaffID': StaffID,'Name': Name,'Picture':Picture}
            orderResult .append(output)
        return jsonify({
            "Engineers":orderResult,
            "Error":""
        })


@app.route('/otherEngineerConfirm', methods=['POST', 'GET'])
def other_engineer_confirm():
    engineerid = request.args.get('EngineerID')
    st = OrderTable.query.filter_by(OrderID = 86).first()
    if st!=None:
        st.OtherEngineerID = engineerid
    st.add()
    return jsonify({
        'Result': True
    })  

@app.route('/DateForReservation', methods=['POST', 'GET'])
def date_for_reservation():
    location = request.args.get('Location')
    date = request.args.get('Date')
    st = OrderTable.query.filter_by(OrderID = 86).first()
    if st!=None:
        st.PredictedReturnTime = date
    st.add()
    return jsonify({
        'Result': "High"
    }) 

@app.route('/finishEnrollEngineer', methods=['POST', 'GET'])
def finish_enroll_engineer():
    location = request.args.get('Location')
    date = request.args.get('Date')
    st = OrderTable.query.filter_by(OrderID = 86).first()
    if st!=None:
        st.PredictedReturnTime = date
    st.add()
    return jsonify({
        'Result': "High"
    }) 

@app.route('/expressInfo', methods=['POST', 'GET'])
def express_info():
    result = request.args.get('Result')
    st = OrderTable.query.filter_by(OrderID = 86).first()
    if st!=None:
        st.WhetherExpress = result
    st.add()
    return jsonify({
        'Result': True
    }) 

@app.route('/engineerConfirmAccept', methods=['POST', 'GET'])
def engineer_confirm_accept():
    st = OrderTable.query.filter_by(OrderID = 86).first()
    if st!=None:
        st.EngineerConfirmTime = datetime.datetime.now()
        st.DutyEngineerID = session.get('userid') #how to remember dutyengineerid
    st.add()
    return jsonify({
        'Result': True
    }) 

@app.route('/ToolsInCurrentOrder', methods=['POST', 'GET'])
def tools_in_current_order():
    st = OrderTable.query.filter_by(OrderID = 86).first()
    if st!=None:
        st.EngineerConfirmTime = datetime.datetime.now()
        st.DutyEngineerID = session.get('userid') #how to remember dutyengineerid
    st.add()
    return jsonify({
        "Error": "",
        "Tools": [{
            'ToolID': "200000",
            'Name': "A",
            'Picture': "/static/images/tool/t1.jpg"
            }]
        })

@app.route('/EngineerReturnTools', methods=['POST', 'GET'])
def engineer_return_tools():
    returnstatus = request.args.get('ReturnStatus')
    toolid = request.args.get('ToolID')
    st = ToolTable.query.filter_by(ToolID = toolid).first()
    if st!=None:
        st.ReturnStatus = returnstatus
    st.add()
    return jsonify({
        'Result': True
    }) 

@app.route('/EngineerFinish', methods=['POST', 'GET'])
def engineer_finish():
    st = OrderTable.query.filter_by(OrderID = 86).first()
    if st!=None:
        st.TaskStatus = True
        st.TaskEndTime = datetime.datetime.now()
    st.add()
    return jsonify({
        'Result': True
    }) 

@app.route('/keeperConfirmAccept', methods=['POST', 'GET'])
def keeper_confirm_accept():
    st = OrderTable.query.filter_by(OrderID = 86).first()
    if st!=None:
        st.KeeperConfirmTime = datetime.datetime.now()
        st.ToolkeeperID = userid
    st.add()
    return jsonify({
        'Result': True
    }) 

@app.route('/chooseOrderID', methods=['POST', 'GET'])
def choose_order_id():
    orderid = request.args.get('OrderID')
    st = OrderTable.query.filter_by(OrderID = 86).all()
    # newOrder = OrderTable(OrderID=orderid)
    # newOrder.add()
    if st!=None:
        return jsonify({
            'Result': True
        })
@app.route('/currentOrder', methods=['POST', 'GET'])
def current_order():
    st = OrderTable.query.filter_by(OrderID=86).first()
    #RequestAcceptTimelist = OrderTable.query.filter_by(ClientID = 10009).all()
    print st.OrderID
    if st!=None:
        OrderID = st.OrderID if st.OrderID!=None else ""
        OnsiteTime = st.OnsiteTime if st.OnsiteTime!=None else ""
        Location = st.Location if st.Location != None else ""
        Title = st.Title if st.Title!=None else ""
        Description= st.Description if st.Description!=None else ""
        ReservationTime = st.ReservationTime if st.ReservationTime != None else ""
        RequestAcceptTime = st.RequestAcceptTime if st.RequestAcceptTime!=None else ""
        EngineerConfirmTime = st.EngineerConfirmTime if st.EngineerConfirmTime!=None else ""
        TaskBeginTime = st.TaskBeginTime if st.TaskBeginTime != None else ""
        TaskEndTime = st.TaskEndTime if st.TaskEndTime!=None else ""
        ClientConfirmTime= st.ClientConfirmTime if st.ClientConfirmTime!=None else ""
        PredictedReturnTime = st.PredictedReturnTime if st.PredictedReturnTime != None else ""
        KeeperConfirmTime = st.KeeperConfirmTime if st.KeeperConfirmTime!=None else ""
        ManagerConfirmTime = st.ManagerConfirmTime if st.ManagerConfirmTime != None else ""
        TaskStatus = st.TaskStatus if st.TaskStatus!=None else ""
        ClientStatus= st.ClientStatus if st.ClientStatus!=None else ""
        WhetherExpress = st.WhetherExpress if st.WhetherExpress != None else ""
        ToolsReservationTime = st.ToolsReservationTime if st.ToolsReservationTime!=None else ""
        ToolsReservationID = st.ToolsReservationID if st.ToolsReservationID != None else ""
        ClientID = st.ClientID if st.ClientID!=None else ""
        ManagerID = st.ManagerID if st.ManagerID!=None else ""
        DutyEngineerID = st.DutyEngineerID if st.DutyEngineerID!=None else ""
        OtherEngineerID = st.OtherEngineerID if st.OtherEngineerID!=None else ""
        ManagerStatus = st.ManagerStatus if st.ManagerStatus != None else ""
        Value = st.Value if st.Value != None else ""
    # time = (str)OnsiteTime
    # date_part = time.split('-')
    # Time = onsitetime[0]+'-'+onsitetime[1]+'-'+onsitetime[2]
    print st.OrderID
    return jsonify({
        'OrderID':OrderID,
        'OnsiteTime': '2016-04-25',
        'Location' : Location,
        'Title': Title,
        'Description': Description,
        'ReservationTime': ReservationTime,
        'RequestAcceptTime': RequestAcceptTime,
        'EngineerConfirmTime': EngineerConfirmTime,
        'TaskBeginTime': TaskBeginTime,
        'TaskEndTime': TaskEndTime,
        'ClientConfirmTime': ClientConfirmTime,
        'PredictedReturnTime': PredictedReturnTime,
        'KeeperConfirmTime': KeeperConfirmTime,
        'ManagerConfirmTime': ManagerConfirmTime,
        'TaskStatus': TaskStatus,
        'ClientStatus': ClientStatus,
        'WhetherExpress': WhetherExpress,
        'ToolsReservationTime' :ToolsReservationTime,
        'ToolsReservationID' :ToolsReservationID,
        'ClientID' :ClientID,
        'ManagerID' :ManagerID,
        'DutyEngineerID' :DutyEngineerID,
        'OtherEngineerID' :OtherEngineerID,
        'ManagerStatus' :ManagerStatus,
        'Value' : Value

    })

@app.route('/clientConfirmFinish', methods=['POST', 'GET'])
def client_confirm_finish():
    ot = OrderTable.query.filter_by(OrderID=86).first()
    if ot!=None:
        ot.ClientStatus = True
        ot.ClientConfirmTime = datetime.datetime.now()
    ot.add()
    return jsonify({
        'Result': True
    })

@app.route('/managerConfirmFinish', methods=['POST', 'GET'])
def manager_confirm_finish():
    ot = OrderTable.query.filter_by(OrderID=86).first()
    if ot!=None:
        ot.ManagerStatus = True
        ot.ManagerConfirmTime= datetime.datetime.now()
    ot.add()
    return jsonify({
        'Result': True
    })
   
# @app.route('/onsiteInfoToExcel', methods=['POST', 'GET'])
# def onsite_info_to_excel():
#     ot = OrderTable.query.filter_by(OrderID=86).first()
#     if ot!=None:
#         ot.ManagerStatus = "True"
#         ot.ManagerConfirmTime= datetime.datetime.now()
#     ot.add()
#     # Create a workbook and add a worksheet.
#     workbook = xlsxwriter.Workbook('Expenses01.xlsx')
# worksheet = workbook.add_worksheet()

# # Some data we want to write to the worksheet.
# expenses = (
#     ['Rent', 1000],
#     ['Gas',   100],
#     ['Food',  300],
#     ['Gym',    50],
# )

# # Start from the first cell. Rows and columns are zero indexed.
# row = 0
# col = 0

# # Iterate over the data and write it out row by row.
# for item, cost in (expenses):
#     worksheet.write(row, col,     item)
#     worksheet.write(row, col + 1, cost)
#     row += 1

# # Write a total using a formula.
# worksheet.write(row, 0, 'Total')
# worksheet.write(row, 1, '=SUM(B1:B4)')

# workbook.close()
#     return jsonify({
#         'Result': True
#     })

@app.route('/managerConfirmAccept', methods=['POST', 'GET'])
def manager_confirm_accept():
    ot = OrderTable.query.filter_by(OrderID=86).first()
    if ot!=None:
        ot.RequestAcceptTime = datetime.datetime.now()
        ot.ManagerID = 10008
    ot.add()
    return jsonify({
        'Result': True
    })
@app.route('/verify_password', methods=["POST", 'GET'])
def verify_password():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
      
        st = StaffTable.query.filter_by(StaffID=username, Password=password).first()
        if st!=None:
            session['userid'] = username
            result = True
            position = st.Position if st.Position!=None else ""
        else:
            result = False
            position = ""
    
        return jsonify({
            "Result": result,
            "Position": position
        })
    except Exception, e:
        print(e)


@app.route('/scanStaffOrTool', methods=["POST", 'GET'])
def scan_staff_or_tool():
    try:
        IDToBeSent = request.args.get('inputID')
        #print IDToBeSent #for test
        if IDToBeSent == "200000":
            return jsonify({
                'Name': "A",
                'Picture': "/static/images/tool/t1.jpg"
            })
        elif IDToBeSent == "10003":
            return jsonify({
                'Position': "Engineer",
                'Name': "Barlow",
                'Picture': "/static/images/staff/r4.jpg"
            })
        elif IDToBeSent == "10006":
            return jsonify({
                'Position': "Toolkeeper",
                'Name': "Dave",
                'Picture': "/static/images/staff/r7.jpg"
            })
        else:
            return jsonify({
                'Error': "without this tool in the tool center!"
            })
    except Exception, e:
        print(e)


@app.route('/confirmBorrowTools', methods=["POST", 'GET'])
def confirm_borrow_tools():
    try:
        return jsonify({
            'Result': True
        })
    except Exception, e:
        print(e)

@app.route('/scan_box', methods=['POST'])
def scan_box():
    return jsonify({
        'Picture':"/static/images/toolbox/a1.jpg",
        'BoxModel':"A"
    })
@app.route('/leaseOrReturn')
def less_or_return():
    return render_template('leaseOrReturn.html')

@app.route('/borrowTools')
def borrow_tools():
    return render_template('borrowTools.html')

@app.route('/returnTools')
def return_tools():
    return render_template('returnTools.html')


@app.route('/onsiteAddress', methods=["POST"])
def onsite_address():
    return jsonify({
        'Result':True
    })
@app.route('/scanReturnedTools', methods=['GET', 'POST'])
def scan_returned_tools():
    try:
        IDToBeSent = request.args.get('inputID')
        # print IDToBeSent #for test
        if IDToBeSent == "200000":
            return jsonify({
                "Error": "",
                "Tools": [{
                    'ToolID': "200000",
                    'Name': "A",
                    'Address': "/static/images/tool/t1.jpg"
                }]
            })
        elif IDToBeSent == "10003":
            return jsonify({
                "Error": "",
                "Tools": [{
                    "ToolID": "200000",
                    "Name": "A",
                    "Address": "/static/images/tool/t1.jpg"
                },
                {
                    "ToolID": "200002",
                    "Name": "B",
                    "Address": "/static/images/tool/t3.jpg"
                },
                {
                    "ToolID": "200006",
                    "Name": "D",
                    "Address": "/static/images/tool/t7.jpg"
                }
                ]})
        else:
            return jsonify({
                'Error': "Please Rescan!"
            })
    except Exception, e:
        print(e)
    # return jsonify({
    #     "Error":"",
    #     "Tools":[{
    #         "ToolID":"1111",
    #         "Name":"xxxx",
    #         "Address":"xxxx"
    #     }]
    # })

@app.route('/toolsReturn',methods=['GET', 'POST'])
def tools_Return():
    return_status = request.args.get('ReturnStatus')
    current_tool_id = request.args.get('ToolID')
    #print return_status,current_tool_id #for test
    if return_status=="Return":
        return jsonify({
            'Result': True
        })
    else:
        return jsonify({
            'Result': False
        })

if __name__== '__main__':
    app.run()
