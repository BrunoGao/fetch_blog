from flask import Flask, request, render_template
from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import subprocess
from upload_picture import PictureUploader
import hashlib
import shelve
import requests
import os




app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
    else:  # For GET requests
        keyword = request.args.get('keyword', '')

    source = request.args.get('source', 'all')  # Default to 'all' if source is not provided
    sort_by = request.args.get('sort_by', 'custom')  # Default to 'custom' sort
    period = request.args.get('period', '0')  # Default to '0' if period is not provided
    print("source: " + source)

    blogs = []
    if source in ['all', 'juejin']:
        blogs.extend(search_juejin(keyword))
        base_url = "https://juejin.cn"
    if source in ['all', 'csdn']:
        blogs.extend(search_csdn(keyword))
        base_url = "https://blog.csdn.net"
    #if source in ['all', 'zhihu']:
        #blogs.extend(search_zhihu(keyword))
        #base_url = "https://www.zhihu.com"

# Remove duplicates based on title and brief
    unique_blogs = []
    seen = set()
    for blog in blogs:       
        title_brief_tuple = (blog['title'], blog['brief'])
        if title_brief_tuple not in seen:
            unique_blogs.append(blog)
            seen.add(title_brief_tuple)
    blogs = unique_blogs
    
    # Filter blogs based on period
    if period != '0':
        if period == '1':  # 最近一天
            time_threshold = 1
        elif period == '2':  # 最近一周
            time_threshold = 7
        elif period == '3':  # 最近三月
            time_threshold = 90
        else:
            time_threshold = float('inf')  # 如果没有匹配的期间，我们不过滤任何博客

        blogs = [blog for blog in blogs if int(blog['last_modify']) == 0 or int(blog['last_modify']) <= time_threshold]


    # Sorting logic based on sort_by parameter
    if sort_by == 'latest':
        blogs.sort(key=lambda blog: blog['last_modify'], reverse=False)
    elif sort_by == 'hottest':
        blogs.sort(key=lambda blog: int(blog['digg_count']), reverse=True)
    else:  # Default to custom sort
        blogs.sort(key=custom_sort)
    
    return render_template('search.html', blogs=blogs, search_query=keyword, source=source, base_url=base_url)


def custom_sort(blog):
        # Assuming last_modify is smaller (closer to 0), the article is newer
        # digg_count larger, the article is more popular
        # The weights can be adjusted according to actual situations
        return int(blog['last_modify']) * 0.6 + (-int(blog['digg_count'])) * 0.4
# 定义过滤器
def days_since(timestamp):  
    if timestamp.find("-") != -1:
        #print("timestamp:str:: " + str(timestamp))
        mtime_datetime = datetime.strptime(timestamp, "%Y-%m-%d")
    else:
        #print("timestamp:int:: " + str(timestamp))
        mtime_datetime = datetime.utcfromtimestamp(int(timestamp))
  
    now_datetime = datetime.utcnow()
    difference = now_datetime - mtime_datetime
    return difference.days
# 注册过滤器
app.jinja_env.filters['days_since'] = days_since

# 定义过滤器
def changeImageUrl(url):
    # 计算 URL 的 hash 值作为文件名，以避免重复下载
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    # 定义图片存储的本地路径
    local_image_path = f'static/images/{url_hash}.jpg'

    # 检查图片是否已经下载
    if not os.path.exists(local_image_path):
        # 图片尚未下载，执行下载
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(local_image_path, 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
        except Exception as e:
            print(f"Failed to download image from {url}. Error: {e}")
            return url  # 如果下载失败，返回原URL

    # 返回本地服务器上的图片URL
    return f'/{local_image_path}'


def search_csdn(keyword):
    base_url = "https://blog.csdn.net"
    base_name = "CSDN"
    url = f"https://so.csdn.net/api/v3/search?q={keyword}&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&ct=-1&pnt=-1&ry=-1&ss=-1&dct=-1&vco=-1&cc=-1&sc=-1&akt=-1&art=-1&ca=-1&prs=&pre=&ecc=-1&ebc=-1&urw=&ia=1&dId=&cl=-1&scl=-1&tcl=-1&platform=pc&ab_test_code_overlap=&ab_test_random_code="
    print("url: " + url)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    blogs = []  # Initialize blogs list
    if response.status_code == 200:
        data = response.json()
        for item in [item for item in data.get('result_vos', []) if item.get("type") == "blog"]:
            try:
    
                blogs.append({
                    'title': item.get('title'),
                    'brief':  item.get('description'),
                    'user_id': base_url + "/" + item.get('author'),
                    'user_name': item.get('nickname'),
                    'digg_count': item.get('view_num'),
                    'url': item.get('url_location'),
                    'tags': [{'tag_name': tag} for tag in item.get('search_tag')] if item.get('search_tag') else [],
                    'last_modify': days_since(item.get('create_time_str')),
                    'base_name': base_name,
                    'base_url': base_url
                })
            except ValueError:  # includes simplejson.decoder.JSONDecodeError
                print('Decoding JSON has failed')
    else:
        print(f"Failed to fetch data: {response.status_code}")
    return blogs

def search_juejin(keyword):
    base_url = "https://juejin.cn"
    base_name = "稀土掘金"
    url = f'https://api.juejin.cn/search_api/v1/search?aid=2608&uuid=7307518557755196954&spider=0&query={keyword}&id_type=0&cursor=0&limit=20&search_type=0&sort_type=0&version=1'
    print("url: " + url)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    blogs = []  # Initialize blogs list
    if response.status_code == 200:
        try:
            results = response.json()['data']
            for result in results:
                if result["result_type"] == 2:
                   # Extracting necessary details from each article
                   article_info = result['result_model']['article_info']
                   author_info = result['result_model']['author_user_info']
                   tags = result['result_model'].get('tags', [])
                   # Preparing tags list
                   article_tags = [{'tag_name': tag['tag_name']} for tag in tags]
                   
                   # Processing cover_image with changeImageUrl
                   cover_image_url = article_info.get('cover_image', '')
                   #print("cover_image_url: " + str(cover_image_url))
                   processed_cover_image_url = changeImageUrl(cover_image_url) if cover_image_url else ''
                   #print("processed_cover_image_url: " + str(processed_cover_image_url))
                   # Appending article details to blogs list
                   brief = result['content_highlight']
                   title = result['title_highlight']
                   blogs.append({
                       'title': title,
                       'url': base_url + "/post/" + article_info['article_id'],
                       'brief': brief,
                       'user_id': base_url + "/user/" +author_info['user_id'],
                       'user_name':  author_info['user_name'],
                       'last_modify': days_since(article_info['mtime']),
                       'tags': article_tags,
                       'digg_count': article_info['digg_count'],
                       'base_name': base_name,
                       'base_url': base_url,
                       'imgUrl': processed_cover_image_url
                   })
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
    else:
        print(f"Failed to fetch data: {response.status_code}")
    return blogs

def search_zhihu(keyword):
    base_url = "https://www.zhihu.com"
    base_name = "知乎"
    url = f"https://api.zhihu.com/search?query={keyword}"
    print("url: " + url)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    blogs = []  # 初始化博客列表
    if response.status_code == 200:
        data = response.json()
        for item in data['data']:
            if item["object"]['type'].equals("article"):
                title = item['highlight']['title']
                description = item['highlight']['description']
                answer_url = item['object']['url']
                first_image_url = item['object']['thumbnail_info']['thumbnails'][0]['url'] if item['object']['thumbnail_info']['thumbnails'] else None
                url_token = item['object']['author']['url_token']
                user_name = item['object']['author']['name']
                blogs.append({
                    'title': title,
                    'brief': description,
                    'user_id': base_url + "/people/" + url_token,
                    'user_name':  user_name,
                    'url': answer_url,
                    'imgUrl': first_image_url,
                    'base_name': base_name,
                    'base_url': base_url,
                    'digg_count': item['object']['comment_count'],
                    'tags': [],
                    'last_modify': item['object']['updated_time']
                })
    else:
        print(f"Failed to fetch data: {response.status_code}")
    return blogs

@app.route('/crawl-article')
def crawl_article():
    article_url = request.args.get('url')
    print("crawl_article:" + article_url)
    if article_url:
        # 调用Python脚本
        command = f'python3 article_crawler.py -u "{article_url}" -o blog'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return jsonify({'message': 'Crawl successful'}), 200
        else:
            return jsonify({'error': 'Crawl failed', 'details': stderr.decode()}), 500
    else:
        return jsonify({'error': 'Missing URL parameter'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)