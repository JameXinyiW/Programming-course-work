
url ='https://p1.music.126.net/ElodFpCyC1ZccjGE3ZpN7Q==/19140298416647191.jpg?param=140y140'

from urllib import request
path =    'D:\\pycharm code\\week12\\图片\\'

import requests

headers={

                "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",

                "cookie":
'_ns=NS1.2.1527376066.1641570966; _ntes_nnid=7a17336b9171afacc52cd2d4d6281e48,1642329090851; _ntes_nuid=7a17336b9171afacc52cd2d4d6281e48; JSESSIONID-WYYY=ZSl51kxbrvvWYl/MOBhanGP98Z9dpMREaTdfK\oiTEtd+a5762iYb3gvhy1bR2CeIBFMx6hZAtjf8K3maK/dDOsnCGuZJSlCfoYxq8b7eGgudyuKmzs6tE0qtDZ0TT3Bptp1bO/1dxJG7CoPcwYfnVNJBa8P9yPZllRZS+//+UBdSeBl:1669255195949; _iuqxldmzr_=32; NMTID=00OaZyVA7D9TgLhHUekm5RJJato4IgAAAGEp0FtMQ; WEVNSM=1.0.0; WNMCID=ujngmx.1669253396335.01.0; WM_NI=Hbp6hQHQLf16aNuApFs8E8xwkCqFgb9kLX9I3MCbxKcJd5hjecFG/O+fMfQ1u/O7zQCLn1ZDok45H6xSxWd0Z9xwMevSgUHkZjPvxvo0ki3SFOgwo6rQYSSLJ5iYOaC0TVY=; WM_NIKE=9ca17ae2e6ffcda170e2e6ee86f944a7bfbfb3c74bb5b88ab2d55e929f8a87d5698befbbbbd447ed88bd83d42af0fea7c3b92a8cbec0d7eb5b8c8f8487b43ea392bba2f34eb1e88bd9fb7da99dbfa7e66afbb584b9bc43f1938d83fb41a196acd6eb62a7bd8aa8ae45e9ba8387d43bb7f181d8f95b8194a2d2d950adb5fcd6cb3ebc8db8b8e73c9ae7b898d06fb68da9b6cb619ab6a097fb7eadf0a58ab2598691a998ee3eb28f97b4d2488aeba7bace6b81f09cb7dc37e2a3; WM_TID=xaEDVs55L4lARAVFVBeQcNl+MVJvD9aU'
}
url1='https://music.163.com/discover/playlist/?order=hot&cat=%E8%AF%B4%E5%94%B1&limit=35&offset='\
        +str(1)
r = requests.get(url1, timeout=1, headers=headers)
print(r.apparent_encoding)
