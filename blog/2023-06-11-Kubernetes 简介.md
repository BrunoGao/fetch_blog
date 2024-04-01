---
title: "Kubernetes 简介"
publishdate: 2023-06-11
authors: 
  name: "wzl"
  title: "Java"
  url: "https://juejin.cn/user/1917157487938744/posts"
  image_url: "https://p3-passport.byteacctimg.com/img/user-avatar/ba5bc0b96c2cb02919c07faaba8fdb14~200x200.image"
tags: ["Kubernetes"]
summary: >-
  Your summary here
---
 也称为 K8s，是用于自动部署、扩缩和管理容器化应用程序的开源系统。将组成应用程序的容器组成逻辑单元，以便管理和服务发现。 

#  Kubernetes 和 Docker 

Kubernetes 和 Docker 是两个互补的技术。⽐如，通常⼈们会使⽤ Docker 进⾏应⽤的开发，然后⽤Kubernetes 在⽣产环境中对应⽤进⾏编排。 

在这样的模式中，开发者使⽤⾃⼰喜欢的语⾔编写代码，然后⽤ Docker 进⾏打包、测试和交付。但是最终在测试环境或⽣产环境中运⾏的过程是由 Kubernetes 来完成的。 

从运⾏架构上来说，假设在某⽣产环境中的 Kubernetes 集群是由 10 个节点构成的。那么其中的每个节点都是以Docker 作为其容器运⾏时 （Container Runtime）。也就是说，Docker 是⼀种更加偏向底层的技 术，它负责诸如启停容器的操作；⽽ Kubernetes 是⼀种更加偏向上层的技术，它注重集群范畴的管理，⽐如决定在哪个节点上运⾏容器、决定什么适合进⾏扩缩容或升级。 

![](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/cafd886d65f546dcbd29ecc1c67e2c02~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp) 

Docker 并⾮ Kubernetes 唯⼀⽀持的容器运⾏时。事实上，Kubernetes 基于⼀系列特性实现了对容器运⾏时的抽象（从⽽可以兼容不同的底层容器运⾏时）。 

Docker 并⾮ Kubernetes 唯⼀⽀持的容器运⾏时。事实上，Kubernetes 基于⼀系列特性实现了对容器运⾏时的抽象（从⽽可以兼容不同的底层容器运⾏时）。 

  1. 容器运⾏时接⼝（Container Runtime Interface, CRI）是 Kubernetes ⽤来与第三⽅容器运⾏时进⾏对接的标准化的抽象层。这 样容器运⾏时与 Kubernetes 是解耦的，同时⼜能够以⼀种标准化的⽅ 式予以⽀持。 
  2. 运⾏时类（Runtime Class）是Kubernetes 1.12引⼊的新特性， 并在 1.14 版中升级为 beta。它对不同的运⾏时进⾏了归类。例如： gVisor 或 Kata 容器运⾏时或许⽐ Docker 和 Containerd 能提供更优的隔离性。 



⽬前，Containerd 已经赶超 Docker 成为 Kubernetes 中最普遍使⽤的容 器运⾏时。它实际上是 Docker 的精简版本，只保留了 Kubernetes 需要 的部分。 

虽有提及，不过这些底层技术不会影响到 Kubernetes 的学习体验。⽆论使⽤哪种容器运⾏时，Kubernetes 层⾯的操作（命令等）都是⼀样的。 

#  Kubernetes 架构简介 

![](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/c4deb5bbeb8a422289e6445468e73a83~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp) 

##  主节点（控制面板） 

⼀个 Kubernetes 集群由主节点（master）与⼯作节点（node）组成。 这些节点都是 Linux 主机，可以运⾏在虚拟机（VM）、数据中⼼的物理 机，或者公有云/私有云的实例上。 

Kubernetes 的主节点（master）是组成集群的控制平⾯的系统服务的 集合。 Kubernetes 架构图 主节点（控制平⾯） 

⼀种最简单的⽅式是将所有的主节点服务（Service）运⾏在同⼀个主 机上。但是这种⽅式只适⽤于实验或测试环境。在⽣产环境上，主节点 的⾼可⽤部署是必需的。这也是为什么主流的云服务提供商都实现了⾃ ⼰的多主节点⾼可⽤性（Multi-master High Availability），并将其作 为⾃身 Kubernetes 平台的⼀部分，⽐如 Azure Kubernetes Service （AKS）、AWS Elastic Kubernetes Service（EKS）以及Google Kubernetes Engine（GKE）。 ⼀般来说，建议使⽤ 3 或 5 个副本来完成⼀个主节点⾼可⽤性部署⽅案。 

###  API Server 

API Server（API 服务）是 Kubernetes 的中央⻋站。所有组件之间的通 信，都需要通过 API Server 来完成。 

API Server 对外通过HTTPS的⽅式提供了 RESTful ⻛格的 API 接⼝，读者上传 YAML 配置⽂件也是通过这种接口实现的。这些YAML⽂件有时 也被称作 manifest ⽂件，它们描述了⽤户希望应⽤在运⾏时达到的期望 状态（desired state）。期望状态中包含但不限于如下内容：需要使⽤的容器镜像、希望对外提供的端⼝号，以及希望运⾏的 Pod 副本数量。 

访问 API Server 的全部请求都必须经过授权与认证，⼀旦通过之后， YAML ⽂件配置就会被认为是有效的，并被持久化到集群的存储中，最 后部署到整个集群。 

###  Controller Manager 

controler manager 负责需要判断做什么 

controller 管理器实现了全部的后台控制循环，完成对集群的监控并对事件作出响应。 

controller 管理器是 controller 的管理者（controller of controller），负责创建 controller，并监控它们的执⾏。 ⼀些控制循环包括：⼯作节点 controller、终端 controller，以及副本 controller。 

对应的每个 controller 都在后台启动了独⽴的循环监听功 能，负责监控 API Server 的变更。这样做的⽬的是保证集群的当前状态（current state）可以与期望状态（desired state）相匹配。 

每个控制循环实现上述功能的基础逻辑⼤致如下。 

  1. 获取期望状态。 
  2. 观察当前状态。 
  3. 判断两者间的差异。 
  4. 变更当前状态来消除差异点。 



上⾯的逻辑是 Kubernetes 与声明式设计模式的关键所在。 每个控制循环都极其定制化，并且仅关⼼ Kubernetes 集群中与其相关 的部分。感知系统的其他部分并调⽤这种复杂的事情我们是绝对不会尝 试的，每个控制循环都只关⼼与⾃⼰相关的逻辑，剩下的部分会交给其 他控制循环来处理。这就是如 Kubernetes 这样的分布式系统设计的关 键点所在，也与 UNIX设 计哲学不谋⽽合：每个组件都专注做好⼀件事，复杂系统是通过多个专⼀职责的组件组合⽽构成的。 

###  Scheduler 

scheduler 负责怎么做，这些容器要放在哪些服务器上。 

调度器的职责就是通过监听 API Server 来启动新的⼯作 任务，并将其分配到适合的且处于正常运⾏状态的节中。为了完成这样的⼯作，调度器实现了复杂的逻辑，过滤掉不能运⾏指定任务的⼯作节点，并对过滤后的节点进⾏排序。排序系统⾮常复杂，在排序之后会选择分数最⾼的节点来运⾏指定的任务。 

当确定了可以执⾏任务的具体节点之后，调度器会进⾏多种前置校验。 这些前置校验包括： 

  * 节点是否仍然存在 
  * 是否有 affinity 或者 anti-affinity规则 
  * 任务所依赖的端⼝在当前⼯作节点是否可以访问 
  * ⼯作节点是否有⾜够的资源等。 



不满⾜任务执⾏条件的⼯作节点会被直接忽略，剩下的⼯作节点会依据下⾯的判定规则计算得分并排序，每条判定规则都有对应的得分，得分最⾼的⼯作节点会被选中，并执⾏相应任务。具体包括： 

  * ⼯作节点上是否已经包含任务所需的镜像 
  * 剩余资源是否满⾜任务执⾏条件 
  * 正在执⾏多少任务 



如果调度器⽆法找到⼀个合适的⼯作节点，那么当前任务就⽆法被调度，并且会被标记为暂停状态。 

调度器并不负责执⾏任务，只是为当前任务选择⼀个合适的节点运⾏。 

###  ETCD 

在整个控制层中，只有集群存储是有状态（stateful）的部分，它持久化地存储了整个集群的配置与状态。因此，这也是集群中的重要组件之⼀——没有集群存储，就没有集群。 

通常集群存储底层会选⽤⼀种常⻅的分布式数据库 etcd。因为这是整个 集群的唯⼀存储源，⽤户需要运⾏ 3～5个 etcd 副本来保证存储的⾼可⽤性，并且需要有充分的⼿段来应对可能出现的异常情况。 

在关于集群的可⽤性（availability）这⼀点上，etcd 认为⼀致性⽐可⽤ 性更加重要。这意味着 etcd 在出现脑裂的情况时，会停⽌为集群提供更新能⼒，来保证存储数据的⼀致性。但是，就算 etcd 不可⽤，应⽤仍然 可以在集群性持续运⾏，只不过⽆法更新任何内容⽽已。 

对于所有分布式数据库来说，写操作的⼀致性都⾄关重要。例如，分布 式数据库需要能够处理并发写操作来尝试通过不同的⼯作节点对相同的 数据进⾏更新。etcd 使⽤业界流⾏的 RAFT ⼀致性算法来解决这个问题。 

##  工作节点 

⼯作节点是 Kubernetes 集群中的⼯作者。从整体上看，⼯作节点主要负责如下 3 件事情。 

  1. 监听 API Server 分派的新任务。 
  2. 执⾏新分派的任务。 
  3. 向控制平⾯回复任务执⾏的结果（通过 API Server）。 



###  kubltet 

Kubelet 是每个⼯作节点上的核⼼部分，是 Kubernetes 中重要的代理端，并且在集群中的每个⼯作节点上都有部署。实际上，通常⼯作节点与 Kubelet 这两个术语基本上是等价的。 

  * 在⼀个新的⼯作节点加⼊集群之后，Kubelet 就会被部署到新节点上。 然后 Kubelet 负责将当前⼯作节点注册到集群当中，集群的资源池就会获取到当前⼯作节点的 CPU、内存以及存储信息，并将⼯作节点加⼊当前资源池。 
  * Kubelet 的⼀个重要职责就是负责监听 API Server 新分配的任务。每当 其监听到⼀个任务时，Kubelet 就会负责执⾏该任务，并维护与控制平 ⾯之间的⼀个通信频道，准备将执⾏结果反馈回去。 如果 Kuberlet ⽆法运⾏指定任务，就会将这个信息反馈给控制平⾯，并由控制平⾯决定接下来要采取什么措施。例如，如果 Kubelet ⽆法执⾏⼀个任务，则其并不会负责寻找另外⼀个可执⾏任务的⼯作节点。 Kubelet 仅仅是将这个消息上报给控制平⾯，由控制平⾯决定接下来该如何做。 



###  容器运行时（Docker、Containerd、... ) 

Kubelet需要⼀个容器运⾏时（container runtime）来执⾏依赖容器才能执⾏的任务，例如拉取镜像并启动或停止容器。 

在早期的版本中，Kubernetes 原⽣⽀持了少量容器运⾏时，例如 Docker。⽽在最近的版本中，Kubernetes 将其迁移到了⼀个叫作容器运⾏时接⼝（CRI）的模块当中。从整体上来看，CRI 屏蔽了 Kubernetes 内部运⾏机制，并向第三⽅容器运⾏时提供了⽂档化接口来接⼊。 

Kubernetes ⽬前⽀持丰富的容器运⾏时。⼀个⾮常著名的例⼦就是 cri-containerd。 

这是⼀个开源的、社区维护的项⽬，将 CNCF 运⾏时通过容器运⾏时 (Docker、Containerd、...) CRI 接⼝接⼊ Kubernetes。该项⽬得到了⼴泛的⽀持，在很多 Kubernetes场景中已经替代 Docker 成为当前最流⾏的容器运⾏时。注 意：containerd（发⾳如“ container-dee ”）是基于Docker Engine 剥离出来的容器管理与运⾏逻辑。该项⽬由 Docker 公司捐献给 CNCF，并获得了⼤量的社区⽀持。同期也存在其他的符合 CRI 标准的容器运⾏ 时。 

###  Kube-proxy 

kube-proxy 运⾏在集群中的每个⼯作节点，负责本地集群⽹络。例如，kube-proxy 保证了每个⼯作节点都可以获取到唯⼀的 IP 地址，并且实现了本地 IPTABLE 以及 IPVS 来保障 Pod 间的⽹络路由与负载均衡。 

###  Pod 

在 VMware 的世界中，调度的原子单位是虚拟机（VM）；在 Docker 的 世界中，调度的原⼦单位是容器；⽽在Kubernetes 的世界中，调度的原子单位是 Pod。 

Kubernetes 的确⽀持运⾏容器化应⽤。但是，⽤户⽆法直接在 Kubernetes 集群中运⾏⼀个容器，容器必须并且总是需要在 Pod 中才能运⾏。 

####  Pod 与容器 

⼀种最简单的⽅式就是，在每个Pod中只运⾏⼀个容器，也是最常使用的方式。 

当然，还有⼀种更⾼级的⽤法，在⼀个 Pod 中会运⾏⼀组容器，称为多容器 Pod（multi-container Pod）。 

**服务⽹格 SideCar**

![](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/bb16b0592ca84897bd7bcaa08c292ed2~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp) 

**应用适配器**

![](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/c8bd9c1b3ee840f3846f5e650472e7bc~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp) 

####  Pod 剖析 

整体看来，pod 是一个用于运行容器的有限制的环境。Pod 本身并不会运行任何东西，只是作为一个承载容器的沙箱而存在。换一种说法：Pod 就是为用户在宿主机操作系统中划出有限的一部分特定区域，构建一个网格栈，创建一组内核命名空间，并且在其中运行一个或多个容器，这就是 Pod。 

如果在 Pod 中运行多个容器，那么多个容器间是共享相同的 Pod 环境的，举个例子：运行在相同 Pod 中所有容器都有相同的 IP 地址，同一个 Pod 间的两个容器需要相互通信，使用 Pod 提供的 localhost 接口就可以完成。共享环境包括了 

  * IPC 命名空间 
  * 共享的内存 
  * 共享的磁盘 
  * 网络 
  * 其他资源 



对于存在强绑定关系的多个容器，比如需要共享内存与存储，多容器 Pod 就是一个非常完美的选择。如果不存在如此紧密的关系，更好的方式是将容器封装到不同的 Pod，通过网络以松耦合的方式来运行，这样可以在任务级别实现容器间的管理，降低之间的影响，当然这样会导致大量的未加密的网络流量产生。 

####  Pause 容器 

Pause 容器，全称 infrastuctue container（又叫 infra）基础容器，作为 init pod 存在，其它 pod 都会从 pause 容器中 fork 出来 

  * 每个 Pod 里运行着一个特殊的被称之为 Pause 的容器，其他容器则为业务容器，这些业务容器共享 Pause 容器的网络栈和 Volume 挂载卷 
  * 因此他们之间通信和数据交换更为高效，在设计时我们可以充分利用这一特性将一组密切相关的服务进程放到同一个 Pod 中 
  * 同⼀个Pod⾥的容器之间仅需通过localhost就能互相通信。 



Pause 容器主要为每个业务容器提供以下功能： 

  * Pid 命名空间：Pod 中的不同应用程序可以看到其他应用程序的进程 ID 
  * 网络命名空间：Pod 中的多个容器可以访问同一个 IP 和端口范围 
  * IPC 命名空间：Pod 中的多个容器能使用 SysteV IPC 或 POSIX 消息队列进行通信 
  * UTS 命名空间：Pod 中的多个容器共享一个主机名；Volumes（共享存储卷） 
  * Pod 中各个容器可以访问在 Pod 级别定义的 Volumes 



![](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/0eb0a4d927634dddb373b5353afa48e0~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp) 

####  调度单元 

kubernetes 中最小的调度单元是 Pod，如果读者要扩容或缩容自己的应用，可以通过添加或删除 Pod 来实现。千万不要选择通过向一个已经存在的 Pod 中增加更多的容器这种方式来完成扩容，多容器仅适用于两个的确是不同容器但又要共享资源的场景。 

####  原子操作单位 

Pod 的部署是一个原子单位，只有当 Pod 中所有容器启动成功并且处于运行状态时，Pod 提供的服务才会被认为是可用的，否者会被认为启动失败，而启动失败的不会相应服务请求。 

####  Pod 的生命周期 

Pod 的生命周期是有限的，Pod 会被创建并运行，并且最终被销毁，如果 Pod 初心预期外的销毁，用户无需将其重新启动，因为 Kubernetes 会启动一个新的 Pod 来取代偶问题的 Pod，尽管新启动的 Pod 看起来和原来的 Pod 完全一样，但本质上不是同一个。这是一个有全新 IP 地址的 Pod。 

###  Deployment（部署） 

Deployment 主要用于部署无状态服务，是最常用的 Pod 控制器，Deployment 是对 Pod 更高一层的封装，除 Pod 之外，还提供了如扩缩容管理、一键回滚、不停机更新以及版本控制及其他特性。 Pod 部署。上层控制器包括：Deployment、DaemonSet 以及 StatefulSet。 

Deployment 是对 Pod 更高一层的封装，除 Pod 之外，还提供了如扩缩容管理、不停机更新以及版本控制及其他特性。 

Deployment、DaemonSet 以及 StatefulSet 还实现了自己 controller 与监控循环，可以持续监控集群状态，并保证当前状态与期望状态相符。 

  * 无状态服务 
    * ⽆状态服务不会在本地存储持久化数据 ，多个 pod 间是没有关系的，A 服务停机或增加对其他服务没有影响 
  * 有状态服务 
    * 有状态服务需要在本地存储持久化数据据，典型的是分布式数据库的应用，分布式节点实例之间有依赖的拓扑关系。比如，主从关系，如果 K8S 停止分布式集群中任⼀实例 pod，就可能会导致数据丢失或者集群的 crash。 



![image.png](https://hg-tech-1300607181.cos.ap-guangzhou.myqcloud.com/blog/413f61eb12b744c58ba794db7fff6ba2~tplv-k3u1fbpfcp-zoom-in-crop-mark:1512:0:0:0.awebp) 

####  扩展：Replication Controller(RC) vs ReplicatSet(RS) 

#####  Replication Controller(RC) 

使用 RC 可以自动使 Pod 副本数量到达指定数量，确保一组 Pod 总是可用的。 

如果存在的 Pod 大于设置的数量，那么 RC 会杀掉多余的 Pod，相反，如果小于，RC 会启动一些 Pod。 

缺点：选择器只能精准匹配 
    
    
    ```yaml
    apiVersion: v1
    kind: ReplicationController
    metadata:
     name: nginx
    spec:
     replicas: 3
     # 精准匹配
     selector:
     	app: nginx
     template:
     	metadata:
     		name: nginx
     		labels:
     			app: nginx
     spec:
     	containers:
     	- name: nginx
     		image: nginx
     		ports:
     		- containerPort: 80
    
    ```

#####  Replication Set(RS) 

RS 是新一代的 RC，RS 主要作用于 Deployment 协调创建、删除、更新 Pod，和 RC 的区别是：RS 支持标签选择器。 

在实际应用中，RS 可以单独使用，但是一般使用 Deployment 来自动管理 RS，除非自定义的 Pod 不需要更新或者其他编排等。 

RC 和 RS 的创建删除和 Pod 并没有太⼤的区别，并且 RC 在实际⽣产环境 基本已经不再使⽤，RS 也很少单独使用，⼀般都会根据需求使⽤更⾼级的 Deployment、DaemonSet、StatefulSet 来管理 Pod。 
    
    
    ```yaml
    apiVersion: apps/v1
    kind: ReplicaSet
    metadata:
     name: frontend
     labels:
     	app: test
    sepc:
     replicas: 3
     selector:
     	matchLabels:
     		app: test
     	matchExpressions:
     	- {key: tier,operator: ln,values: [frontend]}
     template:
     	metadata:
     		labels:
     		app: test
     sepc:
     	containers:
     	- name: redis
     		images: redis:v1.0
     		resources:
     			requests:
     				cpu: 100m
     				memory: 100Mi
     		env:
     		- name: GET_HOSTS_FROM
     			value: dns
     		ports:
     		- containerPort: 6379
    
    ```

###  Service（服务） 

⼀个稳定的⽹络终端，提供了基组动态 Pod 集合的 TCP 以及 UDP 负载均衡能力。 

Pod 是非常重要的，但是可能随时会出现故障并销毁。如果通过 Deployment 或者 DaemonSet 对 Pod 进行管理，出现故障的 Pod 会自动被替换。但替换后哦的新 Pod 会拥有完全不同的 IP 地址，也就是 Pod 是不可靠的。 

Kubernetes Service 提供了一个稳定的服务名称与 IP 地址，并且对于其下的 Pod 提供了请求级别的负载均衡机制。 

###  Containerd 

配置要求： 

  * 3.10的kernel 问题太多了。也是k8s 支持的最低版本。 



cgroup 的 kmem account 特性在 3.x 内核上有内存泄露问题，如果开启了 kmem account 特性会导致可分配内存越来越少，直到无法创建新 pod 或节点异常。建议升级到最新的稳定内核版本。 

[ Kubernetes CentOS7.4 系统内核升级 修复 K8S 内存泄露问题 ](https://link.juejin.cn?target=https%3A%2F%2Fblog.csdn.net%2Fqq_34556414%2Farticle%2Fdetails%2F119827902 "https://blog.csdn.net/qq_34556414/article/details/119827902")

[ CentOS 7升级内核的三种方式 ](https://link.juejin.cn?target=https%3A%2F%2Fwww.cnblogs.com%2Fhaoee%2Fp%2F16402200.html "https://www.cnblogs.com/haoee/p/16402200.html")

:::tip 版权说明
本文由程序自动从互联网获取，如有侵权请联系删除，版权属于原作者。

作者：wzl

链接：https://juejin.cn/post/7243081126826016805
::: 
