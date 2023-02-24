import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, KBinsDiscretizer, MinMaxScaler
from sklearn.compose import ColumnTransformer
from mlxtend.feature_selection import ColumnSelector
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

df = pd.read_csv(
    "data/regressionData.csv").drop(['tconst', 'originalTitle'], axis=1)


X = df.drop(columns='averageRating')
y = df['averageRating']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)


num = X.select_dtypes(exclude=['object']).columns
num

cat = X.select_dtypes(include=['object']).columns
cat

num_transformer = Pipeline(steps=[('imputer', SimpleImputer()),
                                  ('discritiser', KBinsDiscretizer(
                                      encode='ordinal', strategy='uniform')),
                                  ('scaler', MinMaxScaler())])

cat_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
                                  ('col_selector', ColumnSelector(
                                      cols=(['director', 'actor', 'actress', 'writer', 'genre', 'producer']), drop_axis=True)),
                                  ('tfidf', TfidfVectorizer()),])

preprocessor = ColumnTransformer(transformers=[('num', num_transformer, num),
                                               ('cat', cat_transformer, cat)])

pipe = Pipeline(steps=[('preprocessor', preprocessor),
                       ('classiffier', LogisticRegression(random_state=1, max_iter=10000))])

param_grid = dict(regressor__imputer__strategy=['mean', 'median'],
                  regressor__discritiser__nbins=range(5, 10),
                  classiffier__C=[0.1, 10, 100],
                  classiffier__solver=['liblinear', 'saga'])
grid_search = GridSearchCV(pipe, param_grid=param_grid, cv=10)
grid_search.fit(X_train, y_train)
