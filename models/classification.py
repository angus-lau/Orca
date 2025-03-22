import h2o
from h2o.automl import H2OAutoML

h2o.init()
print('h2o started')

# load data
df = h2o.import_file('data/titanic_data.csv')

# set target column as factor so it knows to see values as categorial 
df['Survived']  = df['Survived'].asfactor()

# target and features
x = [col for col in df.columns if col != 'Survived']
y = 'Survived'

# drop irrelvant columns
x = [col for col in df.col_names if col not in ['PassengerId', 'Name', 'Ticket', 'Cabin']]

# split data
train, test = df.split_frame(ratio=[0.8], seed=42)

# train AutoML
aml = H2OAutoML(max_models=20, seed=1)
aml.train(x=x, y=y, training_frame=train)

# view leaderboard
lb = aml.leaderboard
print(lb.head(rows=lb.nrows))

# The leader model is stored here
preds = aml.leader.predict(test)
print(preds.head())