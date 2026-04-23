import matplotlib.pyplot as plt
import numpy as np

# ── RENKLER ──────────────────────────────────────────────
FLASK_COLOR   = "#007bff"   # mavi  (Flask'ın rengi)
FASTAPI_COLOR = "#00c853"   # yeşil (FastAPI'nin rengi)

# ── VERİLER ──────────────────────────────────────────────
projects = ["Flask", "FastAPI"]

loc_data = {
    "LOC":      [9499,  19305],
    "SLOC":     [4215,  15807],
    "Comments": [718,   376],
    "Blank":    [1942,  2278],
}

cc_data = {
    "avg_cc":     [2.73, 3.40],
    "blocks":     [410,  365],
}

mi_data = {
    "Grade A": [24, 46],
    "Grade B": [0,  2],
    "Grade C": [0,  1],
    "Lowest":  [22.29, 1.38],
}

comment_ratio = [17, 2]   # %


# ════════════════════════════════════════════════════════
# GRAFİK 1 — LOC Karşılaştırması (grouped bar)
# ════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(9, 5))

labels   = list(loc_data.keys())
flask_v  = [loc_data[k][0] for k in labels]
fastapi_v= [loc_data[k][1] for k in labels]

x   = np.arange(len(labels))
w   = 0.35

bars1 = ax.bar(x - w/2, flask_v,  w, label="Flask",   color=FLASK_COLOR,   alpha=0.85)
bars2 = ax.bar(x + w/2, fastapi_v, w, label="FastAPI", color=FASTAPI_COLOR, alpha=0.85)

ax.set_title("LOC Metrics Comparison: Flask vs FastAPI", fontsize=14, fontweight="bold")
ax.set_ylabel("Line Count")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.bar_label(bars1, padding=3, fontsize=9)
ax.bar_label(bars2, padding=3, fontsize=9)
ax.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("results/chart_1_loc.png", dpi=150)
plt.close()
print("✅ chart_1_loc.png kaydedildi")


# ════════════════════════════════════════════════════════
# GRAFİK 2 — Yorum Oranı (pie charts yan yana)
# ════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))

for ax, ratio, name, color in [
    (ax1, comment_ratio[0], "Flask",   FLASK_COLOR),
    (ax2, comment_ratio[1], "FastAPI", FASTAPI_COLOR),
]:
    ax.pie(
        [ratio, 100 - ratio],
        labels=["Comments", "Other"],
        colors=[color, "#e0e0e0"],
        autopct="%1.0f%%",
        startangle=90,
    )
    ax.set_title(f"{name} — Comment Ratio", fontsize=12, fontweight="bold")

plt.suptitle("Comment Ratio Comparison", fontsize=13)
plt.tight_layout()
plt.savefig("results/chart_2_comment_ratio.png", dpi=150)
plt.close()
print("✅ chart_2_comment_ratio.png kaydedildi")


# ════════════════════════════════════════════════════════
# GRAFİK 3 — Cyclomatic Complexity (bar + blok sayısı)
# ════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Sol: ortalama CC
bars = ax1.bar(projects, cc_data["avg_cc"],
               color=[FLASK_COLOR, FASTAPI_COLOR], alpha=0.85, width=0.4)
ax1.set_title("Average Cyclomatic Complexity", fontsize=12, fontweight="bold")
ax1.set_ylabel("CC Score")
ax1.set_ylim(0, 5)
ax1.bar_label(bars, padding=3, fontsize=10)
ax1.grid(axis="y", linestyle="--", alpha=0.4)
ax1.axhline(y=5, color="red", linestyle="--", alpha=0.5, label="Grade B threshold")
ax1.legend(fontsize=8)

# Sağ: blok sayısı
bars2 = ax2.bar(projects, cc_data["blocks"],
                color=[FLASK_COLOR, FASTAPI_COLOR], alpha=0.85, width=0.4)
ax2.set_title("Total Blocks Analyzed", fontsize=12, fontweight="bold")
ax2.set_ylabel("Block Count")
ax2.bar_label(bars2, padding=3, fontsize=10)
ax2.grid(axis="y", linestyle="--", alpha=0.4)

plt.suptitle("Cyclomatic Complexity Comparison", fontsize=13)
plt.tight_layout()
plt.savefig("results/chart_3_cyclomatic.png", dpi=150)
plt.close()
print("✅ chart_3_cyclomatic.png kaydedildi")


# ════════════════════════════════════════════════════════
# GRAFİK 4 — Maintainability Index (stacked bar + lowest)
# ════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Sol: grade dağılımı (stacked)
grade_a = [mi_data["Grade A"][0], mi_data["Grade A"][1]]
grade_b = [mi_data["Grade B"][0], mi_data["Grade B"][1]]
grade_c = [mi_data["Grade C"][0], mi_data["Grade C"][1]]

ax1.bar(projects, grade_a, label="Grade A", color="#43a047", alpha=0.85)
ax1.bar(projects, grade_b, bottom=grade_a, label="Grade B", color="#fb8c00", alpha=0.85)
ax1.bar(projects, grade_c,
        bottom=[grade_a[i] + grade_b[i] for i in range(2)],
        label="Grade C", color="#e53935", alpha=0.85)
ax1.set_title("MI Grade Distribution", fontsize=12, fontweight="bold")
ax1.set_ylabel("File Count")
ax1.legend()
ax1.grid(axis="y", linestyle="--", alpha=0.4)

# Sağ: en düşük MI skoru
bars3 = ax2.bar(projects, mi_data["Lowest"],
                color=[FLASK_COLOR, FASTAPI_COLOR], alpha=0.85, width=0.4)
ax2.set_title("Lowest MI Score per Project", fontsize=12, fontweight="bold")
ax2.set_ylabel("MI Score")
ax2.set_ylim(0, 30)
ax2.bar_label(bars3, padding=3, fontsize=10)
ax2.axhline(y=10, color="red", linestyle="--", alpha=0.5, label="Grade C threshold")
ax2.legend(fontsize=8)
ax2.grid(axis="y", linestyle="--", alpha=0.4)

plt.suptitle("Maintainability Index Comparison", fontsize=13)
plt.tight_layout()
plt.savefig("results/chart_4_maintainability.png", dpi=150)
plt.close()
print("✅ chart_4_maintainability.png kaydedildi")

print("\n🎉 Tüm grafikler 'results/' klasörüne kaydedildi!")