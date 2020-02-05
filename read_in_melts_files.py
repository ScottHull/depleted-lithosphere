import os
import pandas as pd

from globals import import_composition
from dl import DepletedLithosphere


adibekyan_bsp_df = pd.read_excel('/Users/scotthull/Desktop/reproduce_melts_files_10_21_2019/Adibekyan_BSP_Compositions.xlsx', index='Star')
adibekyan_morb_f1200_df = pd.read_excel('/Users/scotthull/Desktop/reproduce_melts_files_10_21_2019/Adibekyan_F1200_MORB_Compositions.xlsx', index='Star')

for row in adibekyan_bsp_df.index:
    bsp_norm_comp = import_composition(df=adibekyan_bsp_df, row_index=row)
    morb_norm_comp = import_composition(df=adibekyan_morb_f1200_df, row_index=row)
    morb_mass_fraction = adibekyan_morb_f1200_df['Mass'][row] / 100.0,
    print(bsp_norm_comp)
    print(morb_norm_comp)
