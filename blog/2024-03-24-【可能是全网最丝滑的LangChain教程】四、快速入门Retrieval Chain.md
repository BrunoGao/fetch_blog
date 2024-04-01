---
title: "【可能是全网最丝滑的LangChain教程】四、快速入门Retrieval Chain"
publishdate: 2024-03-24
authors: 
  name: "Jeffray"
  title: "此处留白"
  url: "https://juejin.cn/user/3184633759669848/posts"
  image_url: "https://p3-passport.byteacctimg.com/img/mosaic-legacy/3795/3047680722~200x200.image"
tags: ["人工智能", "ChatGPT", "AIGC"]
summary: >-
  Your summary here
---
 ##  系列文章地址 

[ 【可能是全网最丝滑的LangChain教程】一、LangChain介绍 - 掘金 (juejin.cn) ](https://juejin.cn/post/7341300805282103322 "https://juejin.cn/post/7341300805282103322")

[ 【可能是全网最丝滑的LangChain教程】二、LangChain安装 - 掘金 (juejin.cn) ](https://juejin.cn/post/7344089411984408602 "https://juejin.cn/post/7344089411984408602")

[ 【可能是全网最丝滑的LangChain教程】三、快速入门LLMChain - 掘金 (juejin.cn) ](https://juejin.cn/post/7346519210725179426 "https://juejin.cn/post/7346519210725179426")

##  使用LangChain构建应用 

LangChain支持构建应用程序，将外部数据源和计算源连接到LLM。我们将从一个简单的 LLM 链开始，它只依赖于提示模板中的信息来响应。 接下来，我们将构建一个检索链，该链从单独的数据库获取数据并将其传递到提示模板中。 然后，我们将添加聊天记录，以创建对话检索链。这允许您以聊天方式与此 LLM 进行交互，因此它会记住以前的问题。 最后，我们将构建一个代理，利用 LLM 来确定它是否需要获取数据来回答问题。 

##  Retrieval Chain 

###  1 问一个LLM不知道的问题 

"数据空间研究院是谁出资建立的？" 
    
    
    ```python
    from langchain_openai import ChatOpenAI 
    llm = ChatOpenAI(openai_api_key="...")
    llm.invoke("数据空间研究院是谁出资建立的？")
    
    ```

因为LLM没有学习郭过相关的知识，所以输出的结果不是我们想要的，如下 
    
    
    ```python
    AIMessage(content='抱歉，我不确定数据空间研究院是谁出资建立的。 ')
    
    ```

###  2 怎么让LLM正确回答它没学习过的相关知识的问题？ 

为了正确回答最初的问题（“数据空间研究院是谁出资建立的？”），我们需要为 LLM 提供额外的上下文。 我们可以通过_检索_来做到这一点。 当您有 **太多数据** 无法直接传递给 LLM 时，检索非常有用。 然后，您可以使用检索器仅获取最相关的部分并将其传递。 

在此过程中，我们将从 _Retriever_ 中查找相关文档，然后将它们传递到提示符中。 Retriever 可以由任何东西支持——SQL 表、互联网、文档等——但在这种情况下，我们将填充一个向量存储并将其用作检索器。 

####  2.1 创建用于将文档列表传递给模型的链 

首先，让我们设置一个链，该链接受一个问题和检索到的文档并生成一个答案。 
    
    
    ```python
    from langchain.chains.combine_documents import create_stuff_documents_chain 
    prompt = ChatPromptTemplate.from_template("""仅根据提供的上下文回答以下问题:
    
    <上下文>
    {context}
    
    
    问题: {input}""") 
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    ```

####  2.2 传入文档信息 

这里传入文档信息可以选择手动传入，也可以选择从指定文档（网页、PDF、文档等等）加载。 

#####  2.2.1 手动传入文档信息 
    
    
    ```python
    from langchain_core.documents import Document 
    
    document_chain.invoke({    
        "input": "数据空间研究院是谁出资建立的？",    
        "context": [Document(page_content="合肥综合性国家科学中心数据空间研究院是由安徽省人民政府发起成立的事业单位，是新一代信息技术数据空间领域的大型新型研发机构，致力于引领网络空间安全和数据要素创新技术前沿和创新方向，凝聚一批海内外领军科学家团队，汇聚相关行业大数据，开展数据空间基础理论、体系架构、关键技术研究以及相关能力建设，打造大数据发展新高地，推进“数字江淮”建设，为数字中国建设贡献“安徽智慧”“合肥智慧”。")]
    })
    
    ```

输出： 
    
    
    ```bash
    安徽省人民政府
    
    ```

#####  2.2.2 从网页加载 

首先，我们需要加载要索引的数据。因为我需要从网页（百度百科）获取数据，为此，我们将使用 WebBaseLoader。这需要安装 [ BeautifulSoup ](https://link.juejin.cn?target=https%3A%2F%2Fbeautiful-soup-4.readthedocs.io%2Fen%2Flatest%2F "https://beautiful-soup-4.readthedocs.io/en/latest/") ： 
    
    
    ```bash
    pip install beautifulsoup4
    
    ```

之后，我们可以导入和使用 WebBaseLoader。 
    
    
    ```python
    from langchain_community.document_loaders import WebBaseLoader
    
    loader = WebBaseLoader("https://baike.baidu.com/item/%E5%90%88%E8%82%A5%E7%BB%BC%E5%90%88%E6%80%A7%E5%9B%BD%E5%AE%B6%E7%A7%91%E5%AD%A6%E4%B8%AD%E5%BF%83%E6%95%B0%E6%8D%AE%E7%A9%BA%E9%97%B4%E7%A0%94%E7%A9%B6%E9%99%A2/62996254?fr=ge_ala") 
    docs = loader.load()
    
    ```

接下来，我们需要将其索引到向量存储中。这需要一些组件，即 [ 嵌入模型 ](https://link.juejin.cn?target=https%3A%2F%2Fpython.langchain.com%2Fdocs%2Fmodules%2Fdata_connection%2Ftext_embedding "https://python.langchain.com/docs/modules/data_connection/text_embedding") 和 [ 向量存储 ](https://link.juejin.cn?target=https%3A%2F%2Fpython.langchain.com%2Fdocs%2Fmodules%2Fdata_connection%2Fvectorstores "https://python.langchain.com/docs/modules/data_connection/vectorstores") 。 

对于嵌入模型，这里使用目前比较热门的 [ m3e-base ](https://link.juejin.cn?target=https%3A%2F%2Fhuggingface.co%2Fmoka-ai%2Fm3e-base "https://huggingface.co/moka-ai/m3e-base") 。m3e-base使用时需要指定加载路径，可以是本地或者在线（在线的本质也是先下载后加载），这里我已经提前下载好了。 
    
    
    ```python
    from langchain.embeddings.huggingface import HuggingFaceEmbeddings
    import torch 
    
    EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    embeddings = HuggingFaceEmbeddings(model_name='D:\models\m3e-base',model_kwargs={'device': EMBEDDING_DEVICE})
    
    ```

现在，我们可以使用此嵌入模型将文档摄取到矢量存储中。 为了简单起见，我们将使用一个简单的本地向量存储 [ FAISS ](https://link.juejin.cn?target=https%3A%2F%2Fpython.langchain.com%2Fdocs%2Fintegrations%2Fvectorstores%2Ffaiss "https://python.langchain.com/docs/integrations/vectorstores/faiss") 。 

首先，我们需要为此安装所需的软件包。如果机器有显卡，选择下载完整的faiss，我这里用faiss-cpu，因为我电脑没显卡。 
    
    
    ```bash
    pip install faiss-cpu
    
    ```

然后我们可以建立我们的索引： 
    
    
    ```python
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter  
    
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    vector = FAISS.from_documents(documents, embeddings)
    
    ```

现在，我们已经在向量存储中索引了这些数据，我们将创建一个检索链。 该链将接受一个传入的问题，查找相关文档，然后将这些文档与原始问题一起传递到 LLM 中，并要求它回答原始问题。 

使用从网页获取的数据信息： 
    
    
    ```python
    from langchain.chains import create_retrieval_chain 
    
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    response = retrieval_chain.invoke({"input": "数据空间研究院是谁出资创建的？"})
    print(response["answer"])
    
    ```

这里输出的结果是： 
    
    
    ```python
    合肥综合性国家科学中心数据空间研究院是由安徽省人民政府发起成立的。
    
    ```

##  总结 

我们现在已经成功地建立了一个基本的检索链。我们只触及了检索的基础知识，Retrieval Chain还有更多的用法，包括嵌入模型的选择（不同模型的效果有差异，进而影响最终输出结果的准确性）、文档加载器的选择（你的文档是什么格式？来自本地还是网页？视频还是文本？）、文档怎么检索（MapReduce、MapRerank、Reduce、Refine、Stuff）等等等等。具体怎么使用，请关注后续文章更新。 

Peace Guys~ 

:::tip 版权说明
本文由程序自动从互联网获取，如有侵权请联系删除，版权属于原作者。

作者：Jeffray

链接：https://juejin.cn/post/7349107210658758692
::: 
