import pandas as pd
from math import sqrt

# correction factors
GALE_MGO = 11.844
MODEL_EARTH_MGO = 7.652
MGO_CORRECTION_FACTOR = GALE_MGO / MODEL_EARTH_MGO

# oxide numbers
oxide_cations = {
    'mgo': 1.0,
    'sio2': 1.0,
    'feo': 1.0,
    'fe2o3': 2.0,
    'al2o3': 2.0,
    'nao2': 1.0,
    'cao2': 1.0,
    'tio2': 1.0
}
oxide_anions = {
    'mgo': 1.0,
    'sio2': 2.0,
    'feo': 1.0,
    'fe2o3': 3.0,
    'al2o3': 3.0,
    'nao2': 2.0,
    'cao2': 2.0,
    'tio2': 2.0
}

# molar masses
atomic_masses = {
    'mg': 24.305,
    'si': 28.086,
    'fe': 55.845,
    'al': 26.982,
    'na': 22.99,
    'ca': 40.078,
    'ti': 47.867,
    'o': 16.0
}
oxide_masses = {
    'mgo': (atomic_masses['mg'] * oxide_cations['mgo']) + (atomic_masses['o'] * oxide_anions['mgo']),
    'sio2': (atomic_masses['si'] * oxide_cations['sio2']) + (atomic_masses['o'] * oxide_anions['sio2']),
    'feo': (atomic_masses['fe'] * oxide_cations['feo']) + (atomic_masses['o'] * oxide_anions['feo']),
    'fe2o3': (atomic_masses['fe'] * oxide_cations['fe2o3']) + (atomic_masses['o'] * oxide_anions['fe2o3']),
    'al2o3': (atomic_masses['al'] * oxide_cations['al2o3']) + (atomic_masses['o'] * oxide_anions['al2o3']),
    'nao2': (atomic_masses['na'] * oxide_cations['nao2']) + (atomic_masses['o'] * oxide_anions['nao2']),
    'cao2': (atomic_masses['ca'] * oxide_cations['cao2']) + (atomic_masses['o'] * oxide_anions['cao2']),
    'tio2': (atomic_masses['ti'] * oxide_cations['tio2']) + (atomic_masses['o'] * oxide_anions['tio2'])
}


def calculated_morb_to_original(oxide_weights):

    # this value needs to be removed from BSP
    original_oxide_wt_mgo = oxide_weights['mgo'] / MGO_CORRECTION_FACTOR


def normalize_compositions(oxide_wt_pct_unnormalized):
    normalized = {}
    oxides = list(oxide_wt_pct_unnormalized.keys())
    sum_total = 0
    for i in oxides:
        sum_total += oxide_wt_pct_unnormalized[i]
    for i in oxides:
        normalized.update({i: (float(oxide_wt_pct_unnormalized[i]) / float(sum_total)) * 100.0})

    return normalized

def moles_from_oxide_wt_pct(oxide_wt_pct):
    oxide_moles = {}
    oxides = list(oxide_wt_pct.keys())
    for i in oxides:
        oxide_moles.update({i: oxide_wt_pct[i] / oxide_masses[i]})

    return oxide_moles

def calc_morb_moles_extracted(morb_mass_fraction, normalized_morb_wt_pct):
    moles = {}
    oxides = list(normalized_morb_wt_pct.keys())
    for i in oxides:
        moles.update({i: (morb_mass_fraction / 100.0) * (normalized_morb_wt_pct[i] / oxide_masses[i])})

    return moles

def calc_bsp_morb_moles_difference(moles_bsp, moles_morb_extracted):
    diff = {}
    pct_change = {}
    oxides = list(moles_bsp.keys())
    for i in oxides:
        m_bsp = moles_bsp[i]
        m_morb = moles_morb_extracted[i]
        d = m_bsp - m_morb
        p = 100.0 - (100.0 * (d / m_bsp))
        diff.update({i: d})
        pct_change.update({i: p})

    return diff, pct_change

def calc_bsp_mob_wt_difference(bsp_morb_moles_difference):
    diff = {}
    oxides = list(bsp_morb_moles_difference.keys())
    for i in oxides:
        wt = bsp_morb_moles_difference[i] * oxide_masses[i]
        diff.update({i: wt})

    return diff

def calc_depleted_mantle_composition(differences):
    comp = {}
    oxides = list(differences.keys())
    sum_total = 0
    for i in oxides:
        sum_total += differences[i]
    for i in oxides:
        comp.update({i: 100.0 * (differences[i] / sum_total)})
    return comp

def calc_depleted_lith(bsp_oxide_wt_pct, morb_oxide_wt_pct, morb_mass_fraction):

    normalized_bsp_oxide_wt_pct = normalize_compositions(oxide_wt_pct_unnormalized=bsp_oxide_wt_pct)
    normalized_morb_oxide_wt_pct = normalize_compositions(oxide_wt_pct_unnormalized=morb_oxide_wt_pct)
    moles_bsp = moles_from_oxide_wt_pct(oxide_wt_pct=normalized_bsp_oxide_wt_pct)
    moles_morb_extracted = calc_morb_moles_extracted(morb_mass_fraction=morb_mass_fraction, normalized_morb_wt_pct=normalized_morb_oxide_wt_pct)
    bsp_morb_moles_difference, pct_change = calc_bsp_morb_moles_difference(moles_bsp=moles_bsp, moles_morb_extracted=moles_morb_extracted)
    bsp_morb_wt_difference = calc_bsp_mob_wt_difference(bsp_morb_moles_difference=bsp_morb_moles_difference)
    depleted_lith_comp = calc_depleted_mantle_composition(differences=bsp_morb_wt_difference)

    return depleted_lith_comp



test_bsp = {
    'mgo': 37.92564057,
    'sio2': 47.04549377,
    'feo': 8.022871374,
    'al2o3': 3.318830187,
    'nao2': 0.331411863,
    'cao2': 3.179578462,
    'tio2': 0.176173779
}

test_morb = {
    'mgo': 0.170296864,
    'sio2': 52.10703783,
    'feo': 23.9055925,
    'al2o3': 13.32771365,
    'nao2': 1.646094229,
    'cao2': 6.301999891,
    'tio2': 1.297126116
}

test_mass_fraction = 1.92847

dm = calc_depleted_lith(bsp_oxide_wt_pct=test_bsp, morb_oxide_wt_pct=test_morb, morb_mass_fraction=test_mass_fraction)
print(dm)


