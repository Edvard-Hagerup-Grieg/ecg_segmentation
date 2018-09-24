import os
import time
import shutil
import logging
import pandas as pd

from experiment_num_leads.models import *

from crossvalidation import make_crossvalidation
from dataset import load_dataset

folder_for_results = "experiment_num_leads_results"

logging.basicConfig(filename='log.log',level=logging.DEBUG)

# модели участвующие в эксперименте
arr_models = {
    model1.make_model:"model 1",
    model2.make_model:"model 2",
    model4.make_model:"model 4",
    model6.make_model:"model 6",
    model8.make_model:"model 8",
    model12.make_model:"model 12"
}

# создает отлельную папку под результаты эксперимента и делаем ее на время умолчательной
cwd = os.getcwd()
if os.path.exists(folder_for_results) and os.path.isdir(folder_for_results):
    shutil.rmtree(folder_for_results)

os.makedirs(folder_for_results)
os.chdir(folder_for_results)

# параметры эксперимента
win_len = 3072
batch_size=10
epochs=14
xy = load_dataset()
X = xy["x"]
Y = xy["y"]

arr_results = []
# эксперимент - кроссвалидация по всем моделям
for make_model, model_description in arr_models.items():
    logging.info("start crossvalidation " + model_description + " at " + str(time.ctime()))
    result= make_crossvalidation(kfold_splits=4,
                         create_model=make_model,
                         X=X, Y=Y,
                         win_len=win_len,
                         model_name=model_description,
                         batch_size=batch_size,
                         epochs=epochs)
    logging.info(str(result))
    arr_results.append(result)

# сохраняем результаты в файл
table_results = pd.DataFrame(arr_results)
table_results.to_csv('results.txt', header=True, index=True, sep='\t', mode='a')

print(table_results)
os.chdir(cwd)