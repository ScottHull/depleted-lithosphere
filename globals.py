import pandas as pd

class ExoplanetPocketknifeGlobals:

    def __init__(self):
        # correction factors
        self.GALE_MGO = 7.652
        self.MODEL_EARTH_MGO = 11.844
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


def import_composition(df, row_index):
    if pd.notnull(df['SiO2'][row_index]):
        c = {
            'star': df['Star'][row_index],
            'sio2': df['SiO2'][row_index],
            'tio2': df['TiO2'][row_index],
            'al2o3': df['Al2O3'][row_index],
            'cr2o3': df['Cr2O3'][row_index],
            'feo': df['FeO'][row_index],
            'mgo': df['MgO'][row_index],
            'cao': df['CaO'][row_index],
            'na2o': df['Na2O'][row_index]
        }

        return c
    else:
        return None
