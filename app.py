from flask import Flask, request, jsonify
import json
from flaskext.mysql import MySQL
import pymysql
from flask_cors import CORS, cross_origin

app = Flask(__name__)

mysql = MySQL(app)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
app.config['MYSQL_DATABASE_DB'] = 'quran'
mysql.init_app(app)

@app.route("/search/<search>/<text>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def addSearch(search,text):
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT * FROM search WHERE search = %s",search)
    ss = cur0.fetchone()
    if (len(ss) == 0) :
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("INSERT INTO search (search,result) VALUES (%s,%s)",(search,text))
        conn.commit()
        cur.close()
        return 'ok'
    else :
        return 'fail'

@app.route("/search/<search>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def getSearch(search):
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT * FROM search WHERE search = %s",search)
    ss = cur0.fetchone()
    return json.dumps(ss, ensure_ascii=False)

@app.route("/search", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def search():
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT (search) FROM search ")
    ss = cur0.fetchall()
    return json.dumps(ss, ensure_ascii=False)

@app.route("/hizb-detail/<int:hizbId>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def hizbDetail(hizbId):
    if ( hizbId == 60 ):
        res = [[237,[[87,1,19],[88,1,26],[89,1,30]]],[238,[[90,1,20],[91,1,15],[92,1,21],[93,1,11]]],[239,[[94,1,8],[95,1,8],[96,1,19],[97,1,5],[98,1,8],[99,1,8],[100,1,8]]],[240,[[100,8,11],[101,1,11],[102,1,8],[103,1,3],[104,1,9],[105,1,5],[106,1,4],[107,1,7],[108,1,3],[109,1,6],[110,1,3],[111,1,5],[112,1,4],[113,1,5],[114,1,6]]]]
        return json.dumps(res, ensure_ascii=False)
    else :
        res =[]
        for i in range(1,5):
            conn0 = mysql.connect()
            cur0 = conn0.cursor(pymysql.cursors.DictCursor)
            cur0.execute("SELECT * FROM hizb WHERE id = %s",((hizbId-1)*4)+i)
            hizb0 = cur0.fetchone()
            sura0 = hizb0["sura"]
            aya0 = hizb0["aya"]
            conn1 = mysql.connect()
            cur1 = conn1.cursor(pymysql.cursors.DictCursor)
            cur1.execute("SELECT * FROM hizb WHERE id = %s",((hizbId-1)*4)+i+1)
            hizb1 = cur1.fetchone()
            sura1 = hizb1["sura"]
            aya1 = hizb1["aya"]
            if (aya1 == 1):
                sura1 = sura1 - 1
                conn2 = mysql.connect()
                cur2 = conn2.cursor(pymysql.cursors.DictCursor)
                cur2.execute("SELECT * FROM sura WHERE id = %s",sura1)
                hizb2 = cur2.fetchone()
                aya1 = hizb2['ayaNo']
            else :
                aya1 = aya1 - 1
            s =[]
            if(sura0 == sura1) :
                s.append([sura0,aya0,aya1])
            else :
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute("SELECT * FROM sura WHERE id = %s",sura0)
                sura = cur.fetchone()
                s.append([sura0,aya0,sura['ayaNo']])
                if (sura0 < sura1-1):
                    for i in range(sura0+1,sura1) :
                        conn = mysql.connect()
                        cur = conn.cursor(pymysql.cursors.DictCursor)
                        cur.execute("SELECT * FROM sura WHERE id = %s",i)
                        sura = cur.fetchone()
                        s.append([i,1,sura['ayaNo']])
                s.append([sura1,1,aya1])
            res.append([((hizbId-1)*4)+i,s])
        return json.dumps(res, ensure_ascii=False)

@app.route("/hizb/<int:hizb>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def hizb(hizb):
    if ( hizb == 60 ):
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM quran WHERE id >= 5949")
        quarter = cur.fetchall()
        return json.dumps(quarter, ensure_ascii=False)
    else :
        conn1 = mysql.connect()
        cur1 = conn1.cursor(pymysql.cursors.DictCursor)
        cur1.execute("SELECT * FROM hizb WHERE id = %s",hizb*4-3)
        hizb1 = cur1.fetchone()
        conn11 = mysql.connect()
        cur11 = conn11.cursor(pymysql.cursors.DictCursor)
        cur11.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(hizb1["sura"],hizb1["aya"]))
        hizb11 = cur11.fetchone()
        deb = hizb11["id"]
        conn2 = mysql.connect()
        cur2 = conn1.cursor(pymysql.cursors.DictCursor)
        cur2.execute("SELECT * FROM hizb WHERE id = %s",hizb*4+1)
        hizb2 = cur2.fetchone()
        conn22 = mysql.connect()
        cur22 = conn11.cursor(pymysql.cursors.DictCursor)
        cur22.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(hizb2["sura"],hizb2["aya"]))
        hizb22 = cur22.fetchone()
        fin =hizb22["id"]-1
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM quran WHERE id >= %s AND id <= %s",(deb,fin))
        hizb = cur.fetchall()
        return json.dumps(hizb, ensure_ascii=False)

@app.route("/page-detail/<int:pageId>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def pageDetail(pageId):
    if ( pageId == 604 ):
        res = [[112,1,4],[113,1,5],[114,1,6]]
        return json.dumps(res, ensure_ascii=False)
    else :
        conn0 = mysql.connect()
        cur0 = conn0.cursor(pymysql.cursors.DictCursor)
        cur0.execute("SELECT * FROM page WHERE id = %s",pageId)
        page0 = cur0.fetchone()
        sura0 = page0["sura"]
        aya0 = page0["aya"]
        conn1 = mysql.connect()
        cur1 = conn1.cursor(pymysql.cursors.DictCursor)
        cur1.execute("SELECT * FROM page WHERE id = %s",pageId+1)
        page1 = cur1.fetchone()
        sura1 = page1["sura"]
        aya1 = page1["aya"]
        if (aya1 == 1):
            sura1 = sura1 - 1
            conn2 = mysql.connect()
            cur2 = conn2.cursor(pymysql.cursors.DictCursor)
            cur2.execute("SELECT * FROM sura WHERE id = %s",sura1)
            page2 = cur2.fetchone()
            aya1 = page2['ayaNo']
        else :
            aya1 = aya1 - 1
        res =[]
        if(sura0 == sura1) :
            res.append([sura0,aya0,aya1])
        else :
            conn = mysql.connect()
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute("SELECT * FROM sura WHERE id = %s",sura0)
            sura = cur.fetchone()
            res.append([sura0,aya0,sura['ayaNo']])
            if (sura0 < sura1-1):
                for i in range(sura0+1,sura1) :
                    conn = mysql.connect()
                    cur = conn.cursor(pymysql.cursors.DictCursor)
                    cur.execute("SELECT * FROM sura WHERE id = %s",i)
                    sura = cur.fetchone()
                    res.append([i,1,sura['ayaNo']])
            res.append([sura1,1,aya1])
        return json.dumps(res, ensure_ascii=False)

@app.route("/page/<int:page>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def page(page):
    if ( page == 604 ):
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM quran WHERE id >= 6222")
        pag = cur.fetchall()
        return json.dumps(pag, ensure_ascii=False)
    else :
        conn1 = mysql.connect()
        cur1 = conn1.cursor(pymysql.cursors.DictCursor)
        cur1.execute("SELECT * FROM page WHERE id = %s",page)
        page1 = cur1.fetchone()
        conn11 = mysql.connect()
        cur11 = conn11.cursor(pymysql.cursors.DictCursor)
        cur11.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(page1["sura"],page1["aya"]))
        page11 = cur11.fetchone()
        deb = page11["id"]
        conn2 = mysql.connect()
        cur2 = conn1.cursor(pymysql.cursors.DictCursor)
        cur2.execute("SELECT * FROM page WHERE id = %s",page+1)
        page2 = cur2.fetchone()
        conn22 = mysql.connect()
        cur22 = conn11.cursor(pymysql.cursors.DictCursor)
        cur22.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(page2["sura"],page2["aya"]))
        page22 = cur22.fetchone()
        fin = page22["id"]-1
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM quran WHERE id >= %s AND id <= %s",(deb,fin))
        pag = cur.fetchall()
        return json.dumps(pag, ensure_ascii=False)

@app.route("/juz/<int:juzId>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def juz(juzId):
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT * FROM juz WHERE id = %s",juzId)
    juz = cur0.fetchone()
    deb = juz["deb"]
    fin = juz["fin"]
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran WHERE id >= %s AND id <= %s",(deb,fin))
    juzs = cur.fetchall()
    return json.dumps(juzs, ensure_ascii=False)

@app.route("/juz-detail/<int:juzId>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def juzDetail(juzId):
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT * FROM juz WHERE id = %s",juzId)
    juz = cur0.fetchone()
    deb = juz["deb"]
    fin = juz["fin"]
    conn1 = mysql.connect()
    cur1 = conn1.cursor(pymysql.cursors.DictCursor)
    cur1.execute("SELECT * FROM quran WHERE id = %s",deb)
    juz1 = cur1.fetchone()
    conn2 = mysql.connect()
    cur2 = conn2.cursor(pymysql.cursors.DictCursor)
    cur2.execute("SELECT * FROM quran WHERE id = %s",fin)
    juz2 = cur2.fetchone()
    res = []
    if(juz1['suraId'] == juz2['suraId']) :
        res.append([juz1['suraId'],juz1['ayaId'],juz2['ayaId']])
    else :
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM sura WHERE id = %s",juz1['suraId'])
        sura = cur.fetchone()
        res.append([juz1['suraId'],juz1['ayaId'],sura['ayaNo']])
        if (juz1['suraId'] < juz2['suraId']-1):
            for i in range(juz1['suraId']+1,juz2['suraId']) :
                conn = mysql.connect()
                cur = conn.cursor(pymysql.cursors.DictCursor)
                cur.execute("SELECT * FROM sura WHERE id = %s",i)
                sura = cur.fetchone()
                res.append([i,1,sura['ayaNo']])
        res.append([juz2['suraId'],1,juz2['ayaId']])
    return json.dumps(res, ensure_ascii=False)

@app.route("/getJuz/<int:sura>/<int:aya>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def getJuz(sura,aya):
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT * FROM quran WHERE suraId = %s and ayaId = %s",(sura,aya))
    aya0 = cur0.fetchone()
    index = aya0["id"]
    conn1 = mysql.connect()
    cur1 = conn1.cursor(pymysql.cursors.DictCursor)
    cur1.execute("SELECT * FROM juz WHERE deb <= %s and fin >= %s",(index,index))
    juz = cur1.fetchone()
    return json.dumps(juz, ensure_ascii=False)

@app.route("/getPage/<int:sura>/<int:aya>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def getPage(sura,aya):
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT * FROM page WHERE sura <= %s and aya <= %s ORDER BY id DESC LIMIT 1",(sura,aya))
    aya0 = cur0.fetchone()
    return json.dumps(aya0, ensure_ascii=False)

@app.route("/getHizb/<int:sura>/<int:aya>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def getHizb(sura,aya):
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT * FROM hizb WHERE sura <= %s and aya <= %s ORDER BY id DESC LIMIT 1",(sura,aya))
    aya0 = cur0.fetchone()
    return json.dumps(aya0, ensure_ascii=False)

@app.route("/suras", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def suras():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM sura")
    sura = cur.fetchall()
    resp = jsonify(sura)
    return resp

@app.route("/sura/<int:suraId>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def sura(suraId):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran WHERE suraId = %s",suraId)
    quran = cur.fetchall()
    resp = jsonify(quran)
    return resp

@app.route("/find/<text>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def find(text):
    colorNext = ['AliceBlue','AntiqueWhite','Aqua','Aquamarine','Azure','Beige','Bisque','BlanchedAlmond','Blue','BlueViolet','Brown','BurlyWood','CadetBlue','Chartreuse','Chocolate','Coral','CornflowerBlue','Cornsilk','Crimson','Cyan','DarkCyan','DarkGoldenRod','DarkGrey','DarkGreen','DarkKhaki','DarkMagenta','DarkOliveGreen','DarkOrange','DarkOrchid','DarkRed','DarkSalmon','DarkSeaGreen','DarkSlateBlue','DarkTurquoise','DarkViolet','DeepPink','DeepSkyBlue','DimGray','DimGrey','DodgerBlue','FireBrick','FlralWhite','ForestGreen','Fuchsia','Gainsboro','GhostWhite','GoldenRod','Gray','Grey','Green','GreenYellow','HoneyDew','HotPink','IndianRed','Indigo','Ivory','Khaki','Lavender','LavenderBlush','LawnGreen','LemonChiffon','LightBlue']
    colorLast =['LightCoral','LightCyan','LightGoldenRodYellow','LightGray','LightGreen','LightPink','LightSalmon','LightSeaGreen','LightSkyBlue','Lime','Linen','Magenta','Maroon','MediumAquaMarine','MediumOrchid','MediumPurple','MediumSeaGreen','MediumSlateBlue','MediumSpringGreen','MediumTurquoise','MediumVioletRed','MistyRose','NavajoWhite','Navy','OldLace','Olive','Orange','OrangeRed','Orchid','PaleGoldenRod','PaleGreen','PaleTurquoise','PaleVioletRed','PapayaWhip','PeachPuff','Peru','Pink','Plum','PowderBlue','Purple','RebeccaPurple','Red','RosyBrown','RoyalBlue','Salmon','SandyBrown','SeaGreen','SeaShell','Sienna','Silver','SkyBlue','SlateBlue','SpringGreen','SteelBlue','Tan','Teal','Thistle','Tomato','Turquoise','Violet','Wheat','YellowGreen']
    idL = 0
    idN = 0
    ss = '%' + text + '%'
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran_simple WHERE aya LIKE %s", ss)
    quran = cur.fetchall()
    n = len(text)
    sura = {}
    for aya in quran :
        r = []
        str = []
        i = 0
        x = -n
        while True:
            if(aya['aya'].find(text,x+n) == -1):
                break
            else :
                i = i + 1
                x = aya['aya'].find(text,x+n)
                r.append(x)
                if((i == 1) and (x != 0)):
                    str.append([-1,1,aya['aya'][0:x]])
                else :
                    if((i != 1) and (r[i-2]+n != x)):
                        str.append([1,i-1,aya['aya'][r[i-2]+n:x]])
                str.append([0,aya['aya'][x:x+n]])
        if(r[i-1]+n != len(aya['aya'])):
            str.append([1,i,aya['aya'][r[i-1]+n:len(aya['aya'])]])
        if (aya['suraId'] in sura):
            sura[aya['suraId']] += i
            aya['deb'] = 1
        else :
            sura[aya['suraId']] = i
            aya['deb'] = 0
        aya['nb'] = i
        aya['aya'] = str
    liste = []
    for aya in quran :
        aya['no'] = sura[aya['suraId']]
        for txt in aya['aya'] :
            if(txt[0] == 1):
                xx = nx(quran.index(aya),txt[1],quran,txt[2])
                if(len(xx) != 0):
                    liste.append(xx)
    maxL(liste)
    for el in liste :
        k = el[0]
        color = colorNext[idN]
        if(idN == 61):
            idN = 0
        else :
            idN += 1
        for j in range(1,len(el)) :
            for u in range(len(quran[el[j][0]]['aya'])) :
                if (quran[el[j][0]]['aya'][u][0] == 1) and (quran[el[j][0]]['aya'][u][1] == el[j][1]) :
                    str1 = quran[el[j][0]]['aya'][u][2][0:k]
                    str2 = ''
                    if(k != len(quran[el[j][0]]['aya'][u][2])):
                        str2 = quran[el[j][0]]['aya'][u][2][k:len(quran[el[j][0]]['aya'][u][2])]
                        cc = quran[el[j][0]]['aya'][u][1]
                    u1 = [2,str1,color]
                    quran[el[j][0]]['aya'][u] = u1
                    if ((str2 != '') and (quran[el[j][0]]['aya'][u][1] == quran[el[j][0]]['nb'])):
                        u2 = [3,str2]
                        quran[el[j][0]]['aya'].insert(u+1,u2)
                    elif (str2 != ''):
                        if(quran[el[j][0]]['nb'] == cc):
                            u2 = [3,cc + 1,str2]
                            quran[el[j][0]]['aya'].insert(u+1,u2)
                        else :
                            u2 = [-1,cc + 1,str2]
                            quran[el[j][0]]['aya'].insert(u+1,u2)


    liste2 = []
    for aya in quran :
        for txt in aya['aya'] :
            if(txt[0] == -1):
                xx = ls(quran.index(aya),txt[1],quran,txt[2])
                if(len(xx) != 0):
                    liste2.append(xx)
    maxL(liste2)
    for el in liste2 :
        k = el[0]
        color = colorLast[idL]
        if(idL == 61):
            idL = 0
        else :
            idL += 1
        for j in range(1,len(el)) :
            for u in range(len(quran[el[j][0]]['aya'])) :
                if (quran[el[j][0]]['aya'][u][0] == -1) and (quran[el[j][0]]['aya'][u][1] == el[j][1]) :
                    str1 = ''
                    str2 = ''
                    n1 = len(quran[el[j][0]]['aya'][u][2])
                    if(k != n1):
                        str1 = quran[el[j][0]]['aya'][u][2][0:n1-k]
                        str2 = quran[el[j][0]]['aya'][u][2][n1-k:n1]
                        u1 = [3,str1]
                        u2 = [2,str2,color]
                        quran[el[j][0]]['aya'][u] = u1
                        quran[el[j][0]]['aya'].insert(u+1,u2)
                    else :
                        str2 = quran[el[j][0]]['aya'][u][2]
                        u2 = [2,str2,color]
                        quran[el[j][0]]['aya'][u] = u2
    return json.dumps(quran, ensure_ascii=False)

def maxL(liste) :
    res = []
    n = len(liste)
    while (n>1):
        m = 0
        for i in range(n) :
            if(liste[i][0] < liste[m][0]) :
                m = i
        if (m != n-1) :
            s = liste[n-1]
            liste[n-1] = liste[m]
            liste[m] = s
        n -= 1

def nx(a,b,quran,str):
    res = []
    result = []
    for i in range(len(quran)) :
        for txt in quran[i]['aya'] :
            if (txt[0] == 1)  :
                if (not((i == a) and (txt[1] == b))):
                    j = diff(txt[2],str)
                    if ((j != 0) and (j != 1) and (j != 2) and (j != 3)) :
                        res.append([i,txt[1],j])
    if (len(res) != 0) :
        m = 0
        for k in res :
            if (k[2] > m) :
                m = k[2]
        result.append(m)
        result.append([a,b])
        for k in res :
            if (k[2] == m):
                result.append([k[0],k[1]])
    return result

def ls(a,b,quran,str):
    res = []
    result = []
    for i in range(len(quran)) :
        for txt in quran[i]['aya'] :
            if (txt[0] == -1)  :
                if (not((i == a) and (txt[1] == b))):
                    j = diff2(txt[2],str)
                    if ((j != 0) and (j != 1) and (j != 2) and (j != 3)) :
                        res.append([i,txt[1],j])
    if (len(res) != 0) :
        m = 0
        for k in res :
            if (k[2] > m) :
                m = k[2]
        result.append(m)
        result.append([a,b])
        for k in res :
            if (k[2] == m):
                result.append([k[0],k[1]])
    return result

def diff(str1,str2) :
    n1 = len(str1)
    n2 = len(str2)
    i = 0
    while (i < n1) and (i < n2):
        if(str1[i] == str2[i]):
            i += 1
        else :
            break
    return i

def diff2(str1,str2) :
    n1 = len(str1)
    n2 = len(str2)
    i = 0
    while (i < n1) and (i < n2):
        if(str1[n1-i-1] == str2[n2-1-i]):
            i += 1
        else :
            break
    return i

if __name__ == "__main__":
    app.run()
