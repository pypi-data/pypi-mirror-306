print("""from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix,classification_report,accuracy_score,f1_score)
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('METABRIC_RNA_Mutation.csv')
df.head()
df.dropna(inplace=True)
df_exp = df.iloc[:,30:519].join(df['overall_survival'],how='inner')
target_column = 'overall_survival'

X = df_exp.drop(columns=target_column)
y = df_exp['overall_survival']
X = pd.get_dummies(X,drop_first=True)
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3)
random_forest_model = RandomForestClassifier()
random_forest_model.fit(X_train,y_train)

y_pred = random_forest_model.predict(X_test)
accuracy_score(y_test,y_pred)
f1_score(y_test,y_pred)
svc_model = SVC()
svc_model.fit(X_train,y_train)

y_pred_svc = svc_model.predict(X_test)
accuracy_score(y_test,y_pred_svc)

f1_score(y_test,y_pred_svc)

cm = confusion_matrix(y_test,y_pred_svc)
from sklearn.metrics import ConfusionMatrixDisplay
disp = ConfusionMatrixDisplay(cm)
disp.plot()""")