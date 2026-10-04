from score import (
    LocusFeatures,
    HIGH_RISK_THRESHOLD,
    leakage_guard,
    score,
    high_risk,
    reference_sensitive,
    severe_reference_sensitive,
)


def run():
    clean = LocusFeatures(gene="SAFE")
    assert score(clean) == 0
    assert not high_risk(clean)

    maxed = LocusFeatures(
        gene="COMPLEX",
        segdup_fraction=0.40,
        lowmap_fraction=0.30,
        high_identity_paralog=True,
        confirmed_copy_mismatch=True,
        reference_representation_discordance=True,
        predictor_source_versions=("pre-v5.0q-source",),
    )
    assert score(maxed) == 7
    assert HIGH_RISK_THRESHOLD == 5
    assert high_risk(maxed)

    mid = LocusFeatures(
        gene="MID",
        segdup_fraction=0.10,
        lowmap_fraction=0.10,
        structural_variability=True,
    )
    assert score(mid) == 3

    assert reference_sensitive(0.90, 0.79)
    assert not reference_sensitive(0.90, 0.81)
    assert severe_reference_sensitive(0.95, 0.65)
    assert not severe_reference_sensitive(0.95, 0.71)

    leakage_guard(["gene", "segdup_fraction", "lowmap_fraction"])
    rejected = 0
    for bad in [
        "benchmark_status",
        "cmrg_included_flag",
        "HG002_v5q_coverage",
        "manual_curation_result",
        "truth_label",
        "target_value",
        "recall",
        "f1_score",
    ]:
        try:
            leakage_guard(["gene", bad])
        except ValueError:
            rejected += 1
    assert rejected == 8

    for bad_fraction in (-0.01, 1.01):
        try:
            score(LocusFeatures(gene="BAD", segdup_fraction=bad_fraction))
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid fraction was accepted")

    print("RSC v0.2 self-test PASS: frozen scoring, outcome thresholds, and leakage guard verified")


if __name__ == "__main__":
    run()
