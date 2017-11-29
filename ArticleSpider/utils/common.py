# -*- coding: utf-8 -*-
#author = "王栎汉 2017年11月28日"
import hashlib
def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
# print(get_md5("http://blog.jobbole.com/all-posts/"))
