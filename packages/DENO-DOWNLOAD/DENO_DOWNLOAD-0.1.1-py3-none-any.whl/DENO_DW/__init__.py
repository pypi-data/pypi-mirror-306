import requests
import re
from clint.textui import progress
import os
os.system('cls' if os.name == 'nt' else 'clear')
def TIKTOK(url,namefile):
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__gads=ID=729ca1c9b9df3946:T=1730510571:RT=1730513490:S=ALNI_MYgFrEJbKHOqaE_XBeqvb-wy_0jcw; __gpi=UID=00000f5d9de877dd:T=1730510571:RT=1730513490:S=ALNI_Mbi_Y6XN6E32iD273N1oXue3hrkDg; __eoi=ID=9c3e2848f6398a95:T=1730510571:RT=1730513490:S=AA-AfjZ1JHYzBaPNjUH8apjBVMUz; FCNEC=%5B%5B%22AKsRol-9PUXQfBPwo9blFF_bc8aO63-okwi9KE2N2bsyPOIXGFGjbSqI_UlTdYL6BSez3uAfm5L4BeGVny86LnA0UNiRNHsd2jHmwq-FtSpZTSa9KccNS-uc32O3Zg450ziWY5lXfJ3RIjElqd9hhFGtNZPhEhEDAQ%3D%3D%22%5D%5D',
        'dnt': '1',
        'origin': 'https://snaptik.net',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://snaptik.net/vi',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    baseurl = 'https://snaptik.net/api/ajaxSearch'
    data = {
        'q': url,
        'lang': 'vi',
        }
    try : 
        response = requests.post(baseurl,data=data).text
        TOKEN = re.findall('href=.*?</a>',response)
        TOKENHD = ''.join([i for i in TOKEN if 'Tải xuống MP4 HD' in i])
        TOKENHD = TOKENHD.split('token=')[1].split('\\"')[0]
        downloadurl = requests.get(f'https://dl.snapcdn.app/get?token={TOKENHD}',stream= True).url
        download = requests.get(downloadurl,headers=headers,stream=True)
        total_length = int(download.headers.get('content-length'))
        path = f'{namefile}.mp4'
        with open(path, 'wb') as f:
            for chunk in progress.bar(download.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
    except IndexError:
        print('URL Không Chính xác ! ')
    except requests.exceptions.ConnectionError:
        print('Mất Kết Nối Mạng ! ')


def FACEBOOK(url,namefile):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '_ga=GA1.1.1181718376.1730521834; __gads=ID=9e69ada5379f127d:T=1730521831:RT=1730521831:S=ALNI_MYjDK8EV0YSUn2VhPkFHeF4cJ0JTg; __gpi=UID=00000f4cd9d91c50:T=1730521831:RT=1730521831:S=ALNI_MaQ6LSdfXPSANFzfAAiFKRmeXQMBA; __eoi=ID=bf92adb253c0987e:T=1730521831:RT=1730521831:S=AA-AfjZWX21dTlGyp-3YjeDPohRr; cf_clearance=bdkCVpqmsstFs7lFQj2Rbj_FhpACZxHKeDvaTu5_5tM-1730521844-1.2.1.1-Q452fNiVmhW5TT3OaqP7n_oz7v.xjJpirc83OxqkodC03u9NcwT34i9p9i5awrZd.QVuXTi6xGm_YjVwKoCMCkPZq4CKFZT1MLrvFmhKO8LvzcsWJLrevGa480Hfp_SdDmLAH1hlRqdptrV1XgCiXu9T8gmNIkoBlDE1sVzMLrLxAsO45o.oj4bOv5HjpFlJO7m0NP8PtCbS8x.RvSO4um3ofBfLfssMGXtMuQqLpKRK0wu31vEZ_8lfOzBZ_jL.uXtcWknKxP24LuQTlJn7mm7XDAEyceTWJ7SAPwiZQyWL8ClNF51lcu76eh0Qj45.ys9wIhzZSt2zMx16LxXOwIN.2a06r.m2rcNBRN4dvFZrHRk9QJDUPQGYsuJJ9bwh; FCNEC=%5B%5B%22AKsRol-UhGza8hWN_3LhiCjBpy26PUj0T1Ij_RUXtZMVwum7BMMi73lAQM1LwTSAY2NuN-T4UxhTIAh2lfEBxov6ylJyl2JTb8vwu6Fp2-KdSiDaGMIk0gSXF-MwUG6E49CKV6oQNRAtzmwn2-UhmMTnbwyv3oKR5A%3D%3D%22%5D%5D; _ga_82ERN9JZD3=GS1.1.1730521833.1.1.1730522083.58.0.0',
        'dnt': '1',
        'origin': 'https://fdown.net',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://fdown.net/index.php',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    try :
        response = requests.get('https://fdownloader.net/',headers=headers).text
        k_token = response.split('k_token="')[1].split('"')[0]
        k_exp = response.split('k_exp="')[1].split('"')[0]
        params = {
            'lang': 'en',
        }
        data = {
            'k_exp': k_exp,
            'k_token': k_token,
            'q': url,
            'lang': 'vi',
            'web': 'fdownloader.net',
            'v': 'v2',
            'w': '',
        }
        response2 = requests.post('https://v3.fdownloader.net/api/ajaxSearch', params=params, headers=headers, data=data).text
        resolution = response2.split('https://dl.snapcdn.app/')[1].split('720p')[0]
        resolution = resolution.split('rel=')[0]
        downloadurl =('https://dl.snapcdn.app/' + resolution).replace('\\u0022','')
        download = requests.get(downloadurl,headers=headers,stream=True)
        total_length = int(download.headers.get('content-length'))
        path = f'{namefile}.mp4'
        with open(path, 'wb') as f:
            for chunk in progress.bar(download.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
    except IndexError:
        print('URL Không Chính xác ! ')
    except requests.exceptions.ConnectionError:
        print('Mất Kết Nối Mạng ! ')
def YOUTUBE(url,namefile):
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.1.1964906593.1730647087; _ga_1KPDD5M3P8=GS1.1.1730647086.1.1.1730647114.0.0.0',
        'dnt': '1',
        'origin': 'https://vd6s.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://vd6s.com/en/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'url': url,
        'ajax': '1',
        'lang': 'en',
    }
    response = requests.post('https://vd6s.com/mates/en/analyze/ajax', headers=headers, data=data).text
    HD = response.split(",'mp4',")
    try : 
        for i in HD:
            if ",'720p'," in i:
                HD = i.split(",'720p',")[0]
                ID = response.split('  720p (.mp4) ')[1].split('Download')[0]
            elif ",'720p60'," in i:
                HD = i.split(",'720p60',")[0]
                ID = response.split('  720p60 (.mp4) ')[1].split('Download')[0]
        ID2 = ID.split("','")
        for i in range (len(ID2)):
            if str(HD) in ID2[i]:
                realid = ID2[i-1]
                formatid = ID2[i+1].split("'")[0]
        data2 = {
            'platform': 'youtube',
            'url': url,
            'title': '1',
            'id': realid,
            'ext': 'mp4',
            'note': '720p',
            'format': formatid
        }
        response2 = requests.post(
            f'https://vd6s.com/mates/en/convert?id={realid}',

            headers=headers,
            data=data2,
        ).json()
        download = requests.get(response2['downloadUrlX'],headers=headers,stream=True)
        total_length = int(download.headers.get('content-length'))
        path = f'{namefile}.mp4'
        with open(path, 'wb') as f:
            for chunk in progress.bar(download.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
    except UnboundLocalError :
        print("Video Không Hỗ Trợ Độ Phân giải HD Hoặc Video Không Khả Dụng ! ")
        return 0