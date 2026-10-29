"""
Uber Trip Data Analysis
-----------------------
Cleans one year (2016) of Uber trip logs and answers:
  1. What are trips used for, and how far do they go?
  2. When is demand highest (time of day, weekday, month)?
  3. Which trip purposes drive the longest distances?

Run from the repository root:
    python src/uber_analysis.py
Charts are saved to screenshots/.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "UberDataset.csv"
OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)

# ---------- chart style ----------
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#c9c8c3"
INK, MUTED = "#0b0b0b", "#52514e"
plt.rcParams.update({
    "figure.dpi": 150, "savefig.bbox": "tight", "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": GREY, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.titleweight": "bold", "axes.titlesize": 12,
    "axes.titlecolor": INK, "axes.grid": True, "grid.color": "#ecebe8",
    "axes.axisbelow": True,
})


def highlight(values, top_n=1):
    """Blue for the top bar(s), grey for the rest, so the answer stands out."""
    order = np.argsort(values)[::-1][:top_n]
    return [BLUE if i in order else GREY for i in range(len(values))]


def save(fig, name):
    fig.savefig(OUT / name)
    plt.close(fig)
    print(f"saved screenshots/{name}")


# ---------- 1. load ----------
raw = pd.read_csv(DATA)
print(f"Raw rows: {len(raw)}")

# ---------- 2. clean ----------
df = raw.copy()
# The last row is a 'Totals' summary line, not a trip.
df = df[df["START_DATE"] != "Totals"]
# Missing purpose means the rider did not record one - keep the trip, label it.
df["PURPOSE"] = df["PURPOSE"].fillna("Not recorded")
# Dates come in two formats (01-13-2016 13:00 and 1/13/2016 13:00).
# format="mixed" parses both; the default parser silently turns one format into NaT,
# which would drop about 735 of the 1,155 trips.
df["START_DATE"] = pd.to_datetime(df["START_DATE"], format="mixed", errors="coerce")
df["END_DATE"] = pd.to_datetime(df["END_DATE"], format="mixed", errors="coerce")
df = df.dropna(subset=["START_DATE", "END_DATE", "CATEGORY", "MILES"])
df = df.drop_duplicates()
print(f"Clean trips: {len(df)}")

# ---------- 3. feature engineering ----------
df["hour"] = df["START_DATE"].dt.hour
df["time_of_day"] = pd.cut(
    df["hour"], bins=[-1, 10, 15, 19, 24],
    labels=["Morning (0-10)", "Afternoon (11-15)", "Evening (16-19)", "Night (20-23)"],
)
df["weekday"] = df["START_DATE"].dt.day_name()
df["month"] = df["START_DATE"].dt.month
df["duration_min"] = (df["END_DATE"] - df["START_DATE"]).dt.total_seconds() / 60

# ---------- 4. charts ----------
# 4.1 Trips by purpose
purpose = df["PURPOSE"].value_counts().sort_values()
fig, ax = plt.subplots(figsize=(8, 5))
colors = [GREY if p == "Not recorded" else BLUE for p in purpose.index]
ax.barh(purpose.index, purpose.values, color=colors)
ax.set_title("Meetings and meals are the most common recorded purposes")
ax.set_xlabel("Number of trips")
ax.grid(axis="y", visible=False)
for y, v in enumerate(purpose.values):
    ax.text(v + 5, y, str(v), va="center", color=MUTED, fontsize=8)
save(fig, "trips_by_purpose.png")

# 4.2 Trips by time of day
tod = df["time_of_day"].value_counts().reindex(df["time_of_day"].cat.categories)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(tod.index.astype(str), tod.values, color=highlight(tod.values))
ax.set_title("Afternoon is the busiest time of day")
ax.set_ylabel("Number of trips")
ax.grid(axis="x", visible=False)
for x, v in enumerate(tod.values):
    ax.text(x, v + 5, f"{v / tod.sum():.0%}", ha="center", color=MUTED, fontsize=9)
save(fig, "trips_by_time_of_day.png")

# 4.3 Trips by weekday
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wd = df["weekday"].value_counts().reindex(days)
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar([d[:3] for d in days], wd.values, color=highlight(wd.values))
ax.set_title("Friday has the most trips")
ax.set_ylabel("Number of trips")
ax.grid(axis="x", visible=False)
save(fig, "trips_by_weekday.png")

# 4.4 Trips by month
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
mt = df["month"].value_counts().reindex(range(1, 13), fill_value=0)
fig, ax = plt.subplots(figsize=(8, 4))
colors = [BLUE if v == mt.max() else ORANGE if v == mt.min() else GREY for v in mt.values]
ax.bar(months, mt.values, color=colors)
ax.set_title("December is the busiest month, September the quietest")
ax.set_ylabel("Number of trips")
ax.grid(axis="x", visible=False)
save(fig, "trips_by_month.png")

# 4.5 Longest trip per month
mx = df.groupby("month")["MILES"].max().reindex(range(1, 13))
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(months, mx.values, color=BLUE, lw=2, marker="o", ms=6)
ax.set_title("Longest single trip each month (miles)")
ax.set_ylabel("Miles")
peak = int(np.argmax(mx.values))
ax.annotate(f"{mx.values[peak]:.0f} mi", (peak, mx.values[peak]),
            textcoords="offset points", xytext=(8, 0), color=INK, fontsize=9)
save(fig, "longest_trip_by_month.png")

# 4.6 Distance distribution
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df.loc[df["MILES"] < 40, "MILES"], bins=40, color=BLUE, edgecolor="white")
ax.axvline(df["MILES"].median(), color=ORANGE, lw=2)
ax.text(df["MILES"].median() + 0.5, ax.get_ylim()[1] * 0.9,
        f"median {df['MILES'].median():.1f} mi", color=INK, fontsize=9)
ax.set_title("Most trips are short (trips under 40 miles shown)")
ax.set_xlabel("Miles per trip")
ax.set_ylabel("Number of trips")
save(fig, "trip_distance_distribution.png")

# 4.7 Average distance by purpose (purposes with 10+ trips)
pm = df.groupby("PURPOSE")["MILES"].agg(["mean", "count"])
pm = pm[pm["count"] >= 10].sort_values("mean")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(pm.index, pm["mean"], color=highlight(pm["mean"].values))
ax.set_title("Customer visits are the longest trips on average")
ax.set_xlabel("Average miles per trip (purposes with 10+ trips)")
ax.grid(axis="y", visible=False)
for y, v in enumerate(pm["mean"]):
    ax.text(v + 0.3, y, f"{v:.1f}", va="center", color=MUTED, fontsize=8)
save(fig, "avg_distance_by_purpose.png")

# 4.8 Correlation matrix after one-hot encoding CATEGORY and PURPOSE
encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
encoded = pd.DataFrame(
    encoder.fit_transform(df[["CATEGORY", "PURPOSE"]]),
    columns=encoder.get_feature_names_out(), index=df.index,
)
numeric = pd.concat([df[["MILES", "hour", "duration_min"]], encoded], axis=1)
keep = ["MILES", "hour", "duration_min"] + [
    c for c in encoded.columns if encoded[c].sum() >= 10
]
corr = numeric[keep].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, cmap="RdBu_r", center=0, vmin=-1, vmax=1, annot=True, fmt=".2f",
            annot_kws={"size": 7}, linewidths=1, linecolor="white", ax=ax,
            cbar_kws={"shrink": 0.7})
ax.set_title("Correlation of distance, time and encoded trip type")
save(fig, "correlation_matrix.png")

# ---------- 5. summary numbers used in the README ----------
print("\n--- Summary ---")
print(f"Total miles: {df['MILES'].sum():,.0f}")
print(f"Business share of trips: {(df['CATEGORY'] == 'Business').mean():.1%}")
print(f"Purpose not recorded: {(df['PURPOSE'] == 'Not recorded').mean():.1%}")
print(f"Median trip: {df['MILES'].median():.1f} mi, under 10 mi: {(df['MILES'] < 10).mean():.1%}")
print(f"Correlation miles vs duration: {df['MILES'].corr(df['duration_min']):.2f}")
print("Trips by time of day:", (tod / tod.sum()).round(3).to_dict())
print("Trips by weekday:", wd.to_dict())
print("Trips by month:", dict(zip(months, mt.values)))
