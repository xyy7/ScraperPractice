import urllib.request

pdf_path = "https://arxiv.org/pdf/1908.02111"


def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

# 可以下载pdf，但是有时候也会出现不成功
download_file(pdf_path, "Test")