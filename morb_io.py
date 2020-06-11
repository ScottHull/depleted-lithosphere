import os
import csv

class IO:

    def __init__(self, from_path, to_file="morb.csv"):
        self.from_path = from_path
        self.initial_mass = 0
        self.morb_mass = 0
        self.header = []
        self.morb_comp = []
        if to_file in os.listdir(os.getcwd()):
            os.remove(to_file)
        self.to_file = open(to_file, 'a')
        self.first_file = True
        self.star = None

    def get_liquid(self):
        for i in os.listdir(self.from_path):
            if "_MORB_OUTPUT.csv" in i:
                with open(self.from_path + "/" + i, 'r') as infile:
                    found_liquid = False
                    reader = csv.reader(infile)
                    self.star = next(reader)[1]
                    print(self.star, i)
                    for row in reader:
                        if len(row) > 0:
                            if row[0] == "liquid_0":
                                found_liquid = True
                                if self.first_file:
                                    self.header = ["initial_mass"] + list(next(reader))
                                    # self.to_file.write("{}\n".format(",".join(i for i in self.header)))
                                    self.to_file.write("{},{}\n".format("star", "initial_mass"))
                                    self.first_file = False
                                else:
                                    next(reader)
                                    self.initial_mass = next(reader)[2]
                            if found_liquid:
                                if len(row) > 0:
                                    self.morb_comp = row
                                else:
                                    break
                    comp_line = ",".join(str(i) for i in self.morb_comp)
                    self.to_file.write("{},{}\n".format(self.star, self.initial_mass))
                    infile.close()
        self.to_file.close()
