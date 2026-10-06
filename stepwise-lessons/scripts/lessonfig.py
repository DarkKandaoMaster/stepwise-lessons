"""stepwise-lessons 技能的作图工具。复制到课程目录后，在 make_figures.py 里 `from lessonfig import *`。

提供：中文字体设置、统一配色、relu、style、save、sum_panels（A + B = C 三联图）、flow_diagram（方框箭头示意图）、
surface3d（带地面和重点线条的 3D 曲面）、try_views（并排试视角）。
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# 雅黑没有 ₁₂ 等下标字形：下标请写成 mathtext，如 "$x_1$"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["font.size"] = 12

C1, C2, C3, GREY = "#1f6f8b", "#d1495b", "#edae49", "#888888"  # 主色、对比色、第三色、灰
PALETTE = [C1, C2, C3, "#5a8f29", "#7b4b94"]

OUT = Path.cwd() / "img"


def relu(t):
    return np.maximum(0, t)


def style(ax, xl=None, yl=None):
    """去掉上右边框、加浅网格、设坐标轴标签。"""
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.25)
    if xl:
        ax.set_xlabel(xl)
    if yl:
        ax.set_ylabel(yl)


def save(fig, name, out=None):
    """保存到 img/name（150 dpi），并关闭图。返回路径，生成后记得用 Read 看一眼。"""
    out = Path(out) if out else OUT
    out.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    path = out / name
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def sum_panels(xs, parts, total_title, colors=None, op="+", figsize=None):
    """画 "A + B (+ …) = 合计" 的并排面板。

    parts: [(标题, y 数组), ...]；合计为各 y 之和。返回 fig。
    """
    colors = colors or PALETTE
    n = len(parts) + 1
    fig, axes = plt.subplots(1, n, figsize=figsize or (3.7 * n, 3.2), sharey=True)
    total = np.zeros_like(xs, dtype=float)
    for i, (t, y) in enumerate(parts):
        axes[i].plot(xs, y, color=colors[(i + 2) % len(colors)], lw=3)
        axes[i].set_title(t, fontsize=11)
        style(axes[i], "x")
        total = total + y
    axes[-1].plot(xs, total, color=colors[0], lw=3)
    axes[-1].set_title(total_title, fontsize=11)
    style(axes[-1], "x")
    ymid = (np.nanmin(total) + np.nanmax(total)) / 2
    for i in range(1, n):
        sym = "=" if i == n - 1 else op
        x0 = xs.min() - 0.18 * (xs.max() - xs.min())
        axes[i].text(x0, ymid, sym, fontsize=26, ha="center", va="center")
    return fig


def surface3d(ax, X, Y, Z, *, zlim=None, ground=True, cmap="RdBu_r", lines=(), labels=(),
              view=(25, -150), xlabel="$x_1$", ylabel="$x_2$", zlabel="z", title=None):
    """在 3D 坐标轴上画曲面。

    ax: fig.add_subplot(..., projection="3d")
    ground: 画半透明地面 z=0
    lines: [(xs, ys, zs, dict(样式)), ...]，画在曲面上方（折痕、剖面线等）
    labels: [(x, y, z, 文本), ...]
    颜色按 zlim 对称映射：红高、蓝低、白为 0。
    """
    ax.computed_zorder = False  # 否则线条会被曲面遮住
    zmax = zlim if zlim is not None else float(np.nanmax(np.abs(Z))) or 1.0
    if ground:
        ax.plot_surface(X, Y, 0 * X, color="#7fa37f", alpha=0.22, linewidth=0, zorder=1)
    ax.plot_surface(X, Y, Z, facecolors=plt.get_cmap(cmap)((Z + zmax) / (2 * zmax)),
                    linewidth=0.15, edgecolor="#555555", shade=False, alpha=0.9, zorder=2)
    for i, (lx, ly, lz, kw) in enumerate(lines):
        kw = {"color": "black", "lw": 3, **kw}
        ax.plot(lx, ly, lz, zorder=10 + i, **kw)
    for x, y, z, t in labels:
        ax.text(x, y, z, t, fontsize=12, zorder=50)
    ax.set_zlim(-zmax, zmax)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_zlabel(zlabel)
    if title:
        ax.set_title(title, fontsize=11)
    ax.view_init(*view)
    return ax


def flow_diagram(nodes, *, edges=None, notes=(), figsize=None, box_w=1.8, box_h=0.8, gap=0.5,
                 colors=("#e8eef2", "#d7e8ef", "#fbe8c8")):
    """方框加箭头的示意图（网络结构、流程、比喻里的角色关系），框里可写中文。

    nodes: [(文本, 列号, 行号, 颜色下标), ...]；列号、行号可为小数，行号向上为正。
    edges: [(起点下标, 终点下标), ...]；省略时按 nodes 顺序依次相连。
    notes: [(x, y, 文本, 颜色), ...]，坐标单位与方框相同：第 c 列方框左缘 x = c*(box_w+gap)，第 r 行下缘 y = r*(box_h+gap)。
    返回 fig。
    """
    import matplotlib.patches as mpatches
    if edges is None:
        edges = [(i, i + 1) for i in range(len(nodes) - 1)]
    step = box_w + gap
    xs = [c * step for _, c, _, _ in nodes]
    ys = [r * (box_h + gap) for _, _, r, _ in nodes]
    W = max(xs) + box_w; H_lo = min(ys); H_hi = max(ys) + box_h
    fig, ax = plt.subplots(figsize=figsize or (max(4.0, 1.25 * W), max(2.2, 1.25 * (H_hi - H_lo) + 0.9)))
    ax.set_xlim(-0.2, W + 0.2); ax.set_ylim(H_lo - 0.6, H_hi + 0.6); ax.axis("off")
    for (t, _, _, ci), x, y in zip(nodes, xs, ys):
        ax.add_patch(mpatches.FancyBboxPatch((x, y), box_w, box_h, boxstyle="round,pad=0.04",
                                             fc=colors[ci % len(colors)], ec="#555555"))
        ax.text(x + box_w / 2, y + box_h / 2, t, ha="center", va="center", fontsize=12)
    for a, b in edges:
        xa, ya, xb, yb = xs[a], ys[a], xs[b], ys[b]
        if abs(ya - yb) < 1e-9:
            p0 = (xa + box_w, ya + box_h / 2) if xb > xa else (xa, ya + box_h / 2)
            p1 = (xb, yb + box_h / 2) if xb > xa else (xb + box_w, yb + box_h / 2)
        else:
            p0, p1 = (xa + box_w, ya + box_h / 2), (xb, yb + box_h / 2)
        ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", lw=1.8, color="#333333"))
    for x, y, t, c in notes:
        ax.text(x, y, t, ha="center", fontsize=11, color=c)
    return fig


def try_views(X, Y, Z, views=((25, -150), (25, -100), (30, -60), (25, -20), (30, 30), (35, 120)),
              name="_try_views.png", **kw):
    """把同一曲面按多个视角并排画在一张小图上，用来挑视角。看完可删。"""
    n = len(views)
    fig = plt.figure(figsize=(4 * n, 4))
    for i, v in enumerate(views):
        ax = fig.add_subplot(1, n, i + 1, projection="3d")
        surface3d(ax, X, Y, Z, view=v, title=f"view={v}", **kw)
    return save(fig, name)


__all__ = ["np", "plt", "cm", "C1", "C2", "C3", "GREY", "PALETTE", "OUT", "relu", "style", "save",
           "sum_panels", "surface3d", "flow_diagram", "try_views"]
