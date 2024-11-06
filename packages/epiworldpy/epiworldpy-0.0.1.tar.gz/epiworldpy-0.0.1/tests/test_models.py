import epiworldpy as epiworld

# TODO: Decide the right way to validate data; how often is the underlying C++
# simulation code changed in a way that will change outputs here? What's the
# tradeoff?

def test_diffnet_simple():
    # TODO: How do we invoke this model?
    pass

def test_seir_simple():
    # TODO: Implement `agents_from_adjlist` or something similar.
    pass

def test_seirconn_simple():
    covid19 = epiworld.ModelSEIRCONN(
        name              = 'covid-19',
        n                 = 10000,
        prevalence        = .01,
        contact_rate      = 2.0,
        transmission_rate = .1,
        incubation_days   = 7.0,
        recovery_rate     = 0.14
    )

    covid19.run(100, 223)

def test_seird_simple():
    # TODO: Implement `agents_from_adjlist` or something similar.
    pass

def test_sir_simple():
    # TODO: Implement `agents_from_adjlist` or something similar.
    pass

def test_sirconn_simple():
    covid19 = epiworld.ModelSIRCONN(
        name              = 'covid-19',
        n                 = 10000,
        prevalence        = .01,
        contact_rate      = 2.0,
        transmission_rate = .1,
        recovery_rate     = 0.14
    )

    covid19.run(100, 223)

def test_sird_simple():
    # TODO: Implement `agents_from_adjlist` or something similar.
    pass

def test_sirdconn_simple():
    covid19 = epiworld.ModelSIRDCONN(
        name              = 'covid-19',
        n                 = 10000,
        prevalence        = .01,
        contact_rate      = 2.0,
        transmission_rate = .1,
        recovery_rate     = 0.14,
        death_rate        = 0.1,
    )

    covid19.run(100, 223)

def test_sis_simple():
    # TODO: Implement `agents_from_adjlist` or something similar.
    pass

def test_sisd_simple():
    # TODO: Implement `agents_from_adjlist` or something similar.
    pass

def test_surv_simple():
    # TODO: Implement `agents_from_adjlist` or something similar.
    pass
