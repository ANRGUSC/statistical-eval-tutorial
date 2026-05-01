"""
figures.py - generate every figure in stateval.tex from a single FIFO vs SRPT
simulation. The tutorial is self-reproducing: rerunning this script regenerates
every figure used in the paper.

Usage (from the repo root):
    python code/figures.py             # writes PDFs to paper/figs/

Or from inside code/:
    cd code && python figures.py       # same effect, resolves ../paper/figs/

Dependencies: numpy, scipy, matplotlib.
Tested on Python 3.12, numpy 2.x, scipy 1.17, matplotlib 3.10.
"""

from __future__ import annotations
import os
from dataclasses import dataclass

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

# Resolve paper/figs/ relative to this file, so the script works whether it is
# invoked from the repo root or from inside code/.
HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.normpath(os.path.join(HERE, "..", "paper", "figs"))
os.makedirs(FIGDIR, exist_ok=True)

# Consistent figure styling.
plt.rcParams.update({
    "figure.figsize": (5.0, 3.2),
    "figure.dpi": 120,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
    "legend.frameon": False,
})


# ---------------------------------------------------------------------------
# Single-server queue simulator with FIFO and SRPT policies.
# ---------------------------------------------------------------------------

@dataclass
class RunResult:
    completion_times: np.ndarray  # one entry per completed job
    arrivals: np.ndarray          # arrival times (same length)
    sizes: np.ndarray             # service requirements


def simulate(policy: str, rho: float, n_jobs: int, pareto_alpha: float,
             rng: np.random.Generator, x_max: float = 1e3) -> RunResult:
    """Single-server queue with Poisson arrivals and truncated-Pareto job sizes.

    Service rate is normalized to 1; arrival rate = rho. Pareto sizes use the
    Lomax form with shape `pareto_alpha`, truncated at `x_max` so the variance
    is finite even for alpha <= 2 (M/G/1 mean response time then exists).
    """
    if policy not in ("FIFO", "SRPT"):
        raise ValueError(policy)

    # Truncated Pareto. x_m is chosen so the *truncated* mean is 1, so rho
    # remains the offered load.
    x_m_un = (pareto_alpha - 1) / pareto_alpha
    raw = x_m_un / (1 - rng.random(n_jobs)) ** (1 / pareto_alpha)
    sizes = np.minimum(raw, x_max)
    # Renormalize so the truncated sample mean is ~1 (preserves rho semantics).
    sizes = sizes / sizes.mean()

    # Poisson arrivals with rate rho (mean service = 1, so rho = arrival rate).
    interarrivals = rng.exponential(1.0 / rho, n_jobs)
    arrivals = np.cumsum(interarrivals)

    completion_times = np.empty(n_jobs)

    if policy == "FIFO":
        # Closed-form for FIFO at a single server: completion[i] = max(arrival[i],
        # completion[i-1]) + size[i].
        t = 0.0
        for i in range(n_jobs):
            t = max(arrivals[i], t) + sizes[i]
            completion_times[i] = t
        return RunResult(completion_times - arrivals, arrivals, sizes)

    # SRPT: simulate via event-driven loop. At each event (arrival or completion)
    # the server processes the job with the smallest *remaining* work.
    remaining = sizes.copy()
    completed = np.zeros(n_jobs, dtype=bool)
    in_system_idx = []  # indices currently in the system
    next_arrival = 0
    now = 0.0
    last_event = 0.0
    current = -1  # currently served job

    while next_arrival < n_jobs or in_system_idx:
        # Time of next arrival (inf if none left).
        t_arr = arrivals[next_arrival] if next_arrival < n_jobs else np.inf
        # Time of next completion (inf if server idle).
        t_comp = now + remaining[current] if current >= 0 else np.inf
        t_event = min(t_arr, t_comp)

        # Advance work on current job.
        if current >= 0:
            remaining[current] -= (t_event - now)
            remaining[current] = max(remaining[current], 0.0)
        now = t_event

        if t_arr <= t_comp:
            # Arrival event.
            in_system_idx.append(next_arrival)
            next_arrival += 1
        else:
            # Completion event.
            completion_times[current] = now
            completed[current] = True
            in_system_idx.remove(current)
            current = -1

        # Choose next job to serve (smallest remaining).
        if in_system_idx:
            current = min(in_system_idx, key=lambda i: remaining[i])

    return RunResult(completion_times - arrivals, arrivals, sizes)


def run_seeds(policy: str, rho: float, seeds: range, n_jobs: int = 5000,
              pareto_alpha: float = 1.5) -> np.ndarray:
    """Return array of per-seed mean latencies."""
    out = np.empty(len(seeds))
    for i, s in enumerate(seeds):
        rng = np.random.default_rng(s)
        r = simulate(policy, rho, n_jobs, pareto_alpha, rng)
        # Discard a warmup window.
        warmup = n_jobs // 5
        out[i] = r.completion_times[warmup:].mean()
    return out


# ---------------------------------------------------------------------------
# Figure 1: latency CDF for FIFO vs SRPT at a single load.
# ---------------------------------------------------------------------------

def fig_latency_cdf():
    rng = np.random.default_rng(42)
    rho = 0.8
    n_jobs = 20000
    fifo = simulate("FIFO", rho, n_jobs, 1.5, np.random.default_rng(42))
    srpt = simulate("SRPT", rho, n_jobs, 1.5, np.random.default_rng(42))
    warm = n_jobs // 5
    fifo_lat = np.sort(fifo.completion_times[warm:])
    srpt_lat = np.sort(srpt.completion_times[warm:])

    fig, ax = plt.subplots()
    ccdf = lambda x: 1 - np.arange(1, len(x) + 1) / len(x)
    ax.loglog(fifo_lat, ccdf(fifo_lat), label="FIFO", lw=1.6)
    ax.loglog(srpt_lat, ccdf(srpt_lat), label="SRPT", lw=1.6)
    ax.set_xlabel("Job completion latency")
    ax.set_ylabel(r"$P(\mathrm{latency} > x)$")
    ax.legend()
    ax.grid(True, which="both", alpha=0.25)
    fig.savefig(f"{FIGDIR}/latency_cdf.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2: bootstrap distribution of mean-latency improvement.
# ---------------------------------------------------------------------------

def fig_bootstrap():
    seeds = range(30)
    rho = 0.8
    fifo = run_seeds("FIFO", rho, seeds)
    srpt = run_seeds("SRPT", rho, seeds)
    diff = fifo - srpt  # positive => SRPT improves

    rng = np.random.default_rng(7)
    n_boot = 10000
    boots = np.empty(n_boot)
    n = len(diff)
    for i in range(n_boot):
        idx = rng.integers(0, n, n)
        boots[i] = diff[idx].mean()
    lo, hi = np.quantile(boots, [0.025, 0.975])
    obs = diff.mean()

    fig, ax = plt.subplots()
    ax.hist(boots, bins=50, color="steelblue", alpha=0.85)
    ax.axvline(obs, color="black", lw=1.5, label=f"observed mean = {obs:.2f}")
    ax.axvline(lo, color="firebrick", lw=1.2, ls="--", label="95% CI")
    ax.axvline(hi, color="firebrick", lw=1.2, ls="--")
    ax.set_xlabel("Mean latency reduction (FIFO - SRPT)")
    ax.set_ylabel("Bootstrap frequency")
    ax.legend()
    fig.savefig(f"{FIGDIR}/bootstrap.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3: error bars done wrong vs right (SE vs 95% CI).
# ---------------------------------------------------------------------------

def fig_error_bars():
    seeds = range(30)
    rho = 0.8
    fifo = run_seeds("FIFO", rho, seeds)
    srpt = run_seeds("SRPT", rho, seeds)

    means = [fifo.mean(), srpt.mean()]
    sd = [fifo.std(ddof=1), srpt.std(ddof=1)]
    se = [s / np.sqrt(len(fifo)) for s in sd]

    # Bootstrap 95% CI on each.
    rng = np.random.default_rng(11)
    def boot_ci(x):
        boots = np.array([x[rng.integers(0, len(x), len(x))].mean()
                          for _ in range(5000)])
        return np.quantile(boots, [0.025, 0.975])
    fifo_ci = boot_ci(fifo)
    srpt_ci = boot_ci(srpt)
    ci_low = [means[0] - fifo_ci[0], means[1] - srpt_ci[0]]
    ci_high = [fifo_ci[1] - means[0], srpt_ci[1] - means[1]]

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2), sharey=True)
    x = [0, 1]
    labels = ["FIFO", "SRPT"]

    axes[0].bar(x, means, yerr=se, capsize=6, color=["#888", "#4477AA"])
    axes[0].set_xticks(x); axes[0].set_xticklabels(labels)
    axes[0].set_ylabel("Mean latency")
    axes[0].set_title("SE bars (misleading)")

    axes[1].bar(x, means, yerr=[ci_low, ci_high], capsize=6,
                color=["#888", "#4477AA"])
    axes[1].set_xticks(x); axes[1].set_xticklabels(labels)
    axes[1].set_title("95% bootstrap CI")

    fig.savefig(f"{FIGDIR}/error_bars.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4: factorial interaction plot (load x policy).
# ---------------------------------------------------------------------------

def fig_interaction():
    loads = [0.3, 0.5, 0.7, 0.9]
    seeds = range(20)
    fifo_means = []
    srpt_means = []
    fifo_cis = []
    srpt_cis = []

    rng = np.random.default_rng(99)
    def boot_ci(x):
        boots = np.array([x[rng.integers(0, len(x), len(x))].mean()
                          for _ in range(2000)])
        return np.quantile(boots, [0.025, 0.975])

    for rho in loads:
        f = run_seeds("FIFO", rho, seeds)
        s = run_seeds("SRPT", rho, seeds)
        fifo_means.append(f.mean()); srpt_means.append(s.mean())
        fifo_cis.append(boot_ci(f)); srpt_cis.append(boot_ci(s))

    fifo_means = np.array(fifo_means); srpt_means = np.array(srpt_means)
    fifo_cis = np.array(fifo_cis); srpt_cis = np.array(srpt_cis)

    fig, ax = plt.subplots()
    ax.errorbar(loads, fifo_means,
                yerr=[fifo_means - fifo_cis[:,0], fifo_cis[:,1] - fifo_means],
                marker="o", capsize=4, label="FIFO", lw=1.6)
    ax.errorbar(loads, srpt_means,
                yerr=[srpt_means - srpt_cis[:,0], srpt_cis[:,1] - srpt_means],
                marker="s", capsize=4, label="SRPT", lw=1.6)
    ax.set_xlabel(r"Offered load $\rho$")
    ax.set_ylabel("Mean latency")
    ax.set_yscale("log")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.savefig(f"{FIGDIR}/interaction.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 5: sample-size / power curve.
# ---------------------------------------------------------------------------

def fig_power():
    # Compute power to detect a difference of size delta (in units of paired-
    # difference SD) at alpha = 0.05, two-sided, paired Wilcoxon approximated by
    # the t-test power formula (sufficient for guidance).
    from scipy.stats import norm
    alpha = 0.05
    z_alpha = norm.ppf(1 - alpha / 2)
    ns = np.arange(3, 80)
    deltas = [0.2, 0.5, 0.8]  # small / medium / large effect (Cohen's d)

    fig, ax = plt.subplots()
    for d in deltas:
        ncp = d * np.sqrt(ns)
        power = 1 - norm.cdf(z_alpha - ncp) + norm.cdf(-z_alpha - ncp)
        ax.plot(ns, power, lw=1.6, label=f"effect size d={d}")
    ax.axhline(0.8, color="gray", ls="--", lw=1.0, label="conventional 80% power")
    ax.set_xlabel("Number of seeds (paired)")
    ax.set_ylabel("Power")
    ax.set_ylim(0, 1.02)
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.savefig(f"{FIGDIR}/power.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 6: box plot vs violin plot, FIFO vs SRPT per-seed mean latencies.
# ---------------------------------------------------------------------------

def fig_box_violin():
    seeds = range(40)
    rho = 0.8
    fifo = run_seeds("FIFO", rho, seeds)
    srpt = run_seeds("SRPT", rho, seeds)
    data = [fifo, srpt]
    labels = ["FIFO", "SRPT"]

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.4), sharey=True)

    # Box plot.
    bp = axes[0].boxplot(data, labels=labels, patch_artist=True,
                         medianprops=dict(color="black", lw=1.5),
                         flierprops=dict(marker="o", markersize=4))
    for patch, c in zip(bp["boxes"], ["#cccccc", "#7faed5"]):
        patch.set_facecolor(c)
    axes[0].set_ylabel("Per-seed mean latency")
    axes[0].set_yscale("log")
    axes[0].set_title("Box plot")

    # Violin plot with overlaid points.
    parts = axes[1].violinplot(data, showmedians=True)
    for pc, c in zip(parts["bodies"], ["#cccccc", "#7faed5"]):
        pc.set_facecolor(c)
        pc.set_alpha(0.85)
    rng = np.random.default_rng(3)
    for i, x in enumerate(data, start=1):
        jitter = rng.uniform(-0.07, 0.07, size=len(x))
        axes[1].scatter(np.full_like(x, i) + jitter, x, s=10, color="black",
                        alpha=0.6)
    axes[1].set_xticks([1, 2]); axes[1].set_xticklabels(labels)
    axes[1].set_yscale("log")
    axes[1].set_title("Violin plot (with seeds)")

    fig.savefig(f"{FIGDIR}/box_violin.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Headline numbers (printed for use in the paper text).
# ---------------------------------------------------------------------------

def headline_numbers():
    seeds = range(30)
    print("\nHeadline numbers (for sanity-checking text claims):")
    for rho in [0.3, 0.5, 0.7, 0.9]:
        f = run_seeds("FIFO", rho, seeds)
        s = run_seeds("SRPT", rho, seeds)
        diff = f - s
        rel = diff / f * 100
        wstat, pval = stats.wilcoxon(f, s)
        print(f"  rho={rho}: FIFO={f.mean():.2f} SRPT={s.mean():.2f} "
              f"reduction={rel.mean():.1f}% Wilcoxon p={pval:.3g}")


def main():
    fig_latency_cdf()
    fig_bootstrap()
    fig_error_bars()
    fig_interaction()
    fig_power()
    fig_box_violin()
    headline_numbers()
    print(f"\nWrote figures to {FIGDIR}/")


if __name__ == "__main__":
    main()
