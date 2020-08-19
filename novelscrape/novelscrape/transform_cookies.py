from http.cookies import SimpleCookie
import json

# convert cookie string to dict
# put cookie string in rawdata, see https://stackoverflow.com/questions/12908881/how-to-copy-cookies-in-google-chrome/24961735 for how to get cookie sting from Chrome
rawdata = 'areaId=2; __jdv=122270672|www.google.com|-|referral|-|1597548845879; __jdu=159754884587778156571; shshshfp=bec5dc7fd46f6270f3ed95f7f200dba3; shshshfpa=d8ce5bb1-6c4c-c71f-583f-df6af5bd75a6-1597548914; shshshfpb=pu39iXkUki6Y%2FGB5j45gMnw%3D%3D; ipLoc-djd=2-2830-51803-0; _c_id=zmwe799uv349cf6mla21597807649515nu4j; cid=NWRHOTU4NmZTOTE2N2dMMjMyOHhMMDc2MWtONjM2MnpUOTk4M3FaOTM2NGpSNjMw; pinId=qhSIsmKNO3wFm4AbPqsTS7V9-x-f3wj7; pin=jd_5ecd476f38f40; unick=jd_180617icu; _tp=v8zTB2vhDo7kT%2FByPjcjtfychH2aITkZvJqZ8ssLWAM%3D; _pst=jd_5ecd476f38f40; __jda=122270672.159754884587778156571.1597548846.1597806870.1597825594.6; __jdc=122270672; _s_id=nf2mzxwjihkqeubo5og1597827463571m5ft; nf2mzxwjihkqeubo5og1597827463571m5ft=320; DeviceSeq=16d5f410242a4c4e91757404587ed6b9; mp=18013815083; alc=dmfmPijqtXW1j9F0o032YA==; _t=oeqWiMv7nB2UaNHSvNcxzyfKa+mzJimoqFGwG5D16lc=; 3AB9D23F7A4B3C9B=X7WNQTUDRENNPU3B6ZQFVVR5AFNK6KZZJ6MSETKYLLFCEVXC7Y2LASNGYGJLEVVWASFDY7PZBJ2GNDKKHFNOE4O5XE; wlfstk_smdl=4hm9isjy8z1fxskqi1xsdxlpag7ysgqx; TrackID=1XHbbV2iXHsgU7mfjtFjpsMvkFQoI9o4W29q9eFs44n_cmmxAJnSu2Pi6WvlZOKFX2-QYOUaCP2LE2GPkHwJr3WJuAFjy6eV9fl3CZq2cdqsQJYIsESX3COnYtUb8g0Lc; thor=B8751B3121D5374DAAFE628EEB9D9541ADCBD255A8B566980DD97DF4F7A8105C977C394507A468AC2F0E6C3ED1B42437684E6BDCF5A984E42B72D47B0A171D377441C0A00187D55A1002579D694E4184B7E2FDACB2975D8577CB1A6DF3F1D182789FF4D252B5BF15A9BB6E66DB35C77BFAE335AA6E619697A4E8B54944B648F1BBAC184E88A6C641271E6BEB815E9AA3F24281AB7446B648C3495645530D768C; ceshi3.com=103; shshshsID=f4f9b66be2dff6d27a0f26e45b769f46_5_1597827520980; __jdb=122270672.10.159754884587778156571|6.1597825594'
cookie = SimpleCookie()
cookie.load(rawdata)

cookies = dict()
for key, morsel in cookie.items():
    cookies[key] = morsel.value

# write to JSON file
js = json.dumps(cookies)

with open('./novelscrape/cookies.json', 'w') as f:
    f.write(js)