# IdealYard

使用 `Vue` 和 `Flask` 搭建前后端分离的 RESTful 个人博客。
## 前置条件  

### Python

3.6+

### MySQL

```bash
mysql  Ver 14.14 Distrib 5.7.26, for linux-glibc2.12 (x86_64) using  EditLine wrapper
```
### 创建数据库

开发模式数据库：`iyblog_dev`，此处可以在[此处](back/config.py)修改配置

```sql
CREATE USER 'USERNAME'@'localhost' IDENTIFIED BY 'PASSWORD';
-- 如果需要支持emoji，则设置utf8mb4编码。否则使用utf-8编码即可
CREATE DATABASE DATABASENAME CHARSET=utf8mb4;
grant all privileges on DATABASENAME.* to USERNAME@localhost identified by 'PASSWORD';
flush privileges;
```
### 环境配置

1. 进入当前目录之后，先通过pip安装pipenv管理包
    ```bash
    pip install pipenv [--user]
    ```
2. 安装Python依赖
    ```bash
    pipenv install 
    ```
3. 配置环境变量
    ```bash
    vi .flaskenv
    ```
4. 编辑[dot.env](https://github.com/imoyao/idealyard/blob/master/dot.env)文件,配置环境变量并重命名为`.env`

    ```bash
    vi dot.env
    mv dot.env .env        # 参考 master 分支
    ```
## docker 支持

pass

  
## TODO

因为时间关系，还有一些问题没有解决，详见[此处](./document/TODOlist.md)
如果有同学需要`PR`，可以参考此处已知未解决问题和`bug`单。

## 更多
与其在别处仰望,不如在这里并肩。 
开发模式配置及说明参见[更多文档](./document/deploy.md)

### 代码概览

目录结构和代码量统计参考[此处](./document/README.MD)  

## 致谢   
由于本仓库是在fork这位博主：[@imoyao](https://github.com/imoyao)
他的的这个仓库：[idealyard](https://github.com/imoyao/idealyard)

感谢他！

但由于他叨逼叨的在肉麻的感谢某位妹子，我在这不得已改了这个致谢，毕竟我敬爱的媳妇儿[@crystal](https://github.com/Anxiaozhuang)
生气起来可能是一个毁天灭地的效果。嗯，感谢她。


---
> Она даётся ему один раз, и прожить её надо так, чтобы не было мучительно больно за бесцельно прожитые годы, чтобы не жёг позор за подленькое и мелочное прошлое и чтобы, умирая, смог сказатывся жизнь и все силы были отданы самому прекрасному в мире - борьбе за освобождение человечества.
>
>人最宝贵的东西是生命.
>生命对于我们只有一次.
>一个人的生命应当这样度过：
>当他回首往事的时候,
>也不因虚度年华而悔恨,
>也不因碌碌无为而羞愧——这样,
>在临死的时候,它能够说：
>“我整个的生命和全部精力,
>都已献给世界上最壮丽的事业
>——为人类的解放而斗争.”
>

-- 《钢铁是怎样炼成的》 保尔·柯察金

