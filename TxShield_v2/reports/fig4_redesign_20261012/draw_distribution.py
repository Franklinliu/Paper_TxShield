from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
# Counts and category names preserved from the original Figure 4.
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
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                     'pdf.fonttype': 42, 'ps.fonttype': 42})
fig, ax = plt.subplots(figsize=(7.5, 3.65))
fig.subplots_adjust(left=.405, right=.98, bottom=.16, top=.985)
y = np.arange(len(labels))
ax.barh(y, percent, height=.57, color='#7895AA', edgecolor='none', zorder=3)
ax.set_yticks(y, labels, fontsize=11)
ax.invert_yaxis()
ax.set_xlim(0, 44)
ax.set_xticks([0, 10, 20, 30, 40], ['0', '10', '20', '30', '40'])
ax.set_xlabel('Share of attack transactions (%)', fontsize=11, labelpad=7)
ax.tick_params(axis='y', length=0, pad=9, labelcolor='#202830')
ax.tick_params(axis='x', length=0, pad=6, labelcolor='#46515A')
ax.xaxis.grid(True, color='#E6EAED', linewidth=.65, zorder=0)
for side in ['top', 'right', 'left']:
    ax.spines[side].set_visible(False)
ax.spines['bottom'].set_color('#CBD2D8')
for i, (value, count) in enumerate(zip(percent, counts)):
    ax.text(value + .7, i, f'{value:.1f}% ({count})', va='center',
            fontsize=11, color='#202830')
fig.savefig(ROOT / 'pic/attack_distribution_bar.pdf')
fig.savefig(ROOT / 'pic/attack_distribution_bar.png', dpi=220)
plt.close(fig)
