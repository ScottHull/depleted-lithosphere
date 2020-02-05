from globals import ExoplanetPocketknifeGlobals


class DepletedLithosphere(ExoplanetPocketknifeGlobals):

    def calculated_morb_to_original(self, oxide_weights):

        # this value needs to be removed from BSP
        original_oxide_wt_mgo = oxide_weights['mgo'] / self.MGO_CORRECTION_FACTOR

        return original_oxide_wt_mgo

    def normalize_compositions(self, oxide_wt_pct_unnormalized, mgo_correction='false'):
        normalized = {}
        oxides = list(oxide_wt_pct_unnormalized.keys())
        sum_total = 0
        for i in oxides:
            i = i.lower()
            if i == 'mgo' and mgo_correction != "false":
                sum_total += self.calculated_morb_to_original(oxide_weights=oxide_wt_pct_unnormalized)
            else:
                sum_total += oxide_wt_pct_unnormalized[i]
        for i in oxides:
            i = i.lower()
            if i == 'mgo' and mgo_correction != "false":
                normalized.update({i: (float(
                    self.calculated_morb_to_original(oxide_weights=oxide_wt_pct_unnormalized)) / float(
                    sum_total)) * 100.0})
            else:
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

    def calc_depleted_lith(self, bsp_oxide_wt_pct, morb_oxide_wt_pct, morb_mass_fraction, mgo_correction='false'):

        normalized_bsp_oxide_wt_pct = self.normalize_compositions(oxide_wt_pct_unnormalized=bsp_oxide_wt_pct)
        normalized_morb_oxide_wt_pct = self.normalize_compositions(oxide_wt_pct_unnormalized=morb_oxide_wt_pct,
                                                                   mgo_correction='true')
        moles_bsp = self.moles_from_oxide_wt_pct(oxide_wt_pct=normalized_bsp_oxide_wt_pct)
        moles_morb_extracted = self.calc_morb_moles_extracted(morb_mass_fraction=morb_mass_fraction,
                                                              normalized_morb_wt_pct=normalized_morb_oxide_wt_pct)
        bsp_morb_moles_difference, pct_change = self.calc_bsp_morb_moles_difference(moles_bsp=moles_bsp,
                                                                                    moles_morb_extracted=moles_morb_extracted)
        bsp_morb_wt_difference = self.calc_bsp_mob_wt_difference(bsp_morb_moles_difference=bsp_morb_moles_difference)
        depleted_lith_comp = self.calc_depleted_mantle_composition(differences=bsp_morb_wt_difference)

        return depleted_lith_comp
