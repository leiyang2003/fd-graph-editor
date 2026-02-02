import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

# 中文字体：避免节点标签/标题显示为 □ 方块（tofu）
matplotlib.rcParams["font.sans-serif"] = [
    "PingFang SC", "Heiti SC", "Songti SC", "Arial Unicode MS", "STHeiti", "sans-serif"
]
matplotlib.rcParams["axes.unicode_minus"] = False  # 负号不显示为方块

# 创建有向图
G = nx.DiGraph()

# ------------------ 手动添加主要节点和边（可写脚本解析 YAML 自动化） ------------------

# 起点
G.add_node("Start", label="开始\n(sanity=100, dusty)")

# Chapter 1
G.add_node("intro", label="intro\n描述发现镜子", shape="box")
G.add_node("first_choice", label="first_choice\n怎么处理镜子？", shape="diamond")
G.add_edge("Start", "intro")
G.add_edge("intro", "first_choice")

# 选项分支
G.add_node("clean", label="擦干净它\n→ activated, sanity-10")
G.add_node("ignore", label="忽略\n→ night")
G.add_node("shatter_early", label="直接砸碎\n→ BAD END", shape="ellipse", style="filled", fillcolor="red")
G.add_edge("first_choice", "clean", label="擦")
G.add_edge("first_choice", "ignore", label="忽略")
G.add_edge("first_choice", "shatter_early", label="砸")

# ignore → night_event → clean
G.add_node("night_event", label="night_event\n强制激活")
G.add_edge("ignore", "night_event")
G.add_edge("night_event", "clean")

# clean → chapter2
G.add_node("chapter2_intro", label="chapter2_intro\n低语开始")
G.add_edge("clean", "chapter2_intro")

# Chapter 2 主要分支（简化）
G.add_node("investigate", label="investigate\n如何调查？", shape="diamond")
G.add_edge("chapter2_intro", "investigate")

G.add_node("touch", label="触摸镜面")
G.add_node("research", label="研究符号")
G.add_node("seek_help", label="求助（循环）")
G.add_edge("investigate", "touch", label="触摸")
G.add_edge("investigate", "research", label="研究")
G.add_edge("investigate", "seek_help", label="求助")
G.add_edge("seek_help", "investigate")  # 循环

# touch 分支（简化 sanity 条件）
G.add_node("mirror_world", label="mirror_world\n三扇门")
G.add_edge("touch", "mirror_world")

G.add_node("past_door", label="过去 → fire_clue")
G.add_node("present_door", label="现在 → NEUTRAL END", shape="ellipse", style="filled", fillcolor="orange")
G.add_node("future_door", label="未来 → escape")
G.add_edge("mirror_world", "past_door")
G.add_edge("mirror_world", "present_door")
G.add_edge("mirror_world", "future_door")

# research → ritual → good/bad
G.add_node("ritual_choice", label="ritual_choice\n用银十字？")
G.add_node("perform_ritual", label="执行 → GOOD END", shape="ellipse", style="filled", fillcolor="lightgreen")
G.add_node("hesitation", label="犹豫 → POSSESSED END", shape="ellipse", style="filled", fillcolor="purple")
G.add_edge("research", "ritual_choice")
G.add_edge("ritual_choice", "perform_ritual")
G.add_edge("ritual_choice", "hesitation")

# Chapter 3（weakened）
G.add_node("chapter3", label="chapter3\n最终对抗")
G.add_node("burn", label="烧毁 → NEUTRAL", shape="ellipse", style="filled", fillcolor="orange")
G.add_node("seal", label="封印 → GOOD", shape="ellipse", style="filled", fillcolor="lightgreen")
G.add_edge("perform_ritual", "chapter3")   # 假设从 perform 到 ch3
G.add_edge("chapter3", "burn")
G.add_edge("chapter3", "seal")

# 结局汇总（可指向统一 END 节点或分开）
G.add_node("BAD", label="BAD END\n(多种)", shape="ellipse", style="filled", fillcolor="red")
G.add_node("NEUTRAL", label="NEUTRAL", shape="ellipse", style="filled", fillcolor="orange")
G.add_node("GOOD", label="GOOD END", shape="ellipse", style="filled", fillcolor="lightgreen")

G.add_edge("shatter_early", "BAD")
G.add_edge("present_door", "NEUTRAL")
G.add_edge("hesitation", "BAD")
G.add_edge("burn", "NEUTRAL")
G.add_edge("seal", "GOOD")
# ... 其他结局类似连接

# ------------------ 画图 ------------------
# 用仅含结构的子图算布局，避免 node/edge 属性写入 DOT 时导致解析错误
G_layout = nx.DiGraph()
G_layout.add_edges_from(G.edges())
pos = graphviz_layout(G_layout, prog="dot")   # dot 适合层次结构；试试 "twopi", "circo", "fdp"
plt.figure(figsize=(14, 10))
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'),
        node_size=3000, node_color="lightblue", font_size=8,
        font_family="sans-serif",  # 使用上面配置的中文 sans-serif 字体
        arrows=True, arrowstyle="->", arrowsize=20)
plt.title("被诅咒的古镜 - 故事流程图（简化版）")
plt.axis("off")
plt.tight_layout()
plt.show()   # 或 plt.savefig("story_graph.png", dpi=300)
plt.savefig("story_graph.png", dpi=300)  # 先保存成图片查看
print("图片已保存为 story_graph.png")