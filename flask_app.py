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
    blogs = search_juejin(keyword)
    # 这里可以添加其他网站的搜索结果，并进行去重和排序
    return render_template('search.html', blogs=blogs)

# 定义过滤器
def days_since(timestamp):
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
    
    url = uploader.upload_picture(url) if url.startswith("http") else url
    return url
# 注册过滤器
app.jinja_env.filters['changeImageUrl'] = changeImageUrl


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
                # Extracting necessary details from each article
                article_info = result['result_model']['article_info']
                author_info = result['result_model']['author_user_info']
                tags = result['result_model'].get('tags', [])
                # Preparing tags list
                article_tags = [{'tag_name': tag['tag_name']} for tag in tags]
                # Processing cover_image with changeImageUrl
                cover_image_url = article_info.get('cover_image', '')
                processed_cover_image_url = changeImageUrl(cover_image_url)
                # Appending article details to blogs list
                blogs.append({
                    'title': article_info['title'],
                    'url': base_url + "/post/" + article_info['article_id'],
                    'brief': article_info['brief_content'],
                    'user_id': author_info['user_id'],
                    'user_name': base_url + author_info['user_name'],
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