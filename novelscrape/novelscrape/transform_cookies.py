from http.cookies import SimpleCookie
import json

# convert cookie string to dict
# put cookie string in rawdata, see https://stackoverflow.com/questions/12908881/how-to-copy-cookies-in-google-chrome/24961735 for how to get cookie sting from Chrome
rawdata = 'areaId=2; __jdv=122270672|www.google.com|-|referral|-|1597548845879; __jdu=159754884587778156571; shshshfp=bec5dc7fd46f6270f3ed95f7f200dba3; shshshfpa=d8ce5bb1-6c4c-c71f-583f-df6af5bd75a6-1597548914; shshshfpb=pu39iXkUki6Y%2FGB5j45gMnw%3D%3D; ipLoc-djd=2-2830-51803-0; cid=NWRHOTU4NmZTOTE2N2dMMjMyOHhMMDc2MWtONjM2MnpUOTk4M3FaOTM2NGpSNjMw; pinId=qhSIsmKNO3wFm4AbPqsTS7V9-x-f3wj7; pin=jd_5ecd476f38f40; unick=jd_180617icu; _tp=v8zTB2vhDo7kT%2FByPjcjtfychH2aITkZvJqZ8ssLWAM%3D; _pst=jd_5ecd476f38f40; __jda=122270672.159754884587778156571.1597548846.1597976031.1598148309.10; __jdc=122270672; wlfstk_smdl=zci4jqvmgur0vmkotz9ofd7ze649uhwu; TrackID=1to_BoOPZVFmk-wxhD77ojBoLPEclWMw7MgvG8KeZAU2v8UuFLZiQrTiwMZSbvMLkaGVxGoKvetzku3FegsjcLixoGJ-flqrboIJpyNzOCmoH5ZkKB81CkDZf2LAF9ffV; thor=B8751B3121D5374DAAFE628EEB9D9541ADCBD255A8B566980DD97DF4F7A8105CC0BC0A1C7ECD5096219CDE08347B4796431CFF84A4DE7EFB79A1F89DC19D7C0946E94024DB917E209769F9A343E48CA8E338FCD4CC9BCFE0BE2523FC18E9571EBEB5879EA3756CB7EF6D5FF038831914F5519BA5E3F99914FC0DB6634F6A5768EF1C92ED1F261AE92E9FFE85BA66CA6591A4BDAA2D2C05CFB14DA2A75237758E; ceshi3.com=103; 3AB9D23F7A4B3C9B=RD72SIBHI3RAOGZUV4NEH7NECEXAEOO5VPYJK3Y5LCP2AFGJHARIIZUPSICLHSCH5D4FLDNABQR3Y2LMTM5ITL5FIM; __jdb=122270672.10.159754884587778156571|10.1598148309'
cookie = SimpleCookie()
cookie.load(rawdata)

cookies = dict()
for key, morsel in cookie.items():
    cookies[key] = morsel.value

# write to JSON file
js = json.dumps(cookies)

with open('./novelscrape/cookies.json', 'w') as f:
    f.write(js)
