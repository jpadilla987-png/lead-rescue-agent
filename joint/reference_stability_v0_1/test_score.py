from score import LocusFeatures, high_risk, holdout_gene, score


def test_score_bounds_and_threshold():
    simple = LocusFeatures(gene="SAFE")
    assert score(simple) == 0
    assert not high_risk(simple)

    complex_locus = LocusFeatures(
        gene="COMPLEX",
        segdup_fraction=0.40,
        lowmap_fraction=0.30,
        high_identity_paralog=True,
        confirmed_copy_mismatch=True,
        reference_representation_discordance=True,
    )
    assert score(complex_locus) == 7
    assert high_risk(complex_locus)


def test_intermediate_scoring():
    x = LocusFeatures(
        gene="MID",
        segdup_fraction=0.10,
        lowmap_fraction=0.10,
        structural_variability=True,
    )
    assert score(x) == 3
    assert not high_risk(x)


def test_split_is_deterministic():
    genes = ["PMS2", "SMN1", "CYP2D6", "PKD1", "CBS"]
    first = [holdout_gene(g) for g in genes]
    second = [holdout_gene(g.lower()) for g in genes]
    assert first == second


def test_invalid_fraction_rejected():
    try:
        score(LocusFeatures(gene="BAD", segdup_fraction=1.1))
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
