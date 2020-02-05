from globals import ExoplanetPocketknifeGlobals


class MORBRecalculation(ExoplanetPocketknifeGlobals):

    def normalize_compositions(self, oxide_wt_pct_unnormalized):
        normalized = {}
        oxides = list(oxide_wt_pct_unnormalized.keys())
        sum_total = 0
        for i in oxides:
            i = oxides[i].lower()
            sum_total += oxide_wt_pct_unnormalized[i]
        for i in oxides:
            normalized.update({i: (float(oxide_wt_pct_unnormalized[i]) / float(sum_total)) * 100.0})

        return normalized

    def calculate_oxide_weights(self, oxide_wt_pct, system_mass):
        oxide_weights = {}
        oxides = list(oxide_wt_pct.keys())
        for i in oxides:
            oxide_weights.update({i: (oxide_wt_pct[i] / 100.0) * system_mass})

        return oxide_weights

    def calculate_oxide_moles(self, oxide_wt):
        oxide_moles = {}
        oxides = list(oxide_wt.keys())
        for i in oxides:
            oxide_moles.update({i: oxide_wt[i] / self.oxide_masses[i]})

        return oxide_moles

    def calculate_number_cations(self, oxide_moles):
        calc_oxide_cations = {}
        oxides = list(oxide_moles.keys())
        for i in oxides:
            calc_oxide_cations.update({i: oxide_moles[i] * self.oxide_cations[i]})

        return calc_oxide_cations

    def recalc_feo_fe2o3(self, oxide_cation_nums, morb_normalized_oxide_weight_pct):
        total_cations_fe = oxide_cation_nums['feo'] + oxide_cation_nums['fe2o3']
        wt_fe = total_cations_fe * self.atomic_masses['fe']
        oxide_wt_feo = total_cations_fe * wt_fe

        morb_normalized_oxide_weight_pct['feo'] = oxide_wt_feo
        del morb_normalized_oxide_weight_pct['fe2o3']
        normalized_compositions = self.normalize_compositions(
            oxide_wt_pct_unnormalized=morb_normalized_oxide_weight_pct)

        return normalized_compositions

    def correct_mgo_in_morb(self, oxide_wt_pct):

        corrected_mgo = oxide_wt_pct['mgo'] / self.MGO_CORRECTION_FACTOR
        removed_mgo = oxide_wt_pct['mgo'] - corrected_mgo
        oxide_wt_pct['mgo'] = corrected_mgo
        renormalized_mgo_oxide_wt_pct = self.normalize_compositions(oxide_wt_pct_unnormalized=oxide_wt_pct)

        return renormalized_mgo_oxide_wt_pct

    def recalculate_morb_composition(self, morb_oxide_weight_pct_unnormalized, system_mass):

        morb_normalized_oxide_weight_pct = self.normalize_compositions(
            oxide_wt_pct_unnormalized=morb_oxide_weight_pct_unnormalized)
        morb_oxide_weights = self.calculate_oxide_weights(oxide_wt_pct=morb_normalized_oxide_weight_pct,
                                                          system_mass=system_mass)
        morb_oxide_moles = self.calculate_oxide_moles(oxide_wt=morb_oxide_weights)
        morb_oxide_cations = self.calculate_number_cations(oxide_moles=morb_oxide_moles)
        new_feo_normalzied_wt_pct = self.recalc_feo_fe2o3(
            morb_normalized_oxide_weight_pct=morb_normalized_oxide_weight_pct,
            oxide_cation_nums=morb_oxide_cations)
        mgo_normalized_oxide_wt_pct = self.correct_mgo_in_morb(oxide_wt_pct=new_feo_normalzied_wt_pct)

        return mgo_normalized_oxide_wt_pct

