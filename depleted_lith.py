from dl import DepletedLithosphere
from morb_io import IO




























# model = DepletedLithosphere()
#
# test_bsp = {
#     'mgo': 37.92564057,
#     'sio2': 47.04549377,
#     'feo': 8.022871374,
#     'al2o3': 3.318830187,
#     'nao2': 0.331411863,
#     'cao2': 3.179578462,
#     'tio2': 0.176173779
# }
#
# test_morb = {
#     'mgo': 0.170296864,
#     'sio2': 52.10703783,
#     'feo': 23.9055925,
#     'al2o3': 13.32771365,
#     'nao2': 1.646094229,
#     'cao2': 6.301999891,
#     'tio2': 1.297126116
# }
#
# test_mass_fraction = 1.92847
#
# dm = model.calc_depleted_lith(bsp_oxide_wt_pct=test_bsp, morb_oxide_wt_pct=test_morb,
#                               morb_mass_fraction=test_mass_fraction, mgo_correction='true')
# print(dm)



morb_paths = [
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/reproduce_melts_files_10_21_2019/"
                  "MELTS Outputs/Kepler_Star_Compositions_F1200_Completed_MORB_MELTS_Files",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/reproduce_melts_files_10_21_2019/"
                  "MELTS Outputs/Kepler_Star_Compositions_F1400_Completed_MORB_MELTS_Files",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/reproduce_melts_files_10_21_2019/"
                  "MELTS Outputs/Kepler_Star_Compositions_F1600_Completed_MORB_MELTS_Files",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/reproduce_melts_files_10_21_2019/"
                  "MELTS Outputs/Adibekyan_Star_Compositions_F1200_Completed_MORB_MELTS_Files",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/reproduce_melts_files_10_21_2019/"
                  "MELTS Outputs/Adibekyan_Star_Compositions_F1400_Completed_MORB_MELTS_Files",
    "/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/reproduce_melts_files_10_21_2019/"
                  "MELTS Outputs/Adibekyan_Star_Compositions_F1600_Completed_MORB_MELTS_Files",
]

morb_fnames = [
    "kepler_morb_starting_masses_f1200.csv",
    "kepler_morb_starting_masses_f1400.csv",
    "kepler_morb_starting_masses_f1600.csv",
    "adibekyan_morb_starting_masses_f1200.csv",
    "adibekyan_morb_starting_masses_f1400.csv",
    "adibekyan_morb_starting_masses_f1600.csv",
]

for index, i in enumerate(morb_paths):
    fname = morb_fnames[index]
    io = IO(from_path=i, to_file=fname)
    io.get_liquid()
