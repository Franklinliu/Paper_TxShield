"""Shared publication style for Figures 4 and 5; source values unchanged."""
from pathlib import Path
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
INK = '#26323A'
COLORS = ['#7895AA', '#C49A79', '#82A499', '#A398B4']
plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 9.5,
    'text.color': INK, 'axes.labelcolor': INK,
    'xtick.color': INK, 'ytick.color': INK,
    'pdf.fonttype': 42, 'ps.fonttype': 42,
    'axes.labelsize': 9.5, 'xtick.labelsize': 9, 'ytick.labelsize': 9.5,
    'hatch.linewidth': .35,
})

def style(ax, grid_axis):
    ax.set_axisbelow(True)
    ax.grid(axis=grid_axis, color='#E6EAED', linewidth=.6)
    ax.tick_params(axis='both', length=0, pad=5)
    ax.spines[['top', 'right']].set_visible(False)
    for side in ['bottom', 'left']:
        ax.spines[side].set_color('#CBD2D8')
        ax.spines[side].set_linewidth(.6)

def save(fig, name):
    fig.savefig(ROOT / 'pic' / f'{name}.pdf')
    fig.savefig(ROOT / 'pic' / f'{name}.png', dpi=220)
    plt.close(fig)

# Figure 4: keep all categories and their original order, with compact row spacing.
labels = [
    'Business Logic Flaws', 'Price-related Attacks',
    'Reentrancy & Call Attacks', 'Access Control Vulnerabilities',
    'Input Validation Issues', 'Flashloan-driven Attacks',
    'Mathematical Calculation Issues', 'Token Mechanism Vulnerabilities',
    'Other (20+ subtypes)',
]
counts = np.array([125, 65, 43, 31, 22, 22, 19, 10, 27])
assert counts.sum() == 364
percent = counts / counts.sum() * 100
fig, ax = plt.subplots(figsize=(7.5, 2.45))
fig.subplots_adjust(left=.365, right=.985, bottom=.215, top=.99)
y = np.arange(len(labels))
ax.barh(y, percent, height=.58, color=COLORS[0], zorder=3)
ax.set_yticks(y, labels)
ax.invert_yaxis()
ax.set_xlim(0, 44)
ax.set_xticks([0, 10, 20, 30, 40])
ax.set_xlabel('Share of attack transactions (%)', labelpad=5)
style(ax, 'x')
ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', pad=8)
for i, (value, count) in enumerate(zip(percent, counts)):
    ax.text(value + .65, i, f'{value:.1f}% ({count})', va='center', fontsize=9.5)
save(fig, 'attack_distribution_bar')

# Figure 5: nine backbones together, with all four metrics preserved.
with (ROOT / 'reports/revision_20261011/fig5_data.csv').open() as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 9
keys = ['accuracy_percent', 'precision_percent', 'recall_percent', 'f1_percent']
values = np.array([[float(row[key]) for key in keys] for row in rows])
ticks = ['GPT-4.1\nmini', 'Baidu ERNIE\nSpeed-128k', 'Llama3-8B',
         'Qwen3-8B', 'DeepSeek-R1\nDistill-Qwen-7B', 'InternLM3',
         'GPT-5.6\nluna', 'DeepSeek-v4\npro', 'Kimi-k3']
fig, ax = plt.subplots(figsize=(7.5, 2.35))
fig.subplots_adjust(left=.075, right=.992, bottom=.26, top=.82)
x = np.arange(len(rows))
width = .195
for j, (label, hatch) in enumerate(zip(['Accuracy', 'Precision', 'Recall', 'F1'], ['', '//', '..', '\\\\'])):
    ax.bar(x + (j - 1.5) * width, values[:, j], width, label=label,
           color=COLORS[j], edgecolor='#50616D', linewidth=.3, hatch=hatch, zorder=3)
ax.set_xticks(x, ticks)
ax.tick_params(axis='x', labelsize=8)
ax.set_xlim(-.6, 8.6)
ax.set_ylim(0, 105)
ax.set_yticks(np.arange(0, 101, 20))
ax.set_ylabel('Metric (%)', labelpad=5)
style(ax, 'y')
ax.legend(loc='lower center', bbox_to_anchor=(.5, 1.025), ncol=4,
          frameon=False, fontsize=9.5, handlelength=1.6, columnspacing=1.8)
save(fig, 'model_performance_column_chart')
