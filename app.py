from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/crawl', methods=['POST'])
def crawl_article():
    data = request.json
    url = data.get('url')
    output_dir = data.get('output_dir', './blog')  # 默认输出目录为./data
    if url:
        # 构建命令行命令
        command = f"python article_crawler.py -u {url} -o {output_dir}"
        try:
            # 调用subprocess运行脚本
            subprocess.run(command, check=True, shell=True)
            return jsonify({"message": "Crawling successful", "url": url, "output_dir": output_dir}), 200
        except subprocess.CalledProcessError as e:
            return jsonify({"error": "Crawling failed", "message": str(e)}), 500
    else:
        return jsonify({"error": "URL is required"}), 400

if __name__ == '__main__':
    app.run(debug=True)