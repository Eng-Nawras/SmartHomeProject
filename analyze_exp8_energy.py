"""Analyze Experiment 8 radio energy from recorded OMNeT++ power vectors."""

from pathlib import Path
import re
import pandas as pd

RESULTS = Path("results")
SIM_TIME_S = 60.0

STATE_POWERS_W = {
    "sleep_or_off": 0.0,
    "idle_or_cca": 0.00128,
    "switching": 0.0300,
    "transmit": 0.0522,
    "receive": 0.0591,
}


def state_for_power(power_w):
    return min(
        STATE_POWERS_W,
        key=lambda state: abs(power_w - STATE_POWERS_W[state])
    )


def find_radio_vectors(vector_file):
    pattern = re.compile(
        r"vector (\d+) SmartHomeNetwork\.([^.]+)"
        r"\.wlan\[0\]\.radio\.energyConsumer "
        r"powerConsumption:vector ETV$"
    )

    vectors = {}

    for line in vector_file.read_text().splitlines():
        match = pattern.match(line)
        if match:
            vectors[match.group(2)] = match.group(1)

    return vectors


def read_vector_samples(vector_file, vector_id):
    samples = []

    for line in vector_file.read_text().splitlines():
        if line.startswith(vector_id + "\t"):
            fields = line.split()

            if len(fields) >= 3:
                samples.append(
                    (float(fields[-2]), float(fields[-1]))
                )

    if not samples:
        raise RuntimeError(
            f"No samples found for vector {vector_id}"
        )

    return pd.DataFrame(
        samples,
        columns=["vectime", "vecvalue"]
    )


def integrate_run(samples):
    samples = (
        samples
        .sort_values("vectime")
        .groupby("vectime", as_index=False)
        .last()
    )

    samples["next_time"] = (
        samples["vectime"]
        .shift(-1)
        .fillna(SIM_TIME_S)
    )

    samples["duration_s"] = (
        samples["next_time"] - samples["vectime"]
    ).clip(lower=0)

    samples["state"] = samples["vecvalue"].map(
        state_for_power
    )

    result = {
        f"{state}_time_s": 0.0
        for state in STATE_POWERS_W
    }

    result.update({
        f"{state}_energy_mJ": 0.0
        for state in STATE_POWERS_W
    })

    for state, group in samples.groupby("state"):
        result[f"{state}_time_s"] = (
            group["duration_s"].sum()
        )

        result[f"{state}_energy_mJ"] = (
            group["duration_s"] * group["vecvalue"]
        ).sum() * 1000.0

    result["observed_radio_energy_mJ"] = sum(
        value
        for key, value in result.items()
        if key.endswith("_energy_mJ")
    )

    result["integrated_time_s"] = sum(
        result[f"{state}_time_s"]
        for state in STATE_POWERS_W
    )

    return result


def read_residual_energy(sca_file, node):
    pattern = re.compile(
        rf"scalar SmartHomeNetwork\.{re.escape(node)}"
        rf"\.energyStorage residualEnergyCapacity:last (.+)$"
    )

    for line in sca_file.read_text().splitlines():
        match = pattern.match(line)

        if match:
            return float(match.group(1))

    return float("nan")


def main():
    vector_files = sorted(
        RESULTS.glob("Exp8_AdvancedEnergy-#*.vec")
    )

    if not vector_files:
        raise SystemExit(
            "No Exp8 vector files found."
        )

    rows = []

    for vector_file in vector_files:
        sca_file = vector_file.with_suffix(".sca")
        vectors = find_radio_vectors(vector_file)

        print(
            f"{vector_file.name}: "
            f"{len(vectors)} radio devices found"
        )

        for node, vector_id in sorted(vectors.items()):
            samples = read_vector_samples(
                vector_file,
                vector_id
            )

            result = integrate_run(samples)

            residual = read_residual_energy(
                sca_file,
                node
            )

            rows.append({
                "node": node,
                "run": vector_file.stem,
                **result,
                "residual_energy_J": residual,
            })

    data = pd.DataFrame(rows)

    if data.empty:
        raise SystemExit(
            "No energy data was extracted."
        )

    summary = (
        data
        .groupby("node", as_index=False)
        .mean(numeric_only=True)
        .sort_values("node")
    )

    summary["radio_energy_J"] = (
        summary["observed_radio_energy_mJ"] / 1000.0
    )

    summary["radio_energy_per_second_mJ"] = (
        summary["observed_radio_energy_mJ"]
        / SIM_TIME_S
    )

    output = RESULTS / "exp8_energy_summary.csv"
    summary.to_csv(output, index=False)

    print()
    print("=" * 100)
    print("EXPERIMENT 8 - ADVANCED ENERGY ANALYSIS")
    print("=" * 100)

    print(
        summary[
            [
                "node",
                "observed_radio_energy_mJ",
                "radio_energy_J",
                "transmit_energy_mJ",
                "receive_energy_mJ",
                "idle_or_cca_energy_mJ",
                "switching_energy_mJ",
                "residual_energy_J",
            ]
        ]
        .round(4)
        .to_string(index=False)
    )

    print()
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
