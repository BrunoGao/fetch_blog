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
    return render_template('search.html', data=blogs)

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
    # 示例：调用掘金搜索API（请替换为实际可用的API）
    url = f'https://api.juejin.cn/search_api/v1/search?aid=2608&uuid=7307518557755196954&spider=0&query={keyword}&id_type=0&cursor=0&limit=20&search_type=0&sort_type=0&version=1'
    print("url: " + url)
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    #print( response.json())
    if response.status_code == 200:
        try:
            results = response.json()['data']
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
            results = []
    else:
        print(f"Failed to fetch data: {response.status_code}")
        results = []
    #print("results: " + str(results))
    #blogs = [{'title': result['title'], 'url': result['link_url'], 'summary': result['brief_content']} for result in results]
    return results
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