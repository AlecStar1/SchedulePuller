import requests
from xml.dom.minidom import parse, parseString
from bs4 import BeautifulSoup

url = "https://campus.ps.rit.edu/psc/RITXCPRD_15/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CRSE_INFO_FL.GBL"
CRSE_ID = 115227
querystring = {"Page":"SSR_CRSE_INFO_FL",
"Action":"U",
"ACAD_CAREER":"UGRD",
"CRSE_ID":str(CRSE_ID),
"CRSE_OFFER_NBR":"1",
"INSTITUTION":"RIT01",
"STRM":"2245",
"ICAJAX":"1",
"ICMDTarget":"start",
"ICPanelControlStyle":" pst_side1-fixed pst_panel-mode "}

payload = ""
days_of_week = {
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6,
    "Sunday": 7
}
headers = {"Cookie": "PS_TokenSite=https://campus.ps.rit.edu/psp/RITXCPRD/?ritxcprd-lnxmt-pub-PORTAL-PSJSESSIONID;_shibsession_63616d70757368747470733a2f2f63616d7075732e70732e7269742e6564752f73686962626f6c657468=_975c02fd81f864e78139252be15b290a;PS_TOKEN=pwAAAAQDAgEBAAAAvAIAAAAAAAAsAAAABABTaGRyAk4Abwg4AC4AMQAwABTg1d2B+lISUnp35SMVqVdZG06/XWcAAAAFAFNkYXRhW3icHYw7DkBAFEWPT5R2MsIYxtSCTiT0olArbM/i3My7ybmf4j1AnqVJIv9S4pUXNy+egZaOYmJlodzYmTk4GZWcpcbiMDSSUfORjkq9Fy1BdHrSagkSP5X+C8A="}
try:
    ll = parse(f"cached/{CRSE_ID}.cache")
except: 
    response = requests.request("GET",
        url,
        data=payload,
        headers=headers,
        params=querystring)
    ll = parseString(response.text)
    assert ll.getElementsByTagName("FIELD")[-3].getAttribute("id") == "divPAGECONTAINER_TGT"
    with open(f"./cached/{CRSE_ID}.cache", "w+", encoding="UTF-8") as fv:
        fv.write(response.text)

   

guh = ll.getElementsByTagName("FIELD")[-3]
assert guh.getAttribute("id") == "divPAGECONTAINER_TGT"
oo = BeautifulSoup(guh.firstChild.wholeText, features="lxml")
ouf = []
    # print(i.getAttribute("id"))
for i in ["SSR_CRSE_INFO_V_COURSE_TITLE_LONG","SSR_CRSE_INFO_V_SSS_SUBJ_CATLG","SSR_CLSRCH_F_WK_UNITS_RANGE"]:
    ouf.append(oo.find("span", attrs={'id':i}).text)
ouf[1].replace(' ', '-')

def TtoM(time):
    HR, MIN = time.split(":")
    out = int(HR) * 60
    out += int(MIN[0:2])
    print(MIN[-2:-1])
    if(MIN[-2:-1] == "P" and int(HR) != 12):
        out += 720
    return out

ARG = oo.find("tbody").findChildren("tr")
lectures = []
for i in ARG:
    stats = [ugh.find('span').getText() for ugh in i.findChildren("td")]
    lecturHall = stats[6].split("\n")
    TIMEHELL = [[stats[5].split("\n")[i],stats[5].split("\n")[i+1]] for i in range(0,len(stats[5].split("\n")),2)]
    puh = []
    for i in range(len(TIMEHELL)):
        for b in TIMEHELL[i][0].split(" "):
            puh.append({
                "bldg":{"code":lecturHall[i].split("(")[1].split(")")[0],"number":None},
                "room":lecturHall[i].split("-")[-1] if lecturHall[i] is not "Online" else lecturHall[i],
                "day":days_of_week[b],
                "start":TtoM(TIMEHELL[i][1].split(" to ")[0]),
                "end":TtoM(TIMEHELL[i][1].split(" to ")[1]),
                "off_campus":False
                })
    lectures.append({
        "id": f"{stats[3].split('-')[-2].strip()}",
        "title":ouf[0],
        "type":"",
        "instructor":stats[7],
        "curenroll": int(''.join(filter(str.isdigit, stats[8].split(' of ')[0]))),
        "maxenroll": int(stats[8].split(' of ')[1]),
        "department" : {"code":ouf[1].split(' ')[0],"number":None},
        "course":ouf[1].split(' ')[1],
        "section":f"{stats[3].split('-')[-1]}",
        "courseNum": f"{ouf[1].replace(' ', '-')}-{stats[3].split('-')[-1]}",
        "courseParentNum": f"{ouf[1].replace(' ', '-')}",
        "courseId": str(CRSE_ID),
        "online":any(i["room"] is "Online" for i in puh),
        "credits": str(int(float(ouf[2]))),
        "times":puh
            
    })

# FFF = {}
# for q in lectures:
#     FFF

print(lectures)