# ptool
发种工具ptool运行在发种员机器上

## 功能
- [x] 用户输入
    - [x] 选择本地文件/文件夹
    - [x] 输入豆瓣地址
- [x] 自动生成
    - [x] 自动为选中的视频文件创建缩略图 `ffmpeg`
    - [x] 自动上传缩略图到图床
    - [x] 自动捕获视频文件的media info `mediainfo`
- [x] 最终产出
    - 在海胆pt站创建种子条目
- [x] Docker内服务使用supervisor托管
- [x] 容器内代码更新功能，避免发布新版本后，需要使用新镜像重建容器

## 依赖
- python3.8
- ffmpeg
- mediainfo

## 使用
[docker hub](https://hub.docker.com/r/blllicn/ptools)


## 技术实现
Docker内服务使用supervisor托管

- /var/web/ptools
  - app
    - app
      - uploads # 软链接/uploads
  - app_backup
  - manager
  - db 
  - log
- /uploads