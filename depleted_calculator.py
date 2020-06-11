import os
import shutil




BSP_FILE_FORMAT = "0,20,80,{},0,-2,0\n6,2,4,2\noxides\nSi          {}      5.39386    0\nMg          {}     2.71075    0\n" \
                             "Fe          {}      .79840    0\nCa            {}      .31431    0\nAl            {}      .96680    0\n" \
                             "Na            {}      .40654    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\nhc\n" \
                             "phase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\njd\n" \
                             "phase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\nmgwa\nfewa\n" \
                             "phase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\nphase ppv\n0\nmppv\n" \
                             "fppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n1\nqtz\nphase coes\n0\ncoes\n" \
                             "phase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n0\nneph"

MORB_FILE_FORMAT = "0,20,80,1200,0,-2,0\n6,2,4,2\noxides\nSi           {}     5.33159    0\n" \
                             "Mg           {}     1.37685    0\nFe           {}      .55527    0\n" \
                             "Ca           {}     1.33440    0\nAl           {}     1.82602    0\n" \
                             "Na           {}     0.71860    0\n1,1,1\ninv251010\n47\nphase plg\n1\nan\nab\nphase sp\n0\nsp\n" \
                             "hc\nphase opx\n1\nen\nfs\nmgts\nodi\nphase c2c\n0\nmgc2\nfec2\nphase cpx\n1\ndi\nhe\ncen\ncats\n" \
                             "jd\nphase gt\n0\npy\nal\ngr\nmgmj\njdmj\nphase cpv\n0\ncapv\nphase ol\n1\nfo\nfa\nphase wa\n0\n" \
                             "mgwa\nfewa\nphase ri\n0\nmgri\nferi\nphase il\n0\nmgil\nfeil\nco\nphase pv\n0\nmgpv\nfepv\nalpv\n" \
                             "phase ppv\n0\nmppv\nfppv\nappv\nphase cf\n0\nmgcf\nfecf\nnacf\nphase mw\n0\npe\nwu\nphase qtz\n" \
                             "1\nqtz\nphase coes\n0\ncoes\nphase st\n0\nst\nphase apbo\n0\napbo\nphase ky\n0\nky\nphase neph\n" \
                             "0\nneph"


class WriteFiles:

    def __init__(self):

        self.base_dir = os.getcwd() + "/HeFESTo_Input_Files"
        self.bsp_dir = self.base_dir + "/BSP"
        self.morb_dir = self.base_dir + "/MORB"
        self.F_temperature_dir = None
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)
        os.mkdir(self.base_dir)
        os.mkdir(self.bsp_dir)
        os.mkdir(self.morb_dir)
        self.current_temp_dir = None


    def writeFile(self, star, type, F_temperature, temperatures_to_run=[], **kwargs):

        mg = kwargs['kwargs']['mg']
        si = kwargs['kwargs']['si']
        fe = kwargs['kwargs']['fe']
        al = kwargs['kwargs']['al']
        na = kwargs['kwargs']['na']
        ca = kwargs['kwargs']['ca']
        ti = kwargs['kwargs']['ti']

        if type.lower() == 'bsp':

            self.F_temperature_dir = self.bsp_dir + "/F{}".format(F_temperature)

            if not os.path.exists(self.F_temperature_dir):
                os.mkdir(self.F_temperature_dir)

            for temperature in temperatures_to_run:
                if not os.path.exists(self.F_temperature_dir + "/{}".format(temperature)):
                    os.mkdir(self.F_temperature_dir + "/{}".format(temperature))

                self.current_temp_dir = self.F_temperature_dir + "/{}".format(temperature)

                f = open(self.current_temp_dir + "/{}_{}_{}_HeFESTo_Input_File.txt".format(star, type,
                                                                                            temperature), 'w')
                f_str = BSP_FILE_FORMAT.format(temperature, si, mg, fe, ca, al, na)
                f.write(f_str)
                f.close()

        elif type.lower() == 'morb':

            self.F_temperature_dir = self.morb_dir + "/{}".format(F_temperature)

            if not os.path.exists(self.F_temperature_dir):
                os.mkdir(self.F_temperature_dir)

            for temperature in temperatures_to_run:
                if not os.path.exists(self.F_temperature_dir + "/{}".format(temperature)):
                    os.mkdir(self.F_temperature_dir + "/{}".format(temperature))

                self.current_temp_dir = self.F_temperature_dir + "/{}".format(temperature)

                f = open(self.current_temp_dir + "/{}_{}_{}_F{}_HeFESTo_Input_File.txt".format(star, type, temperature,
                                                                                                F_temperature), 'w')
                f_str = MORB_FILE_FORMAT.format(temperature, si, mg, fe, ca, al, na)
                f.write(f_str)
                f.close()





class _AtomicWeights:

    def __init__(self):
        self.fe = 55.845
        self.mg = 24.305
        self.si = 28.086
        self.ca = 40.078
        self.al = 26.982
        self.ti = 47.867
        self.na = 22.99
        self.o = 16


class _OxideCationNumbers:

    def __init__(self):
        self.fe = 1  # feo, 1
        self.mg = 1  # mgo, 1
        self.si = 1  # sio2, 1
        self.ca = 1  # cao, 1
        self.al = 2  # al2o3, 2
        self.ti = 1  # tio2, 1
        self.na = 2  # na2o, 2


class _OxideWeights:

    def __init__(self):
        self.atomic_weights = _AtomicWeights()
        self.oxide_cation_numbers = _OxideCationNumbers()
        self.feo = (self.atomic_weights.fe * self.oxide_cation_numbers.fe) + self.atomic_weights.o
        self.mgo = (self.atomic_weights.mg * self.oxide_cation_numbers.mg) + self.atomic_weights.o
        self.sio2 = (self.atomic_weights.si * self.oxide_cation_numbers.si) + (self.atomic_weights.o * 2)
        self.cao = (self.atomic_weights.ca * self.oxide_cation_numbers.ca) + self.atomic_weights.o
        self.al2o3 = (self.atomic_weights.al * self.oxide_cation_numbers.al) + (self.atomic_weights.o * 3)
        self.tio2 = (self.atomic_weights.ti * self.oxide_cation_numbers.ti) + (self.atomic_weights.o * 2)
        self.na2o = (self.atomic_weights.na * self.oxide_cation_numbers.na) + self.atomic_weights.o


class Calculator:

    def __init__(self):
        self.oxide_weights = _OxideWeights()
        self.cation_numbers = _OxideCationNumbers()
        self.type = None  # bsp or morb
        self.temperature = 1400  # degK
        self.mass_fraction = 0
        self.mgo = 0  # wt%
        self.sio2 = 0  # wt%
        self.feo = 0  # wt%
        self.al2o3 = 0  # wt%
        self.na2o = 0  # wt%
        self.cao = 0  # wt%
        self.tio2 = 0  # wt%
        self.sum = (self.mgo + self.sio2 + self.feo + self.al2o3 + self.na2o +
                    self.cao + self.tio2)  # wt%

    def calculator(self, type, temperature, mass_fraction, mgo, sio2, feo, al2o3, na2o, cao, tio2):

        self.type = type  # bsp by default, other option is morb
        self.temperature = temperature  # degK
        self.mass_fraction = mass_fraction
        self.mgo = mgo  # wt%
        self.sio2 = sio2  # wt%
        self.feo = feo  # wt%
        self.al2o3 = al2o3  # wt%
        self.na2o = na2o  # wt%
        self.cao = cao  # wt%
        self.tio2 = tio2  # wt%
        self.sum = (self.mgo + self.sio2 + self.feo + self.al2o3 + self.na2o +
                    self.cao + self.tio2)

        response = {
            'mgo': self.mgo,
            'sio2': self.sio2,
            'feo': self.feo,
            'al2o3': self.al2o3,
            'na2o': self.na2o,
            'cao': self.cao,
            'tio2': self.tio2,
            'sum': self.sum,
        }

        return response



    def calcWtPercent(self):
        """
        In wt%.
        :return:
        """
        mgo = self.mgo / self.sum * 100
        sio2 = self.sio2 / self.sum * 100
        feo = self.feo / self.sum * 100
        al2o3 = self.al2o3 / self.sum * 100
        na2o = self.na2o / self.sum * 100
        cao = self.cao / self.sum * 100
        tio2 = self.tio2 / self.sum * 100
        sum = (mgo + sio2 + feo + al2o3 + na2o + cao + tio2)

        response = {
            'mgo': mgo,
            'sio2': sio2,
            'feo': feo,
            'al2o3': al2o3,
            'na2o': na2o,
            'cao': cao,
            'tio2': tio2,
            'sum': sum,
        }

        return response

    def calcMoles(self):
        """
        In moles.
        :return:
        """
        wt_pct = self.calcWtPercent()

        mgo = wt_pct['mgo'] / (self.oxide_weights.mgo)
        sio2 = wt_pct['sio2'] / (self.oxide_weights.sio2)
        feo = wt_pct['feo'] / (self.oxide_weights.feo)
        al2o3 = wt_pct['al2o3'] / (self.oxide_weights.al2o3)
        na2o = wt_pct['na2o'] / (self.oxide_weights.na2o)
        cao = wt_pct['cao'] / (self.oxide_weights.cao)
        tio2 = wt_pct['tio2'] / (self.oxide_weights.tio2)
        sum = (mgo + sio2 + feo + al2o3 + na2o + cao + tio2)

        response = {
            'mgo': mgo,
            'sio2': sio2,
            'feo': feo,
            'al2o3': al2o3,
            'na2o': na2o,
            'cao': cao,
            'tio2': tio2,
            'sum': sum,
        }

        return response

    def calcMolesExtracted(self):
        """
        In moles.
        :return:
        """
        wt_pct = self.calcWtPercent()

        mgo = (self.mass_fraction / 100) * wt_pct['mgo'] / (self.oxide_weights.mgo)
        sio2 = (self.mass_fraction / 100) * wt_pct['sio2'] / (self.oxide_weights.sio2)
        feo = (self.mass_fraction / 100) * wt_pct['feo'] / (self.oxide_weights.feo)
        al2o3 = (self.mass_fraction / 100) * wt_pct['al2o3'] / (self.oxide_weights.al2o3)
        na2o = (self.mass_fraction / 100) * wt_pct['na2o'] / (self.oxide_weights.na2o)
        cao = (self.mass_fraction / 100) * wt_pct['cao'] / (self.oxide_weights.cao)
        tio2 = (self.mass_fraction / 100) * wt_pct['tio2'] / (self.oxide_weights.tio2)
        sum = (mgo + sio2 + feo + al2o3 + na2o + cao + tio2)

        response = {
            'mgo': mgo,
            'sio2': sio2,
            'feo': feo,
            'al2o3': al2o3,
            'na2o': na2o,
            'cao': cao,
            'tio2': tio2,
            'sum': sum,
        }

        return response

    def bsp_morb_difference(self, moles_bsp, moles_morb_extracted):
        """
        Changes by mole.
        :param moles_bsp:
        :param moles_morb_extracted:
        :return:
        """
        differences = {}

        for key in moles_bsp:
            if key != 'sum':
                diff = moles_bsp[key] - moles_morb_extracted[key]
                differences.update({key: diff})

        total = sum([i for i in differences.values()])
        differences.update({'sum': total})

        return differences

    def molesPctChanges(self, bsp_morb_differences, moles_bsp):
        """
        Changes by mole.
        :param bsp_morb_differences:
        :param moles_bsp:
        :return:
        """
        changes = {}

        for key in bsp_morb_differences:
            if key != 'sum':
                change = 100 - (100 * moles_bsp[key] / bsp_morb_differences[key])
                changes.update({key: change})
        total = sum([i for i in changes.values()])
        changes.update({'sum': total})

        return changes

    def wtBSPMORB(self, bsp_morb_moles):
        """
        In moles, returns wt (g).
        :return:
        """
        changes = {}

        mgo = bsp_morb_moles['mgo'] * self.oxide_weights.mgo
        sio2 = bsp_morb_moles['sio2'] * self.oxide_weights.sio2
        feo = bsp_morb_moles['feo'] * self.oxide_weights.feo
        al2o3 = bsp_morb_moles['al2o3'] * self.oxide_weights.al2o3
        na2o = bsp_morb_moles['na2o'] * self.oxide_weights.na2o
        cao = bsp_morb_moles['cao'] * self.oxide_weights.cao
        tio2 = bsp_morb_moles['tio2'] * self.oxide_weights.tio2
        changes.update({
            'mgo': mgo,
            'sio2': sio2,
            'feo': feo,
            'al2o3': al2o3,
            'na2o': na2o,
            'cao': cao,
            'tio2': tio2,
        })
        total = sum([i for i in changes.values()])
        changes.update({'sum': total})

        return changes


    def depletedMantleCompositionWtPct(self, bsp_morb_wt):
        """
        In g, returns wt%.
        :return:
        """
        composition = {}

        for key in bsp_morb_wt:
            if key != 'sum':
                c = 100 * (bsp_morb_wt[key] / bsp_morb_wt['sum'])
                composition.update({key: c})
        total = sum([i for i in composition.values()])
        composition.update({'sum': total})

        return composition


    def depletedMantleCompositionCations(self, depletedMantleCompositionWtPct):
        """
        In wt%, out cations percent (unitless).
        :param depletedMantleCompositionWtPct:
        :return:
        """

        composition = {}

        mgo = depletedMantleCompositionWtPct['mgo'] * self.cation_numbers.mg
        sio2 = depletedMantleCompositionWtPct['sio2'] * self.cation_numbers.si
        feo = depletedMantleCompositionWtPct['feo'] * self.cation_numbers.fe
        al2o3 = depletedMantleCompositionWtPct['al2o3'] * self.cation_numbers.al
        na2o = depletedMantleCompositionWtPct['na2o'] * self.cation_numbers.na
        cao = depletedMantleCompositionWtPct['cao'] * self.cation_numbers.ca
        tio2 = depletedMantleCompositionWtPct['tio2'] * self.cation_numbers.ti
        sum_cations = (mgo + sio2 + feo + al2o3 + na2o + cao + tio2)

        composition.update({
            'mg': mgo / sum_cations * 100,
            'si': sio2 / sum_cations * 100,
            'fe': feo / sum_cations * 100,
            'al': al2o3 / sum_cations * 100,
            'na': na2o / sum_cations * 100,
            'ca': cao / sum_cations * 100,
            'ti': tio2 / sum_cations * 100,
        })
        total = sum([i for i in composition.values()])
        composition.update({'sum': total})

        return composition
