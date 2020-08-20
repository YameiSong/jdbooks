from http.cookies import SimpleCookie
import json

# convert cookie string to dict
# put cookie string in rawdata, see https://stackoverflow.com/questions/12908881/how-to-copy-cookies-in-google-chrome/24961735 for how to get cookie sting from Chrome
rawdata = 'areaId=2; __jdv=122270672|www.google.com|-|referral|-|1597548845879; cud=3308eb6d123f99ef523b2e9c203ca41c; __jdu=159754884587778156571; shshshfp=bec5dc7fd46f6270f3ed95f7f200dba3; shshshfpa=d8ce5bb1-6c4c-c71f-583f-df6af5bd75a6-1597548914; shshshfpb=pu39iXkUki6Y%2FGB5j45gMnw%3D%3D; ipLoc-djd=2-2830-51803-0; cid=NWRHOTU4NmZTOTE2N2dMMjMyOHhMMDc2MWtONjM2MnpUOTk4M3FaOTM2NGpSNjMw; pinId=qhSIsmKNO3wFm4AbPqsTS7V9-x-f3wj7; pin=jd_5ecd476f38f40; unick=jd_180617icu; _tp=v8zTB2vhDo7kT%2FByPjcjtfychH2aITkZvJqZ8ssLWAM%3D; _pst=jd_5ecd476f38f40; __jda=122270672.159754884587778156571.1597548846.1597825594.1597888751.7; __jdc=122270672; cvt=7; 3AB9D23F7A4B3C9B=X7WNQTUDRENNPU3B6ZQFVVR5AFNK6KZZJ6MSETKYLLFCEVXC7Y2LASNGYGJLEVVWASFDY7PZBJ2GNDKKHFNOE4O5XE; csn=3; wlfstk_smdl=2ouhdtqeapcvb4tkshy8ju0g7p188afb; TrackID=1sleRZ2qzDZ5F5HisgKZ6t-ODIYSYW9OFF--L_cf9pNe__93MWYYfhUsa6KhMJ9gbL8TZZsSc1kJUxFeOwdEKXFGz0E_p9v0oCvA38W3ixYUjo0UtArNIq_kDOHiivr3A; thor=B8751B3121D5374DAAFE628EEB9D9541ADCBD255A8B566980DD97DF4F7A8105C71B010684041B38EBD081938407AC5530496E09C64060D0154F89240F039FF3D0F350E65FA64CFD5DCBD52F301D5A6269AEE0CDB6EF18E92865C5E338804741C4EC5FB1BF60707F43D52B4209E84760B0802D042CFC5C49E7BCB8560A815ACCE3D287BC27C14B6D248B9AC19494BD7E2274F6307765FE5A36F4D30CAC85CEA54; ceshi3.com=103; logining=1; __jdb=122270672.4.159754884587778156571|7.1597888751'
cookie = SimpleCookie()
cookie.load(rawdata)

cookies = dict()
for key, morsel in cookie.items():
    cookies[key] = morsel.value

# write to JSON file
js = json.dumps(cookies)

with open('./novelscrape/cookies.json', 'w') as f:
    f.write(js)