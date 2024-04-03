# article_crawler

## 项目简介
`article_crawler`是一个用于爬取并保存文章内容的Python脚本。它支持从掘金(juejin)和知乎(zhihu)等平台上爬取文章。

## 安装指南
本项目使用Python编写，要运行此脚本，您需要先确保已安装Python环境。

1. 克隆仓库到本地：
   ```
   git clone https://github.com/your-repository/article_crawler.git
   ```
2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 使用方法

python article_crawler.py -u <文章URL> -o <输出目录>

示例：
python article_crawler.py -u https://www.jianshu.com/p/609878670 -o ./data

```mermaid
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
- 简单易用，通过命令行参数控制
- 代码自动识别并高亮
- 图片自动转存到自己的图床

