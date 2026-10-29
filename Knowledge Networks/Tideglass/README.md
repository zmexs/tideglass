🌌 3D 记忆星图 (Memory Star)

基于 MongoDB、Flask 与 3D-Force-Graph 构建的个人 AI 记忆知识图谱与可视化系统。

它将大语言模型（如 DeepSeek）的结构化记忆以 3D 发光星系的形式展现，并内置了安全的本地 API，让你的 AI 真正拥有“外挂海马体”。



✨ 核心亮点 (Features)

🔮 极致 3D 可视化：基于 WebGL 渲染的 3D 球状星系，支持鼠标任意拖拽、滚轮缩放、视角自动环绕。

💫 流光粒子特效：节点之间的连线带有动态流动的粒子效果，直观展示知识关联的方向与流动。

🛡️ 绝对隐私的安全架构：前端源码绝对干净，不包含任何真实记忆数据。所有数据均通过本地 Flask 后台实时从 MongoDB 动态拉取（前后端分离）。

⏳ 时间轴回溯系统：左侧面板内置时间轴滑块，拖动即可像“时间旅行”一样，查看过去某个时间点的记忆网络生长状态。

🔍 双向检索交互：



左侧支持节点名称模糊搜索与类型筛选（人物、项目、概念等）。

右侧悬浮窗实时展示结构化的关系链（如：张三 --\[负责]--> AI助手）。

点击节点，3D 镜头会自动飞向该节点并展示详情。

🧠 AI 友好 (RAG Ready)：内置结构化数据 API 接口，完美支持 DeepSeek 等大模型的 Function Calling，实现“按需查库，极度省 Token”。





Tideglass/

├── server.py              # Flask 后台 API，负责动态拉取数据并保护隐私

├── db.py                  # MongoDB 数据库连接配置

├── memory.py              # 记忆的增删改查核心逻辑

├── app.py                 # 命令行工具（快速添加节点/关系）

├── search.py              # 本地终端检索脚本

├── chat.py                # 接入 DeepSeek 的对话脚本（包含 Function Calling）

├── star\_template.html     # 3D 前端页面（无真实数据，安全可开源）

├── requirements.txt       # 依赖清单

└── .gitignore             # Git 忽略配置（防止隐私数据泄露）





1\. 安装依赖

请确保你的本地已安装 Python 及 MongoDB 服务。

pip install -r requirements.txt

2\. 启动本地服务

运行后台服务器（默认运行在 5000 端口）：

python server.py



3\. 访问星图

在浏览器中打开：http://127.0.0.1:5000

(⚠️ 注意：请务必通过本地服务器访问，直接双击 HTML 文件将无法加载数据。)



🧠 如何让 AI 拥有记忆

本项目不仅是一个可视化工具，更是 AI 的记忆库。

1\.使用 python app.py node 或 python chat.py 向 MongoDB 写入记忆。

2\.在 AI 对话中，通过 chat.py 提供的工具调用机制，让 DeepSeek 在回答前自动去查询星图数据。

3\.结合 http://127.0.0.1:5000/api/graph 接口，你可以让任何支持联网/API请求的 AI Agent 都能“读取”你的记忆星图。

🛡️ 隐私与安全声明

本项目的初衷是打造私有的 AI 记忆体。因此：

\-前端页面不嵌入任何硬编码的记忆数据。

\-建议在 .gitignore 中忽略所有的本地数据库文件及导出的 .md 记忆快照。

\-不要将 server.py 部署到公网（0.0.0.0），仅供本地环境（127.0.0.1）使用。



Built with ❤️ and a little bit of starlight.





