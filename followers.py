import requests
from xml.dom.minidom import parse, parseString
from bs4 import BeautifulSoup

url = "https://campus.ps.rit.edu/psc/RITXCPRD_15/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_CRSE_INFO_FL.GBL"
CRSE_ID = 114227
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
headers = {"Cookie": "PS_TokenSite=https://campus.ps.rit.edu/psp/RITXCPRD/?ritxcprd-lnxmt-pub-PORTAL-PSJSESSIONID;"+OTHERCOOKIESUNLISTED}
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
ARG = oo.find("tbody").findChildren("tr")
lectures = []
for i in ARG:
    stats = [ugh.find('span').getText() for ugh in i.findChildren("td")]
    lectures.append({
        "title":ouf[0],
        "instructor":stats[7],
        "curenroll": int(''.join(filter(str.isdigit, stats[8].split(' of ')[0]))),
        "maxenroll": int(stats[8].split(' of ')[1]),
        "courseNum": f"{ouf[1].replace(' ', '-')}-{stats[3].split('-')[-1]}",
        "courseParentNum": f"{ouf[1].replace(' ', '-')}",
        "courseId": str(CRSE_ID),
        "id": "353441",
        "online":False,
        "credits": str(int(float(ouf[2])))
    })

# FFF = {}
# for q in lectures:
#     FFF

print(lectures)