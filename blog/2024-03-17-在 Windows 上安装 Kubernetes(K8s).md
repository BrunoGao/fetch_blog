---
title: "在 Windows 上安装 Kubernetes(K8s)"
publishdate: 2024-03-17
authors: 
  name: "魔法编码者X"
  title: "此处留白"
  url: "https://juejin.cn/user/4213779362220253/posts"
  image_url: "https://p6-passport.byteacctimg.com/img/user-avatar/40e392f5f85f559ee7ac91cbfc400be2~200x200.awebp"
tags: ["Kubernetes"]
summary: >-
  Your summary here
---
 由于 Docker Desktop 自带 Kubernetes 选项，对于新手来说安装 Kubernetes 省心不少。 在安装过程中容易出问题的地方是 Windows 版本不满足最低要求，比如 Windows 10 家庭版很可能安装 Docker Desktop 不成功，对于系统是 Win7/Win8/Win10 家庭版的用户可尝试通过 Docker Toolbox 安装 Docker Desktop。 

##  安装 WSL2/Hyper-V 

对于不同的 Windows 版本，需要安装 WSL2 或者 Hyper-V。请结合实际的 Windows 版本，搜索对应的教程安装 WSL2 或者 Hyper-V，比如可以参考以下教程： 

  * [ Windows Docker Desktop 安装 ](https://link.juejin.cn?target=https%3A%2F%2Fblog.csdn.net%2FB11050729%2Farticle%2Fdetails%2F132002572 "https://blog.csdn.net/B11050729/article/details/132002572")
  * [ docs.docker.com/desktop/tro… ](https://link.juejin.cn?target=https%3A%2F%2Fdocs.docker.com%2Fdesktop%2Ftroubleshoot%2Ftopics%2F%23virtualization "https://docs.docker.com/desktop/troubleshoot/topics/#virtualization")



##  下载 Docker Desktop for windows 

可以通过点击 [ 链接 ](https://link.juejin.cn?target=https%3A%2F%2Fdocs.docker.com%2Fdesktop%2Finstall%2Fwindows-install%2F "https://docs.docker.com/desktop/install/windows-install/") 进入 Docker 官方安装指南页面下载安装包。 

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/5d7aaa8732334b3ca21309cdb0de1248~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

##  安装 Docker Desktop 

双击下载完成的 "Docker Desktop Installer.exe" 去安装 Docker Desktop。 

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/64c1166f680f4f43ba0680ac26406ba0~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

备注：如果在安装确认中提示 "Use WSL 2 instead of Hyper-V" 选项， 请根据步骤 "安装 WSL2/Hyper-V" 使用的方式选择。 

##  安装 Kubernetes 

勾上 "Enable Kubernetes" 然后点击 "Apply & restart" 安装 Kubernetes。 

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/dba5df15efeb44e0b2d0993a1904edd2~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

##  部署 Kubernetes 仪表盘 

默认情况下不会部署 Dashboard，可以通过以下命令部署。 
    
    
    ```bash
    kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
    
    ```

如果上述命令执行出错，可以在浏览器打开网址 [ recommended.yaml ](https://link.juejin.cn?target=https%3A%2F%2Fraw.githubusercontent.com%2Fkubernetes%2Fdashboard%2Fv2.7.0%2Faio%2Fdeploy%2Frecommended.yaml "https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml") 并另存到本地，然后执行以下命令。 
    
    
    ```plaintext
    kubectl apply -f 替换成实际的文件路径
    
    ```

##  创建示例用户 

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/7e77d783c96344f39629113d6bf1c7a7~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

新建文件保存下方创建 ServiceAccount 的内容，假设该文件的名称是 dashboard-service-account-adminuser.yaml。 
    
    
    ```yaml
    apiVersion: v1
    kind: ServiceAccount
    metadata:
      name: admin-user
      namespace: kubernetes-dashboard
    
    ```

执行以下命令生效上述 dashboard-service-account-adminuser.yaml 配置。 
    
    
    ```plaintext
    kubectl apply -f dashboard-service-account-adminuser.yaml
    
    ```

新建文件保存下方创建 ClusterRoleBinding 的内容，假设该文件的名称是 dashboard-cluster-role-binging-adminuser.yaml。 
    
    
    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: admin-user
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: cluster-admin
    subjects:
    - kind: ServiceAccount
      name: admin-user
      namespace: kubernetes-dashboard
    
    ```

执行以下命令生效上述 dashboard-cluster-role-binging-adminuser.yaml 配置。 
    
    
    ```plaintext
    kubectl apply -f dashboard-cluster-role-binging-adminuser.yaml
    
    ```

新建文件保存下方创建 Secret 的内容，假设该文件的名称是 dashboard-secret-adminuser.yaml。(用于获取长期访问令牌 long-lived Bearer Token) 
    
    
    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: admin-user
      namespace: kubernetes-dashboard
      annotations:
        kubernetes.io/service-account.name: "admin-user"   
    type: kubernetes.io/service-account-token  
    
    ```

执行以下命令生效上述 dashboard-secret-adminuser.yaml 配置。 
    
    
    ```plaintext
    kubectl apply -f dashboard-secret-adminuser.yaml
    
    ```

##  启用 Kubernetes 仪表盘 

执行以下命令启用 Dashboard。 
    
    
    ```plaintext
    kubectl proxy
    
    ```

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/b8847a064c2e458ba8a9385f43a434e1~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

##  访问 Kubernetes 仪表盘 

点击 [ http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/ ](https://link.juejin.cn?target=http%3A%2F%2Flocalhost%3A8001%2Fapi%2Fv1%2Fnamespaces%2Fkubernetes-dashboard%2Fservices%2Fhttps%3Akubernetes-dashboard%3A%2Fproxy%2F "http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/") 打开仪表盘。 

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/6ba614e76e6e41c2878fdf0547b943dd~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

可以通过以下命令获取 Token。 
    
    
    ```sql
    kubectl -n kubernetes-dashboard create token admin-user
    
    ```

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/ae44b7b95deb4bd2ab98a43dcb274ca9~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

或者通过以下命令获取长期访问 token。(以下命令在 PowerShell 下执行可能会出错，可使用 Git Bash 执行) 
    
    
    ```ini
    kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
    
    ```

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/891d6a2aa2a64fe6a00ad77ee236d188~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

通过上述获取的 token 登录进入仪表盘。 

![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/13b26886e87f477aa2eddb0228bc4320~tplv-k3u1fbpfcp-jj-mark:3024:0:0:0:q75.awebp) 

##  参考资料 

  * Docker 官方安装指南 [ Install Docker Desktop on Windows | Docker Docs ](https://link.juejin.cn?target=https%3A%2F%2Fdocs.docker.com%2Fdesktop%2Finstall%2Fwindows-install%2F "https://docs.docker.com/desktop/install/windows-install/")
  * Kubernetes 官方文档 [ 部署和访问 Kubernetes 仪表板（Dashboard） | Kubernetes ](https://link.juejin.cn?target=https%3A%2F%2Fkubernetes.io%2Fzh-cn%2Fdocs%2Ftasks%2Faccess-application-cluster%2Fweb-ui-dashboard%2F "https://kubernetes.io/zh-cn/docs/tasks/access-application-cluster/web-ui-dashboard/")
  * 微软官方文档 [ Install WSL | Microsoft Learn ](https://link.juejin.cn?target=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fwindows%2Fwsl%2Finstall "https://learn.microsoft.com/en-us/windows/wsl/install")



:::tip 版权说明
本文由程序自动从互联网获取，如有侵权请联系删除，版权属于原作者。

作者：魔法编码者X

链接：https://juejin.cn/post/7346959888009035810?searchId%3D20240401181139ED938895D9504232BCC1
::: 
