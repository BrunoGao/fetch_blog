from flask import Flask, request, render_template
from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import subprocess
from upload_picture import PictureUploader

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    source = request.form.get('source', 'all')  # Default to 'all' if source is not provided
    print("source: " + source)

    blogs = []
    if source in ['all', 'juejin']:
        blogs.extend(search_juejin(keyword))
        base_url = "https://juejin.cn"
    if source in ['all', 'csdn']:
        blogs.extend(search_csdn(keyword))
        base_url = "https://blog.csdn.net"

    # Optionally, sort or process blogs list as needed

    # Remove duplicates based on title and brief
    unique_blogs = []
    seen = set()
    for blog in blogs:
        title_brief_tuple = (blog['title'], blog['brief'])
        if title_brief_tuple not in seen:
            unique_blogs.append(blog)
            seen.add(title_brief_tuple)
    blogs = unique_blogs
    
  
    #blogs.sort(key=custom_sort)
    blogs.sort(key=lambda blog: blog['last_modify'], reverse=False)

    return render_template('search.html', blogs=blogs, search_query=keyword, source=source, base_url=base_url)
def custom_sort(blog):
        return blog['last_modify'] * 0.6 + (-int(blog['digg_count'])) * 0.4
# 定义过滤器
def days_since(timestamp):  
    if timestamp.find("-") != -1:
        print("timestamp:str:: " + str(timestamp))
        mtime_datetime = datetime.strptime(timestamp, "%Y-%m-%d")
    else:
        print("timestamp:int:: " + str(timestamp))
        mtime_datetime = datetime.utcfromtimestamp(int(timestamp))
  
    now_datetime = datetime.utcnow()
    difference = now_datetime - mtime_datetime
    return difference.days
# 注册过滤器
app.jinja_env.filters['days_since'] = days_since

# 定义过滤器
def changeImageUrl(url):
    uploader = PictureUploader(config_path='uploader_config.ini')
    url = uploader.upload_picture(pic_url=url.split("#")[0]) if (url.startswith("http")) else url
    return url
# 注册过滤器
app.jinja_env.filters['changeImageUrl'] = changeImageUrl

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
                    #processed_cover_image_url = changeImageUrl(cover_image_url)
                    # Appending article details to blogs list
                    blogs.append({
                        'title': article_info['title'],
                        'url': base_url + "/post/" + article_info['article_id'],
                        'brief': article_info['brief_content'],
                        'user_id': base_url + "/user/" +author_info['user_id'],
                        'user_name':  author_info['user_name'],
                        'last_modify': days_since(article_info['mtime']),
                        'tags': article_tags,
                        'digg_count': article_info['digg_count'],
                        'base_name': base_name,
                        'base_url': base_url,
                        'imgUrl': cover_image_url
                    })
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
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