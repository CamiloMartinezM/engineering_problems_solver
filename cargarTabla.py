# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 13:23:16 2020

@author: Camilo Martínez
"""

from tabula import read_pdf
import pandas as pd

df = read_pdf('out.pdf', pages='all', output_format='dataframe')[0]
# df.drop(df.index[[0,1]], inplace=True)
# df.reset_index(drop=True, inplace=True)
# df.columns = ["UNS", "SAE/AISI", "Proc.", "Sut[MPa]", "Sy[MPa]", "ef", "af", "HB"]
# df["Sut[kpsi]"] = df["Sut[MPa]"]
# df["Sy[kpsi]"] = df["Sy[MPa]"]

# for i, row in enumerate(df["Sut[MPa]"]):
#     df["Sut[kpsi]"][i] = row.split(" ")[1][1:-1]
#     df["Sut[MPa]"][i] = row.split(" ")[0]
    
# for i, row in enumerate(df["Sy[MPa]"]):
#     df["Sy[kpsi]"][i] = row.split(" ")[1][1:-1]
#     df["Sy[MPa]"][i] = row.split(" ")[0]
    
# columns_titles = ["UNS", "SAE/AISI", "Proc.", "Sut[MPa]", "Sut[kpsi]", \
#                   "Sy[MPa]", "Sy[kpsi]", "ef", "af", "HB"]
# df = df.reindex(columns=columns_titles)

# df["UNS"] = df["UNS"] + "(" + df["Proc."] + ")"

# i = 0
# while i < len(df["UNS"]) and i <= 18:
#     df["UNS"][i+1] = df["UNS"][i]
#     df["SAE/AISI"][i+1] = df["SAE/AISI"][i]
#     i += 2
    
# df.to_excel('Materials_1.xlsx', index=False)