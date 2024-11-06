#!/usr/bin/env python

import pandas as pd

import useful_rdkit_utils as uru
from lgbm_wrapper import LGBMMorganCountWrapper
from sklearn.metrics import r2_score, mean_absolute_error

model_list = [("lgbm_morgan", LGBMMorganCountWrapper)]
group_list = [("butina", uru.get_butina_clusters), ("random", uru.get_random_split),
              ("scaffold", uru.get_bemis_murcko_clusters), ("umap", uru.get_umap_clusters)]
metric_list = [("R2", r2_score), ("MAE", mean_absolute_error)]


df = pd.read_csv("/Users/pwalters/software/benchmark/data/biogen_logS.csv")
y = "logS"

result_list = uru.cross_validate(df, model_list, y, group_list, metric_list, 5, 5)
result_df = pd.DataFrame(result_list)
result_df.to_csv("biogen_logS_results.csv", index=False)
