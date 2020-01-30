class DepletedLithosphere:

    def __init__(self):
        # correction factors
        self.GALE_MGO = 11.844
        self.MODEL_EARTH_MGO = 7.652
        self.MGO_CORRECTION_FACTOR = self.GALE_MGO / self.MODEL_EARTH_MGO

        # oxide numbers
        self.oxide_cations = {
            'mgo': 1.0,
            'sio2': 1.0,
            'feo': 1.0,
            'fe2o3': 2.0,
            'al2o3': 2.0,
            'nao2': 1.0,
            'cao2': 1.0,
            'tio2': 1.0
        }
        self.oxide_anions = {
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
        self.atomic_masses = {
            'mg': 24.305,
            'si': 28.086,
            'fe': 55.845,
            'al': 26.982,
            'na': 22.99,
            'ca': 40.078,
            'ti': 47.867,
            'o': 16.0
        }
        self.oxide_masses = {
            'mgo': (self.atomic_masses['mg'] * self.oxide_cations['mgo']) + (
                        self.atomic_masses['o'] * self.oxide_anions['mgo']),
            'sio2': (self.atomic_masses['si'] * self.oxide_cations['sio2']) + (
                        self.atomic_masses['o'] * self.oxide_anions['sio2']),
            'feo': (self.atomic_masses['fe'] * self.oxide_cations['feo']) + (
                        self.atomic_masses['o'] * self.oxide_anions['feo']),
            'fe2o3': (self.atomic_masses['fe'] * self.oxide_cations['fe2o3']) + (
                        self.atomic_masses['o'] * self.oxide_anions['fe2o3']),
            'al2o3': (self.atomic_masses['al'] * self.oxide_cations['al2o3']) + (
                        self.atomic_masses['o'] * self.oxide_anions['al2o3']),
            'nao2': (self.atomic_masses['na'] * self.oxide_cations['nao2']) + (
                        self.atomic_masses['o'] * self.oxide_anions['nao2']),
            'cao2': (self.atomic_masses['ca'] * self.oxide_cations['cao2']) + (
                        self.atomic_masses['o'] * self.oxide_anions['cao2']),
            'tio2': (self.atomic_masses['ti'] * self.oxide_cations['tio2']) + (
                        self.atomic_masses['o'] * self.oxide_anions['tio2'])
        }

    def calculated_morb_to_original(self, oxide_weights):

        # this value needs to be removed from BSP
        original_oxide_wt_mgo = oxide_weights['mgo'] / self.MGO_CORRECTION_FACTOR

    def normalize_compositions(self, oxide_wt_pct_unnormalized):
        normalized = {}
        oxides = list(oxide_wt_pct_unnormalized.keys())
        sum_total = 0
        for i in oxides:
            sum_total += oxide_wt_pct_unnormalized[i]
        for i in oxides:
            normalized.update({i: (float(oxide_wt_pct_unnormalized[i]) / float(sum_total)) * 100.0})

        return normalized

    def moles_from_oxide_wt_pct(self, oxide_wt_pct):
        oxide_moles = {}
        oxides = list(oxide_wt_pct.keys())
        for i in oxides:
            oxide_moles.update({i: oxide_wt_pct[i] / self.oxide_masses[i]})

        return oxide_moles

    def calc_morb_moles_extracted(self, morb_mass_fraction, normalized_morb_wt_pct):
        moles = {}
        oxides = list(normalized_morb_wt_pct.keys())
        for i in oxides:
            moles.update({i: (morb_mass_fraction / 100.0) * (normalized_morb_wt_pct[i] / self.oxide_masses[i])})

        return moles

    def calc_bsp_morb_moles_difference(self, moles_bsp, moles_morb_extracted):
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

    def calc_bsp_mob_wt_difference(self, bsp_morb_moles_difference):
        diff = {}
        oxides = list(bsp_morb_moles_difference.keys())
        for i in oxides:
            wt = bsp_morb_moles_difference[i] * self.oxide_masses[i]
            diff.update({i: wt})

        return diff

    def calc_depleted_mantle_composition(self, differences):
        comp = {}
        oxides = list(differences.keys())
        sum_total = 0
        for i in oxides:
            sum_total += differences[i]
        for i in oxides:
            comp.update({i: 100.0 * (differences[i] / sum_total)})
        return comp

    def calc_depleted_lith(self, bsp_oxide_wt_pct, morb_oxide_wt_pct, morb_mass_fraction):

        normalized_bsp_oxide_wt_pct = self.normalize_compositions(oxide_wt_pct_unnormalized=bsp_oxide_wt_pct)
        normalized_morb_oxide_wt_pct = self.normalize_compositions(oxide_wt_pct_unnormalized=morb_oxide_wt_pct)
        moles_bsp = self.moles_from_oxide_wt_pct(oxide_wt_pct=normalized_bsp_oxide_wt_pct)
        moles_morb_extracted = self.calc_morb_moles_extracted(morb_mass_fraction=morb_mass_fraction,
                                                              normalized_morb_wt_pct=normalized_morb_oxide_wt_pct)
        bsp_morb_moles_difference, pct_change = self.calc_bsp_morb_moles_difference(moles_bsp=moles_bsp,
                                                                                    moles_morb_extracted=moles_morb_extracted)
        bsp_morb_wt_difference = self.calc_bsp_mob_wt_difference(bsp_morb_moles_difference=bsp_morb_moles_difference)
        depleted_lith_comp = self.calc_depleted_mantle_composition(differences=bsp_morb_wt_difference)

        return depleted_lith_comp
