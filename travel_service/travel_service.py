from decimal import Decimal
from flask import Flask, Response, redirect, url_for, request, render_template,jsonify
import pymysql
from urllib import request as rq
import json ,time, math
import pandas as pd
from datetime import date
    
app = Flask(__name__)

# login
@app.route('/login', methods = ['POST', 'GET'])
def login():
    datajsonstr = request.get_data()
    input = json.loads(datajsonstr)
    name = input["name"]
    password = input["password"]
    # print(name, password)

    print(datajsonstr)

    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')

    sql1 = "SELECT user_id, password FROM User WHERE user_name = '%s'"%(name)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql1)
            User_data = cursor.fetchone()
            print(User_data)
    except Exception as e:
        print(e)

    mysql_conn.close()

    if User_data == None:
        return "用户不存在"
    elif password == User_data[1]:
        # if name == 'bankadmin1' or name == 'bankadmin2' or name == 'bankadmin3':
        #     # session["bankadmin"] = name
        #     return redirect(url_for('bank_manual_judge'))
        # elif name == 'fundadmin':
        #     return redirect(url_for('fund_manual_judge'))
        # session["userId"] = User_data[0]
        # session['name'] = name
        return "密码正确"
    else:
        return "密码错误"


# datatime转换为json
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

# ticket query
@app.route('/ticket_query', methods = ['POST', 'GET'])
def ticket_query():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)

    departure_city = input["departure_city"]
    arrival_city = input["arrival_city"]
    departure_time = input["departure_date"]
    preference = input["preference"]
    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')
    if preference == "price" :
        sql = "select flight_id, departure_city, arrival_city, departure_time, price, company_name from FlightInfo, Company where FlightInfo.company_id = Company.company_id and departure_city = '%s' and arrival_city = '%s' and departure_time = '%s' order by price"%(departure_city, arrival_city, departure_time)
    else:
        sql = "select flight_id, departure_city, arrival_city, departure_time, price, company_name from FlightInfo, Company where FlightInfo.company_id = Company.company_id and departure_city = '%s' and arrival_city = '%s' and departure_time = '%s' order by rating desc"%(departure_city, arrival_city, departure_time)

    print(sql)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            User_data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = {}
            print(columns)
            i = 0
            for row in User_data:
                label = "ticket" + str(i)
                i = i + 1
                result[label] = dict(zip(columns, row)) 
            # return json.dumps(result, cls=DateEncoder, ensure_ascii=False)
            # 使用 json.dumps 和 Response 来禁用 ASCII 转义
            json_data = json.dumps({"data": result}, cls=DateEncoder, ensure_ascii=False)
            # print(json_string)
            # json_data = json.dumps({"data": json_string}, cls=DateEncoder, ensure_ascii=False)
            return Response(json_data, mimetype='application/json')
    except Exception as e:
        print(e)
    mysql_conn.close()
        

# hotel query
@app.route('/hotel_query', methods = ['POST', 'GET'])
def hotel_query():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    arrival_city = input["arrival_city"]
    preference = input["preference"]
    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')
    if preference == "price" :
        sql = "select room_id, room_number, room_type, room_price, rating, hotel_name from Hotel, RoomInfo where Hotel.hotel_id = RoomInfo.hotel_id and city = '%s' order by price"%(arrival_city)
    else:
        sql = "select room_id, room_number, room_type, room_price, rating, hotel_name from Hotel, RoomInfo where Hotel.hotel_id = RoomInfo.hotel_id and city = '%s' order by rating desc"%(arrival_city)

    # print(sql)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            User_data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = {}
            print(columns)
            i = 0
            for row in User_data:
                label = "room" + str(i)
                i = i + 1
                result[label] = dict(zip(columns, row))
                # result.append(dict(zip(columns, row)))
                # 使用 json.dumps 和 Response 来禁用 ASCII 转义
            json_data = json.dumps({"data": result}, cls=DateEncoder, ensure_ascii=False)
            return Response(json_data, mimetype='application/json')
            # return json.dumps(result, cls=DateEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
    mysql_conn.close()

# car_rental query
@app.route('/car_rental_query', methods = ['POST', 'GET'])
def car_rental_query():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    need_car = input["need_car"]
    car_type = input["car_type"]
    gear_type = input["gear_type"]
    arrival_city = input["arrival_city"]
    preference = input["preference"]
    if need_car != "no":
        mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')
        if preference == "price" :
            sql = "select carrental_id, car_type, transmission_type, rental_location, return_location, price, rating, company_name from CarRental, Company where CarRental.company_id = Company.company_id and car_type = '%s' and transmission_type = '%s' and rental_location = '%s' and return_location = '%s' order by price"%(car_type, gear_type, arrival_city, arrival_city)
        else:
            sql = "select carrental_id, car_type, transmission_type, rental_location, return_location, price, rating, company_name from CarRental, Company where CarRental.company_id = Company.company_id and car_type = '%s' and transmission_type = '%s' and rental_location = '%s' and return_location = '%s' order by rating desc"%(car_type, gear_type, arrival_city, arrival_city)
        print(sql)
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
                User_data = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                result = {}
                print(columns)
                i = 0
                for row in User_data:
                    label = "car" + str(i)
                    i = i + 1
                    result[label] = dict(zip(columns, row))
                    # result.append(dict(zip(columns, row)))
                # return json.dumps(result, cls=DateEncoder, ensure_ascii=False)
                json_data = json.dumps({"data": result}, cls=DateEncoder, ensure_ascii=False)
                return Response(json_data, mimetype='application/json')
        except Exception as e:
            print(e)
        mysql_conn.close()
    else:
        return []

# car_rental query
@app.route('/attraction_query', methods = ['POST', 'GET'])
def attraction_query():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    arrival_city = input["arrival_city"]
    preference = input["preference"]
    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')
    if preference == "price" :
        sql = "select attraction_id, attraction_name, city, price, rating from Attraction where city = '%s' order by price"%(arrival_city)
    else:
        sql = "select attraction_id, attraction_name, city, price, rating from Attraction where city = '%s' order by rating desc"%(arrival_city)
    print(sql)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            User_data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = {}
            print(columns)
            i = 0
            for row in User_data:
                label = "attraction" + str(i)
                i = i + 1
                result[label] = dict(zip(columns, row))
                # result.append(dict(zip(columns, row)))
            json_data = json.dumps({"data": result}, cls=DateEncoder, ensure_ascii=False)
            return Response(json_data, mimetype='application/json')
            # return json.dumps(result, cls=DateEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
    mysql_conn.close()

@app.route('/guide_query', methods = ['POST', 'GET'])
def guide_query():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    arrival_city = input["arrival_city"]
    preference = input["preference"]
    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')
    if preference == "price" :
        sql = "select attraction_id, attraction_name, city, price, rating from Attraction where city = '%s' order by price"%(arrival_city)
    else:
        sql = "select attraction_id, attraction_name, city, price, rating from Attraction where city = '%s' order by rating desc"%(arrival_city)
    print(sql)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            User_data = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            result = []
            print(columns)
            for row in User_data:
                result.append(dict(zip(columns, row)))
            json_data = json.dumps({"data": result}, cls=DateEncoder, ensure_ascii=False)
            return Response(json_data, mimetype='application/json')
            # return json.dumps(result, cls=DateEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
    mysql_conn.close()

@app.route('/travel_recommend', methods = ['POST', 'GET'])
def travel_recommend():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    ticket_result = input["ticket_result"]
    hotel_result = input["hotel_result"]
    car_rental_result = input["car_rental_result"]
    attraction_result = input["attraction_result"]

    recommend_result = {}
    recommend_result["ticket_result"] = ticket_result
    recommend_result["hotel_result"] = hotel_result
    recommend_result["car_rental_result"] = car_rental_result
    recommend_result["attraction_result"] = attraction_result
    # recommend_result["hotel_result"] = hotel_result

    return json.dumps(recommend_result, ensure_ascii=False)


# 买飞机票
@app.route('/ticket_purchase', methods = ['POST', 'GET'])
def ticket_purchase():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    user_id = input["user_id"]
    flight_id = input["flight_id"]

    sql = "insert into ticket_purchase values (%s, %s)"%(user_id, flight_id)

    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')

    print(sql)
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        mysql_conn.commit()
        # result = cursor.fetchone()
        # print(result)
    return jsonify({"message": "Travel plan received successfully"})

# 酒店预定
@app.route('/hotel_preserve', methods = ['POST', 'GET'])
def hotel_preserve():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    print(input)

    user_id = input["user_id"]
    hotel_id = input["hotel_id"]
    room_id = input["room_id"]

    sql = "insert into hotel_preserve values (%s, %s, %s)"%(user_id, hotel_id, room_id)

    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')

    print(sql)
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        mysql_conn.commit()
        # result = cursor.fetchone()
        # print(result)
    return jsonify({"message": "Travel plan received successfully"})


# 车子预定
@app.route('/car_preserve', methods = ['POST', 'GET'])
def car_preserve():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    print(input)
    user_id = input["user_id"]
    carrental_id = input["carrental_id"]

    sql = "insert into car_preserve values (%s, %s)"%(user_id, carrental_id)

    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')

    print(sql)
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        mysql_conn.commit()
        # result = cursor.fetchone()
        # print(result)
    return jsonify({"message": "Travel plan received successfully"})


# 景点预定
@app.route('/attraction_preserve', methods = ['POST', 'GET'])
def attraction_preserve():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    user_id = input["user_id"]
    attraction_id = input["attraction_id"]

    sql = "insert into attraction_preserve values (%s, %s)"%(user_id, attraction_id)

    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')

    print(sql)
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        mysql_conn.commit()
        # result = cursor.fetchone()
        # print(result)
    return jsonify({"message": "Travel plan received successfully"})

# 导游预定
@app.route('/guide_preserve', methods = ['POST', 'GET'])
def guide_preserve():
    datajson = request.get_data()
    # print(datajson)
    input = json.loads(datajson)
    
    user_id = input["user_id"]
    guide_id = input["guide_id"]

    sql = "insert into guide_preserve values (%s, %s)"%(user_id, guide_id)

    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'ysm', password= 'yangshiming', db= 'ysm_tourism')

    print(sql)
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        mysql_conn.commit()
        # result = cursor.fetchone()
        # print(result)
    return jsonify({"message": "Travel plan received successfully"})

@app.route('/bank_query', methods = ['POST', 'GET'])
def bank_query():

    '''
    每个servicetask用request.getdata接收到一个json格式的数据
    '''
    datajsonstr = request.get_data()
    print(datajsonstr)
    input = json.loads(datajsonstr)
    userId = input["userId"]

    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'root', password= 'rootroot', db= 'loan')

    sql1 = "SELECT id, rate FROM Bank"
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql1)
            Bank_data = cursor.fetchall()
            # print(Bank_data)
    except Exception as e:
        print(e)

    sql2 = "SELECT bankId, userId, discount, quota FROM BankUser WHERE UserId = %s"%(userId)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql2)
            BankUser_data = cursor.fetchall()
            # print(BankUser_data)
    except Exception as e:
        print(e)

    sql3 = "SELECT name, salary FROM User WHERE id = %s"%(userId)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql3)
            User_data = cursor.fetchone()
            # print(User_data)
    except Exception as e:
        print(e)

    mysql_conn.close()
    
    output = {}
    bank_data = []
    bank_data_dict = {}
    for i in range(3):
        # print(Bank_data[i][1], BankUser_data[i][2])
        bank_data_dict["bankId"] = i + 1
        bank_data_dict["d_rate"] = round(Bank_data[i][1] * BankUser_data[i][2],4)
        bank_data_dict["b_quota"] = BankUser_data[i][3]
        bank_data.append(bank_data_dict.copy())
    output["bank"] = bank_data
    output["salary"] = User_data[1]
    return output


@app.route('/fund_query',methods = ['POST', 'GET'])
def fund_query():
    datajsonstr = request.get_data()
    print(datajsonstr)
    input = json.loads(datajsonstr)
    userId = input["userId"]

    mysql_conn = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'root', password= 'rootroot', db= 'loan')

    sql1 = "SELECT UserId, quota, rate FROM FundUser WHERE UserId = %s"%(userId)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql1)
            FundUser_data = cursor.fetchone()
            # print(FundUser_data)
    except Exception as e:
        print(e)

    mysql_conn.close()
    
    output = {}
    output["f_rate"] = FundUser_data[2]
    output["f_quota"] = FundUser_data[1]
    return output


def loan_calculator(amount, rate, term,):    # 传入的rate要乘100（比如5%传入5）
    up = amount * math.pow((1 + rate / 1200), term * 12)
    down = 1
    for i in range(1, term * 12):
        down = down + math.pow((1 + rate / 1200), i)
    A = up / down
    total_pay = round(A * term * 12, 2)
    monthly_pay = round(A, 2)
    loan_cal_dict = {}
    loan_cal_dict["total_pay"] = total_pay
    loan_cal_dict["monthly_pay"] = monthly_pay
    return loan_cal_dict


@app.route('/loan_rec',methods = ['POST', 'GET'])
def loan_rec(): 
    datajsonstr = request.get_data()
    input_data_dict = json.loads(datajsonstr)
    print(input_data_dict)
    # userId = int(input_data_dict["userId"])
    loanEXP = int(input_data_dict["loanEXP"])
    f_rate = float(input_data_dict["f_rate"])
    f_quota = int(input_data_dict["f_quota"])
    salary = int(input_data_dict["salary"])
    bankId_list = input_data_dict["bankId"]
    d_rate_list = input_data_dict["d_rate"]
    b_quota_list = input_data_dict["b_quota"]
    bank = [
        {"bankId":int(bankId_list[0]), "d_rate":float(d_rate_list[0]), "b_quota":int(b_quota_list[0])},
        {"bankId":int(bankId_list[1]), "d_rate":float(d_rate_list[1]), "b_quota":int(b_quota_list[1])},
        {"bankId":int(bankId_list[2]), "d_rate":float(d_rate_list[2]), "b_quota":int(b_quota_list[2])}
    ]
    # bank = input_data_dict['bank']    # b图帮忙把bank列表里面的字典给提取了，因此不能直接读bank列表
    print(bank)
    # 先按 d_rate 升序排序，再按 b_quota 降序排序(d_rate排序优先级高，放后面)
    bank_sorted_temp = sorted(bank, key = lambda i: i['b_quota'], reverse = True)
    bank_sorted = sorted(bank_sorted_temp, key = lambda i: i['d_rate']) 
    print(bank_sorted)

    bankId_rec = 0
    # d_rate_rec = 0
    # b_quota_rec = 0
    for bank_data in bank_sorted:   # 选择最佳银行
        if bank_data["b_quota"] >= (loanEXP - f_quota):
            bankId_rec = bank_data["bankId"]
            d_rate_rec = bank_data["d_rate"]
            b_quota_rec = bank_data["b_quota"]
            break

    # max_b_quota_dict = bank_sorted_temp[0]
    # max_b_quota = max_b_quota_dict["b_quota"]
    if bankId_rec == 0:     # 如果所有银行额度加上公积金额度都不到期望，返回贷款类型为0，代表期望过高
        return json.dumps({"loan_type_rec": 0, "total_quota": bank_sorted_temp[0]["b_quota"] + f_quota, "loanEXP": loanEXP})

    term_list = [5,10,15,25,30]
    loan_cal_list = []
    loan_cal_list_dict = {}
    if f_quota == 0:
        loan_type_rec = 3   # 公积金额度0，商业贷款
        b_amount_rec = loanEXP
        f_amount_rec = 0
        for term in term_list:  # 计算所有的term对应的还款明细
            loan_cal_dict = loan_calculator(b_amount_rec, d_rate_rec * 100, term)
            loan_cal_list_dict["term"] = term
            loan_cal_list_dict["total_pay"] = loan_cal_dict["total_pay"]
            loan_cal_list_dict["monthly_pay"] = loan_cal_dict["monthly_pay"]
            loan_cal_list.append(loan_cal_list_dict.copy())
    elif f_quota >= loanEXP:
        loan_type_rec = 1   # 公积金额度覆盖期望贷款，公积金贷款
        b_amount_rec = 0
        f_amount_rec = loanEXP
        for term in term_list:  # 计算所有的term对应的还款明细
            loan_cal_dict = loan_calculator(f_amount_rec, f_rate * 100, term)
            loan_cal_list_dict["term"] = term
            loan_cal_list_dict["total_pay"] = loan_cal_dict["total_pay"]
            loan_cal_list_dict["monthly_pay"] = loan_cal_dict["monthly_pay"]
            loan_cal_list.append(loan_cal_list_dict.copy())
    else:
        loan_type_rec = 2   # 混合贷款
        f_amount_rec = f_quota
        b_amount_rec = loanEXP - f_quota
        for term in term_list:  # 计算所有的term对应的还款明细
            f_loan_cal_dict = loan_calculator(f_amount_rec, f_rate * 100, term)
            b_loan_cal_dict = loan_calculator(b_amount_rec, d_rate_rec * 100, term)
            loan_cal_list_dict["term"] = term
            loan_cal_list_dict["total_pay"] = f_loan_cal_dict["total_pay"] + b_loan_cal_dict["total_pay"]
            loan_cal_list_dict["monthly_pay"] = f_loan_cal_dict["monthly_pay"] + b_loan_cal_dict["monthly_pay"]
            loan_cal_list.append(loan_cal_list_dict.copy())
    print(loan_cal_list)

    term_rec = 0
    for loan_cal_data in loan_cal_list:     # 找出满足月还款低于月收入的条件下，最小的还款年数（总还款少）
        if loan_cal_data["monthly_pay"] <= salary:
            term_rec = loan_cal_data["term"]
            total_pay_rec = loan_cal_data["total_pay"]
            monthly_pay_rec = loan_cal_data["monthly_pay"]
            break
    
    if term_rec == 0:     # 如果所有还款年数的月还款都高于月收入，返回贷款类型为-1，代表期望过高
        return json.dumps({"loan_type_rec": -1, "salary": salary, "min_monthly_pay": loan_cal_list[4]["monthly_pay"]})

    output = {
        "loan_type_rec":loan_type_rec,
        "bankId_rec":bankId_rec,
        "b_amount_rec":b_amount_rec,
        "d_rate_rec":d_rate_rec,
        "f_amount_rec":f_amount_rec,
        "f_rate_rec":f_rate,
        "term_rec":term_rec,
        "monthly_pay_rec":round(monthly_pay_rec, 2),
        "total_pay_rec":round(total_pay_rec, 2)
    }
    return output


@app.route('/credit_query', methods=['POST', 'GET'])
def credit_query():##############################################查征信
    datajsonstr = request.get_data()
    print(datajsonstr)
    userId_dict = json.loads(datajsonstr)
    userId = userId_dict["userId"]
    loan_time = time.strftime('%Y%m%d%H%M%S', time.localtime())

    mysql_conn = pymysql.connect(
        host='127.0.0.1', port=3306, user='root', password='rootroot', db='loan')
    
    sql1 = "SELECT credit FROM User WHERE id = %s" % (userId)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql1)
            credit = cursor.fetchone()[0]
            # print(credit)
    except Exception as e:
        print(e)

    mysql_conn.close()

    return {"credit": credit, "loan_time": loan_time}



@app.route('/store_bank_loan', methods=['POST', 'GET'])
def store_bank_loan():
    datajsonstr = request.get_data()
    print(datajsonstr)
    bank_dict = json.loads(datajsonstr)
    credit = bank_dict["credit"]
    userId = bank_dict["userId"]
    bankId = bank_dict["bankId"]
    loan_type = int(bank_dict["loan_type"])
    repay_type = bank_dict["repay_type"]
    term = bank_dict["term"]
    d_rate = bank_dict["d_rate"]
    b_amount = bank_dict["b_amount"]
    b_interest = bank_dict["b_interest"]
    b_total_pay = bank_dict["b_total_pay"]
    b_monthly_pay = bank_dict["b_monthly_pay"]
    b_monthly_decrement = bank_dict["b_monthly_decrement"]
    loan_time = bank_dict["loan_time"]

    if loan_type == 3 or loan_type == 2:
        mysql_conn = pymysql.connect(
            host='127.0.0.1', port=3306, user='root', password='rootroot', db='loan')
        sql = "INSERT INTO BankLoan (userId, bankId, loan_type, repay_type, term, d_rate, \
            b_amount, b_interest, b_total_pay, b_monthly_pay, b_monthly_decrement, loan_time) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
            userId, bankId, loan_type, repay_type, term, d_rate, b_amount, b_interest,
            b_total_pay, b_monthly_pay, b_monthly_decrement, loan_time)
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            print(e)
        mysql_conn.commit()
        mysql_conn.close()
    return {"credit": credit, "loan_time": loan_time}


@app.route('/store_fund_loan', methods=['POST', 'GET'])
def store_fund_loan():
    datajsonstr = request.get_data()
    print(datajsonstr)
    fund_dict = json.loads(datajsonstr)
    credit = fund_dict["credit"]
    userId = fund_dict["userId"]
    loan_type = int(fund_dict["loan_type"])
    repay_type = fund_dict["repay_type"]
    term = fund_dict["term"]
    f_rate = fund_dict["f_rate"]
    f_amount = fund_dict["f_amount"]
    f_interest = fund_dict["f_interest"]
    f_total_pay = fund_dict["f_total_pay"]
    f_monthly_pay = fund_dict["f_monthly_pay"]
    f_monthly_decrement = fund_dict["f_monthly_decrement"]
    loan_time = fund_dict["loan_time"]

    if loan_type == 1 or loan_type == 2:
        mysql_conn = pymysql.connect(
            host='127.0.0.1', port=3306, user='root', password='rootroot', db='loan')
        sql = "INSERT INTO FundLoan (userId, loan_type, repay_type, term, f_rate, \
            f_amount, f_interest, f_total_pay, f_monthly_pay, f_monthly_decrement, loan_time) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
            userId, loan_type, repay_type, term, f_rate, f_amount, f_interest, 
            f_total_pay, f_monthly_pay, f_monthly_decrement, loan_time)
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            print(e)
        mysql_conn.commit()
        mysql_conn.close()
    return {"credit": credit, "loan_time": loan_time}


@app.route('/bank_auto_judge', methods=['POST', 'GET'])
def bank_auto_judge():
    datajsonstr = request.get_data()
    print(datajsonstr)
    bank_dict = json.loads(datajsonstr)
    credit = int(bank_dict["credit"])
    userId = int(bank_dict["userId"])
    bankId = int(bank_dict["bankId"])
    b_amount = float(bank_dict["b_amount"])
    b_monthly_pay = float(bank_dict["b_monthly_pay"])
    loan_time = bank_dict["loan_time"]

    mysql_conn = pymysql.connect(
        host='127.0.0.1', port=3306, user='root', password='rootroot', db='loan')
    sql = "SELECT salary FROM User WHERE id = %s" % (userId)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            salary = cursor.fetchone()[0]
    except Exception as e:
        print(e)
    # print(salary)

    sql = "SELECT quota FROM BankUser WHERE userId = %s AND bankId = %s" % (
        userId, bankId)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            quota = cursor.fetchone()[0]
    except Exception as e:
        print(e)
    # print(quota)

    sql = "SELECT id FROM BankLoan WHERE loan_time = %s" % (loan_time)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            BankLoan_data = cursor.fetchone()
            if BankLoan_data is not None:
                loan_id = BankLoan_data[0]
            else:
                return {"result": "fail", "loan_time": loan_time}
    except Exception as e:
        print(e)

    # 如果 每月计划还款 < salary * 0.8 且 贷款不超过额度 且 征信良好 则自动通过
    if b_monthly_pay < salary * 0.8 and b_amount <= quota and credit == 1:
        sql = "UPDATE BankLoan SET auto_judge = '1' WHERE id = %s" % (loan_id)
        print(sql)
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            print(e)
        mysql_conn.commit()
        mysql_conn.close()
        return {"result": "ok", "loan_time": loan_time}
    else:
        sql = "UPDATE BankLoan SET auto_judge = '0' WHERE id = %s" % (loan_id)
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            print(e)
        mysql_conn.commit()
        mysql_conn.close()
        return {"result": "no", "loan_time": loan_time}


@app.route('/fund_auto_judge', methods=['POST', 'GET'])
def fund_auto_judge():
    datajsonstr = request.get_data()
    print(datajsonstr)
    fund_dict = json.loads(datajsonstr)
    credit = int(fund_dict["credit"])
    userId = int(fund_dict["userId"])
    f_amount = float(fund_dict["f_amount"])
    loan_time = fund_dict["loan_time"]

    mysql_conn = pymysql.connect(
        host='127.0.0.1', port=3306, user='root', password='rootroot', db='loan')
    sql = "SELECT f_month FROM FundUser WHERE userId = %s" % (userId)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            f_month = cursor.fetchone()[0]
    except Exception as e:
        print(e)
    print(f_month)

    sql = "SELECT quota FROM FundUser WHERE userId = %s" % (userId)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            quota = cursor.fetchone()[0]
    except Exception as e:
        print(e)
    # print(quota)

    sql = "SELECT id FROM FundLoan WHERE loan_time = %s" % (loan_time)
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            FundLoan_data = cursor.fetchone()
            if FundLoan_data is not None:
                loan_id = FundLoan_data[0]
            else:
                return {"result": "fail", "loan_time": loan_time}
    except Exception as e:
        print(e)

    # 如果 缴纳公积金 > 12个月 且 征信良好 则自动通过
    if f_month > 12 and f_amount <= quota and credit == 1:

        sql = "UPDATE FundLoan SET auto_judge = '1' WHERE id = %s" % (loan_id)
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            print(e)
        mysql_conn.commit()
        mysql_conn.close()
        return {"result": "ok", "loan_time": loan_time}
    else:
        sql = "UPDATE FundLoan SET auto_judge = '0' WHERE id = %s" % (loan_id)
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
        except Exception as e:
            print(e)
        mysql_conn.commit()
        mysql_conn.close()
        return {"result": "no", "loan_time": loan_time}


if __name__ == '__main__':
   app.run(debug = True, host='0.0.0.0',port=2024)
