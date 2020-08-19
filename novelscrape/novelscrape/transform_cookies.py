from http.cookies import SimpleCookie
import json

# convert cookie string to dict
# put cookie string in rawdata, see https://stackoverflow.com/questions/12908881/how-to-copy-cookies-in-google-chrome/24961735 for how to get cookie sting from Chrome
rawdata = 'areaId=2; __jdv=122270672|www.google.com|-|referral|-|1597548845879; __jdu=159754884587778156571; shshshfp=bec5dc7fd46f6270f3ed95f7f200dba3; shshshfpa=d8ce5bb1-6c4c-c71f-583f-df6af5bd75a6-1597548914; shshshfpb=pu39iXkUki6Y%2FGB5j45gMnw%3D%3D; ipLoc-djd=2-2830-51803-0; __jdc=122270672; __jda=122270672.159754884587778156571.1597548846.1597803247.1597806870.5; _c_id=zmwe799uv349cf6mla21597807649515nu4j; _s_id=8ylcv8n1a21xu2e0dnk1597807649515f9hj; 8ylcv8n1a21xu2e0dnk1597807649515f9hj=1481; alc=iAzp/yacLhHI335zU/ghYA==; wlfstk_smdl=5syyakhh4nbv9qg2a5726r6gd9c32n67; _t=rRAHPTglQh0NEZMynZrt4uog79zzGIUZOvsB/R4rYUI=; cid=NWRHOTU4NmZTOTE2N2dMMjMyOHhMMDc2MWtONjM2MnpUOTk4M3FaOTM2NGpSNjMw; thor=B8751B3121D5374DAAFE628EEB9D9541ADCBD255A8B566980DD97DF4F7A8105C80B15E0776DFA2358D6A22FCBE97F76B933647BFE872B54D8CDBC1198D01D604E7F24EE393B58620792E36887FD9F28F5766B5C8583E87FB5867007BA5F444487F87AFB9625CAF78F65E682E9B0BEB2F3388C5E7EDDFD630015EAA4233C26FCDEFCBA248CE3D2EB401CF2FA47C869B1DD357A087972DA046F8F9E72CCF8E50BF; pinId=qhSIsmKNO3wFm4AbPqsTS7V9-x-f3wj7; pin=jd_5ecd476f38f40; unick=jd_180617icu; ceshi3.com=103; _tp=v8zTB2vhDo7kT%2FByPjcjtfychH2aITkZvJqZ8ssLWAM%3D; _pst=jd_5ecd476f38f40; 3AB9D23F7A4B3C9B=RD72SIBHI3RAOGZUV4NEH7NECEXAEOO5VPYJK3Y5LCP2AFGJHARIIZUPSICLHSCH5D4FLDNABQR3Y2LMTM5ITL5FIM; shshshsID=373ba48084d28dac2a725d7b9825c727_3_1597807898565; __jdb=122270672.7.159754884587778156571|5.1597806870'
cookie = SimpleCookie()
cookie.load(rawdata)

cookies = dict()
for key, morsel in cookie.items():
    cookies[key] = morsel.value

# write to JSON file
js = json.dumps(cookies, indent=4)

with open("./novelscrape/cookies.json", "w") as f:
    f.write(js)