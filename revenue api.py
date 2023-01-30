# -*- coding: utf-8 -*-
"""
"""
#account/GROUP_CUSTOMER/custname= product category
#vertical=  region
#sbu= sales channel
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from collections import OrderedDict
import json
import os
import datetime
import pandas as pd
import requests
import random
import plotly.graph_objs as go
import os
from plotly import __version__
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

mysql = MySQL()
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app, support_credentials=True)
app.config['MYSQL_DATABASE_USER'] = 'username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Password'
app.config['MYSQL_DATABASE_DB'] = 'demo_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)



@app.route("/compareRevenue", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def compareRevenue():
    category_arg = request.args.get('account')
    region_arg = request.args.get('vertical')
    channel_arg = request.args.get('sbu')
    # custname_lst = ','.join(['%s'] * len(custname_arg))
    # cursor.execute("DELETE FROM foo.bar WHERE baz IN (%s)" % custname_lst,tuple(custname_arg))
    cursor = mysql.connect().cursor()
    if category_arg:
        custname_lst = str(category_arg).split(',')
        if len(custname_lst) > 1:
            query = """
                    SELECT 
                        sales_channel,
                        region AS VERTICAL,
                        product_category AS ACCOUNT,
                        SUM(CASE
                            WHEN qtr = 'Q1_FY18' THEN revenue
                        END) 'Q1',
                        SUM(CASE
                            WHEN qtr = 'Q2_FY18' THEN revenue
                        END) 'Q2',
                        SUM(CASE
                            WHEN qtr = 'Q3_FY18' THEN revenue
                        END) 'Q3',
                        SUM(CASE
                            WHEN qtr= 'Q4_FY18' THEN revenue
                        END) 'Q4'
                    FROM
                        demo_db.demo_new
                    WHERE
                        sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR')
                            AND qtr IN ('Q1_FY18' , 'Q2_FY18', 'Q3_FY18', 'Q4_FY18')
                            
                            AND product_category IN %s """ % repr(tuple(map(str, custname_lst))) + """
                    GROUP BY sales_channel , region , product_category
                    """
        else:
            query = """
                    SELECT 
                        sales_channel,
                        region AS VERTICAL,
                        product_category AS ACCOUNT,
                        SUM(CASE
                            WHEN qtr = 'Q1_FY18' THEN revenue
                        END) 'Q1',
                        SUM(CASE
                            WHEN qtr = 'Q2_FY18' THEN revenue
                        END) 'Q2',
                        SUM(CASE
                            WHEN qtr = 'Q3_FY18' THEN revenue
                        END) 'Q3',
                        SUM(CASE
                            WHEN qtr= 'Q4_FY18' THEN revenue
                        END) 'Q4'
                    FROM
                       demo_db.demo_new
                    WHERE
                        sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR')
                            AND qtr IN ('Q1_FY18' , 'Q2_FY18', 'Q3_FY18', 'Q4_FY18')
                            
                            AND product_category IN ('%s')""" % custname_lst[0] + """
                    GROUP BY sales_channel , region , product_category
                    """
        cursor.execute(query)
        title = {"title": "Revenue Comparison of " + (', '.join(custname_lst)).upper() + " Product Categories."}
    elif region_arg:
        vertical_lst = str(region_arg).split(',')
        if len(vertical_lst) > 1:
            cursor.execute(
                """
                SELECT 
                        sales_channel,
                        region AS VERTICAL,
                        product_category AS ACCOUNT,
                        SUM(CASE
                            WHEN qtr = 'Q1_FY18' THEN revenue
                        END) 'Q1',
                        SUM(CASE
                            WHEN qtr = 'Q2_FY18' THEN revenue
                        END) 'Q2',
                        SUM(CASE
                            WHEN qtr = 'Q3_FY18' THEN revenue
                        END) 'Q3',
                        SUM(CASE
                            WHEN qtr= 'Q4_FY18' THEN revenue
                        END) 'Q4'
                    FROM
                       demo_db.demo_new
                    WHERE
                        sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR')
                            AND qtr IN ('Q1_FY18' , 'Q2_FY18', 'Q3_FY18', 'Q4_FY18')
                     
                    AND region in %s""" % repr(tuple(map(str, vertical_lst))) + """
                GROUP BY sales_channel,region
                """)

        else:
            cursor.execute(
                """
                SELECT sales_channel, region AS VERTICAL, 
                     SUM(CASE
                            WHEN qtr = 'Q1_FY18' THEN revenue
                        END) 'Q1',
                        SUM(CASE
                            WHEN qtr = 'Q2_FY18' THEN revenue
                        END) 'Q2',
                        SUM(CASE
                            WHEN qtr = 'Q3_FY18' THEN revenue
                        END) 'Q3',
                        SUM(CASE
                            WHEN qtr= 'Q4_FY18' THEN revenue
                        END) 'Q4'
                    FROM
                       demo_db.demo_new
                    WHERE
                        sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR')
                            AND qtr IN ('Q1_FY18' , 'Q2_FY18', 'Q3_FY18', 'Q4_FY18')
                     
                    AND region in ('%s')""" % vertical_lst[0] + """
                GROUP BY sales_channel, region
                """)

        title = {"title": "Revenue Comparison of " + (', '.join(vertical_lst)).upper() + " Regions."}
    elif channel_arg:
        sbu_lst = str(channel_arg).split(',')
        if len(sbu_lst) > 1:
            cursor.execute("""
                            SELECT sales_channel, 
                                SUM(CASE
                            WHEN qtr = 'Q1_FY18' THEN revenue
                        END) 'Q1',
                        SUM(CASE
                            WHEN qtr = 'Q2_FY18' THEN revenue
                        END) 'Q2',
                        SUM(CASE
                            WHEN qtr = 'Q3_FY18' THEN revenue
                        END) 'Q3',
                        SUM(CASE
                            WHEN qtr= 'Q4_FY18' THEN revenue
                        END) 'Q4'
                    FROM
                        demo_db.demo_new
                    WHERE
                        sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR')
                            AND qtr IN ('Q1_FY18' , 'Q2_FY18', 'Q3_FY18', 'Q4_FY18')
                                 
                                AND sales_channel in %s""" % repr(tuple(map(str, sbu_lst))) + """
                            GROUP BY sales_channel
                            """)

        else:
            cursor.execute("""
                            SELECT sales_channel, 
                               SUM(CASE
                            WHEN qtr = 'Q1_FY18' THEN revenue
                        END) 'Q1',
                        SUM(CASE
                            WHEN qtr = 'Q2_FY18' THEN revenue
                        END) 'Q2',
                        SUM(CASE
                            WHEN qtr = 'Q3_FY18' THEN revenue
                        END) 'Q3',
                        SUM(CASE
                            WHEN qtr= 'Q4_FY18' THEN revenue
                        END) 'Q4'
                    FROM
                        demo_db.demo_new
                    WHERE
                        sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR')
                            AND qtr IN ('Q1_FY18' , 'Q2_FY18', 'Q3_FY18', 'Q4_FY18') 
                                 
                                AND sales_channel in ('%s')""" % sbu_lst[0] + """
                            GROUP BY sales_channel
                            """)
        title = {"title": "Revenue Comparison of " + (', '.join(sbu_lst)).upper() + " Sales Channels."}
    else:
        cursor.execute("""
                        SELECT sales_channel, 
                            SUM(CASE
                            WHEN qtr = 'Q1_FY18' THEN revenue
                        END) 'Q1',
                        SUM(CASE
                            WHEN qtr = 'Q2_FY18' THEN revenue
                        END) 'Q2',
                        SUM(CASE
                            WHEN qtr = 'Q3_FY18' THEN revenue
                        END) 'Q3',
                        SUM(CASE
                            WHEN qtr= 'Q4_FY18' THEN revenue
                        END) 'Q4'
                    FROM
                       demo_db.demo_new
                    WHERE
                        sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR')
                            AND qtr IN ('Q1_FY18' , 'Q2_FY18', 'Q3_FY18', 'Q4_FY18') 
                             
                        GROUP BY sales_channel
                         """)
        title = {"title": "Revenue Comparison of Sales Channels."}

    data_json = []
    header = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    for j in data:
        if j[2]:
            data_json.append(OrderedDict(zip(header, j)))
    data_json.append(title)
   
    print(data_json)
    varx="Hello from server"
    return jsonify(data_json)
    return varx




@app.route("/getPredictions", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getPredictions():
    """ Returns the predictions for the given entity along with inference and factors. """
    # getjson, value = json.loads(getAllEntitiesList())
    # ent_dict = json.loads(value)
    # print (ent_dict)
    # print("inside the new api")
    print("Hitting GET PREDICTIONS API")
    region_arg = request.args.get('vertical')
    channel_arg = request.args.get('sbu')
    category_arg = request.args.get('account')
    try:
        if len(channel_arg.split(',')) > 1:
            channel_arg = channel_arg.split(',')[0]
    except:
        pass

    try:
        if len( region_arg.split(',')) > 1:
            region_arg =  region_arg.split(',')[0]
    except:
        pass
    try:
        if len(category_arg.split(',')) > 1:
            category_arg = category_arg.split(',')[0]
    except:
        pass

    timeline_arg = 'Q1_FY19'
    cursor = mysql.connect().cursor()
    query = """SELECT sales_channel AS SALES_CHANNEL, region AS REGION, 
                    SUM(CASE WHEN qtr = 'Q1_FY18' THEN revenue END) AS 'REGION_REVENUE_Q1',
                    SUM(CASE WHEN qtr = 'Q2_FY18' THEN revenue END) AS 'REGION_REVENUE_Q2',
                    SUM(CASE WHEN qtr = 'Q3_FY18' THEN revenue END) AS 'REGION_REVENUE_Q3',
                    SUM(CASE WHEN qtr = 'Q4_FY18' THEN revenue END) AS 'REGION_REVENUE_Q4',
					SUM(CASE WHEN qtr = 'Q1_FY19' THEN predicted_revenue END) 'PREDICTED_REGION_REVENUE_Q1',
                FROM demo_db.demo_new WHERE qtr IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18', 'Q1_FY19') 
                 AND region = '""" + region_arg + """' 
                GROUP BY sales_channel, region"""
    cursor.execute(query)
    title = {'title': 'Revenue of ' + str(vertical_arg).upper() + " Region - Last Financial year."}

    # if SBU NAME is given
    if channel_arg:
  
        # returns the details of that particular sbu
        cursor.execute("""SELECT SBU AS SALES_CHANNEL, SUM(CASE WHEN qtr = 'Q1_FY18' revenue END) 'CHANNEL_REVENUE_Q1'  ,
                             SUM(CASE WHEN qtr = 'Q2_FY18' revenue END) 'CHANNEL_REVENUE_Q2'  , 
                             SUM(CASE WHEN qtr = 'Q3_FY18' revenue END) 'CHANNEL_REVENUE_Q3'  , 
                             SUM(CASE WHEN qtr = 'Q4_FY18' revenue END) 'CHANNEL_REVENUE_Q4' , 
							 SUM(CASE WHEN qtr = 'Q1_FY19' THEN predicted_revenue END) 'PREDICTED_CHANNEL_REVENUE_Q1',
                         FROM   demo_db.demo_new  WHERE sales_channel = '""" + channel_arg + """'
                         AND qtr IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18', 'Q1_FY19')  
                          
                         GROUP BY sales_channel ORDER BY 5 DESC""")
        title = {'title': 'Revenue of ' + str(channel_arg).upper() + " Channel - Last Financial year."}
        

    # if category Name is given
    elif category_arg:
        # returns the details of that particular customer along with vertical name and its corresponding sbu name
        query = """SELECT sales_channel, region AS VERTICAL, product_category AS ACCOUNT,
                    SUM(CASE WHEN qtr = 'Q1_FY18' THEN revenue END) 'ACCOUNT_REVENUE_Q1',
                    SUM(CASE WHEN qtr = 'Q2_FY18' THEN revenue END) 'ACCOUNT_REVENUE_Q2', 
                    SUM(CASE WHEN qtr = 'Q3_FY18' THEN revenue END) 'ACCOUNT_REVENUE_Q3', 
                    SUM(CASE WHEN qtr = 'Q4_FY18' THEN revenue END) 'ACCOUNT_REVENUE_Q4',
					SUM(CASE WHEN qtr = 'Q1_FY19' THEN predicted_revenue END) 'PREDICTED_ACCOUNT_REVENUE_Q1'
                    FROM demo_db.demo_new  WHERE sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR') 
                    AND qtr IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18', 'Q1_FY19')  
                    AND product_category = '""" + category_arg + """' 
                    GROUP BY sales_channel, region, ACCOUNT ORDER BY 7 DESC"""
        cursor.execute(query)
        title = {"title": "Revenue of " + str(category_arg).upper() + " Account - Last Financial year."}

    # if no name is specified
    else:
       
        # returns the verticals with their corresponding revenues
        query = """SELECT sales_channel AS SALES_CHANNEL, region AS REGION, 
                    SUM(CASE WHEN qtr = 'Q1_FY18' THEN predicted_revenue END) 'REGION_REVENUE_Q1',
                    
                    FROM   demo_db.demo_new WHERE sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR') 
                    AND qtr IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18') 
                     GROUP BY sales_channel, region ORDER BY 3 DESC"""
        cursor.execute(query)
        title = {"title": "Revenue of All Regions - Last Financial year."}
       
    
    
    data_json = []
    header = [i[0] for i in cursor.description]
    data = cursor.fetchall()
    for j in data:
        data_json.append(OrderedDict(zip(header, j)))
    # title = 'Title':'Predicted Revenue' +
    data_json.append(title)
    print(data_json)
    return jsonify(data_json)
    # return json.dumps(data_json)




@app.route("/getHistoricRevenueDetails", methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def getHistoricRevenueDetails():
    """ Returns the json data of the sql quries based on the parameters """
    # VARIABLE ASSIGNMENT BASED ON PARAMETERS
    #custname= category
    #vertical = region
    #sbu= channel 
    category_arg = request.args.get('account')
    region_arg = request.args.get('vertical')
    channel_arg = request.args.get('sbu')
    #revenue_level = request.args.get('revenueLevel') 
    #type_of_chart = request.args.get('chartType')

    # declaring cursor for database
    cursor = mysql.connect().cursor()

    # if vertical name is given
    if region_arg:

#        #if revenue_level == 'account':
#        query = """SELECT SBU, VERTICAL_TO_BE_CONSIDERED AS VERTICAL, GROUP_CUSTOMER AS ACCOUNT,
#                            SUM(CASE WHEN QTR = 'Q1_FY18' THEN PLAN_REV_FY18 END) 'ACCOUNT_REVENUE_Q1', 
#                            SUM(CASE WHEN QTR = 'Q2_FY18' THEN PLAN_REV_FY18 END) 'ACCOUNT_REVENUE_Q2', 
#                            SUM(CASE WHEN QTR = 'Q3_FY18' THEN PLAN_REV_FY18 END) 'ACCOUNT_REVENUE_Q3', 
#                            SUM(CASE WHEN QTR = 'Q4_FY18' THEN PLAN_REV_FY18 END) 'ACCOUNT_REVENUE_Q4'
#                        FROM  demo_db.sales_tb_demo
#                        WHERE SBU IN ('ECOMMERCE', 'BRICK AND MORTAR') 
#                        AND QTR IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18')  
#                        AND VERTICAL_TO_BE_CONSIDERED = '""" + vertical_arg + """' 
#                        GROUP BY sbu ,VERTICAL_TO_BE_CONSIDERED, account"""
#            # Returns the top ten accounts of the vertical
#        cursor.execute(query)
#        title = {"title": "Account Level Revenue Details of " + str(
#                vertical_arg).upper() + " Vertical - Last Financial year."}
#        else:
        # Returns the details of the particular vertical
        query = """SELECT sales_channel AS SALES_CHANNEL, region AS REGION, 
                    SUM(CASE WHEN qtr = 'Q1_FY18' THEN revenue END) AS 'REGION_REVENUE_Q1',
                    SUM(CASE WHEN qtr = 'Q2_FY18' THEN revenue END) AS 'REGION_REVENUE_Q2',
                    SUM(CASE WHEN qtr = 'Q3_FY18' THEN revenue END) AS 'REGION_REVENUE_Q3',
                    SUM(CASE WHEN qtr = 'Q4_FY18' THEN revenue END) AS 'REGION_REVENUE_Q4'
                FROM demo_db.demo_new WHERE qtr IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18') 
                 AND region = '""" + region_arg + """' 
                GROUP BY sales_channnel, region"""
        cursor.execute(query)
        title = {'title': 'Revenue of ' + str(region_arg).upper() + " Region - Last Financial year."}

    # if SBU NAME is given
    elif channel_arg:
  
        # returns the details of that particular sbu
        cursor.execute("""SELECT sales_channel AS SALES_CHANNEL, SUM(CASE WHEN qtr = 'Q1_FY18' THEN revenue END) AS 'REGION_REVENUE_Q1',
                    SUM(CASE WHEN qtr = 'Q2_FY18' THEN revenue END) AS 'REGION_REVENUE_Q2',
                    SUM(CASE WHEN qtr = 'Q3_FY18' THEN revenue END) AS 'REGION_REVENUE_Q3',
                    SUM(CASE WHEN qtr = 'Q4_FY18' THEN revenue END) AS 'REGION_REVENUE_Q4'
                         FROM   demo_db.demo_new  WHERE sales_channel = '""" + channel_arg + """'
                         AND qtr IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18') 
                          
                         GROUP BY sales_channel ORDER BY 5 DESC""")
        title = {'title': 'Revenue of ' + str(channel_arg).upper() + " Channel - Last Financial year."}
        

    # if category Name is given
    elif category_arg:
        # returns the details of that particular customer along with vertical name and its corresponding sbu name
        query = """SELECT sales_channel, region AS VERTICAL, product_category AS ACCOUNT,
                   SUM(CASE WHEN qtr = 'Q1_FY18' THEN revenue END) AS 'REGION_REVENUE_Q1',
                    SUM(CASE WHEN qtr = 'Q2_FY18' THEN revenue END) AS 'REGION_REVENUE_Q2',
                    SUM(CASE WHEN qtr = 'Q3_FY18' THEN revenue END) AS 'REGION_REVENUE_Q3',
                    SUM(CASE WHEN qtr = 'Q4_FY18' THEN revenue END) AS 'REGION_REVENUE_Q4'
                    FROM demo_db.demo_new  WHERE sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR') 
                    AND qtr IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18')  
                    AND product_category = '""" + category_arg + """' 
                    GROUP BY sales_channel, region, product_category ORDER BY 7 DESC"""
        cursor.execute(query)
        title = {"title": "Revenue of " + str(category_arg).upper() + " Account - Last Financial year."}

    # if no name is specified
    else:
       
        # returns the verticals with their corresponding revenues
        query = """SELECT sales_channel AS SALES_CHANNEL, region AS REGION, 
                    SUM(CASE WHEN qtr = 'Q1_FY18' THEN revenue END) AS 'REGION_REVENUE_Q1',
                    SUM(CASE WHEN qtr = 'Q2_FY18' THEN revenue END) AS 'REGION_REVENUE_Q2',
                    SUM(CASE WHEN qtr = 'Q3_FY18' THEN revenue END) AS 'REGION_REVENUE_Q3',
                    SUM(CASE WHEN qtr = 'Q4_FY18' THEN revenue END) AS 'REGION_REVENUE_Q4'
                    FROM   demo_db.demo_new  
                    WHERE sales_channel IN ('ECOMMERCE', 'BRICK AND MORTAR') 
                    AND qtr IN ('Q1_FY18', 'Q2_FY18','Q3_FY18', 'Q4_FY18') 
                    GROUP BY sales_channel, region, ORDER BY 6 DESC"""
        cursor.execute(query)
        title = {"title": "Revenue of All Regions - Last Financial year."}
       
          

    data_json = []
    header = [i[0] for i in cursor.description]
    header_tuple = tuple(header)
    # adding the descriptions to header list
    # output of the sql query execution
    data = cursor.fetchall()
    # data is tuple
    # converting the data to a dataframe for easy handling of graph data
    output_dataframe = pd.DataFrame(list(data), columns=header)
    # defaults
    
    for j in data:
        data_json.append(OrderedDict(zip(header, j)))

    for i in range(len(data_json)):
        for k, v in data_json[i].items():
            try:
                x = round(float(v) / 1000000, 2)
                data_json[i][k] = x
            except:
                continue
    for i in range(len(data_json) - 2):
        data_json[i] = OrderedDict(sorted(data_json[i].items(), key=lambda pair: header_tuple.index(pair[0])))
    final_data = list()
    final_data.append({'table': data_json})
    # final_data.append({'table':json.dumps(data_json, sort_keys=True)})
    final_data.append(title)

    return jsonify(final_data)


if __name__ == "__main__":
     
    app.run(host='0.0.0.0', port=5001, debug=True)