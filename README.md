# fetch blog

## 项目简介

`fetch blog`是一个用于爬取并保存文章内容的Python脚本。它支持从掘金(juejin)和知乎(zhihu)等平台上爬取文章。

## 安装指南

本项目使用Python编写，要运行此脚本，您需要先确保已安装Python环境。

1. 克隆仓库到本地：

   ```
   git clone https://github.com/BrunoGao/fetch_blog.git
   ```

2. 安装依赖：

   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. 启动 web server

   ```
   python3 fetch_blog_web.py
   ```

2. 访问 web server

   ```
   http://localhost:5001/search
   ```

3. 输入标题进行搜索, 点击 "Search" 
   ![Search](https://heguang-tech-1300607181.cos.ap-shanghai.myqcloud.com/uPic/image.png)

4. 在下面的博客列表中, 选择要爬取的博客

5. 点击 "一键复制" 

6. 复制后的博客如下图:
   ![blog](https://heguang-tech-1300607181.cos.ap-shanghai.myqcloud.com/uPic/image-1.png)

## 主要流程

```mermaid
graph TD
    A[Flask App] --> B((/))
    A --> C((/search))
    A --> D((/crawl-article))
    B --> E[Render search.html]
    C --> F{Request Method}
    F -->|GET| G[Get keyword, source, sort_by, period from args]
    F -->|POST| H[Get keyword from form]
    G --> I[Search Blogs]
    H --> I
    I --> J[Remove Duplicates]
    J --> K[Filter by Period]
    K --> L[Sort Blogs]
    L --> M[Render search.html with blogs]
    D --> N{URL Parameter}
    N -->|Present| O[Run article_crawler.py]
    N -->|Missing| P[Return Error]
    O -->|Success| Q[Return Success Message]
    O -->|Failure| R[Return Failure Message]
graph TD
    A[ArticleCrawler] -->|init| B[load_config]
    A -->|start| C[send_request / send_request_d]
    A -->|parse_detail| D[fetch_author_info]
    A -->|parse_detail| E[deal_code]
    A -->|parse_detail| F[deal_images]
    A -->|parse_detail| G[write_content]
    B -->|load JSON config| H[Identify domain specific configuration]
    C -->|Fetch HTML| I[BeautifulSoup Parsing]
    D -->|Extract Author Info| J[Name, Title, URL, Image URL]
    E -->|Format Code Blocks| K[Replace with Markdown]
    F -->|Upload and Replace Images| L[Replace with Markdown Image Tags]
    G -->|Generate HTML and Markdown Files| M[HTML and Markdown Outputs]
    I --> D
    I --> E
    I --> F
    I --> G
    J -.->|Used in| G
    K -.->|Included in| G
    L -.->|Included in| G
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style B fill:#bbf,stroke:#f66,stroke-width:2px
    style C fill:#bbf,stroke:#f66,stroke-width:2px
    style D fill:#bbf,stroke:#f66,stroke-width:2px
    style E fill:#bbf,stroke:#f66,stroke-width:2px
    style F fill:#bbf,stroke:#f66,stroke-width:2px
    style G fill:#bbf,stroke:#f66,stroke-width:2px
    style H fill:#bbf,stroke:#f66,stroke-width:2px
    style I fill:#bbf,stroke:#f66,stroke-width:2px
    style J fill:#bbf,stroke:#f66,stroke-width:2px
    style K fill:#bbf,stroke:#f66,stroke-width:2px
    style L fill:#bbf,stroke:#f66,stroke-width:2px
    style M fill:#bbf,stroke:#f66,stroke-width:2px
```

## 功能特性

- 支持从掘金,知乎,csdn和简书平台爬取文章。
- web 界面搜索, 掘金风格
- 代码自动识别并高亮
- 图片自动转存到自己的图床