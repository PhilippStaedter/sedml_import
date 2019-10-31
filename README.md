# ReadMe
About the order in which all scripts are executed.

## 1 Create the whole model collection 
### 1.1 Download all sedml and sbml models from the JWS Online Database
	script_download_all_sedml_models.py

### 1.2 Download chosen sbml models from the BioModels Database
	downloaded "by hand" --- no script available

### 1.3 Import all sbml models to AMICI
	sbml2amici.py
	sbml2amici_BioModelsDatabase.py

### 1.4 Check for correctly generated .so files and delete all other sbml models 
	no explicit script yet 

### 1.5 Compare the state trajectories of the local simulation to the in-built simulation routine of JWS
	compareStateTrajectories_1.py
	compareStateTrajectories_2.py
	compareStateTrajectories_plot.py

### 1.6 Derive the whole model collection
	correctStateTrajectories.py

### 1.7 Plot basic properties
	plot_first_results.py
	stat_reac_par.py
	Intern_vs_Extern.py
	num_x_num_p.py


## 2 Do the solver settings study based on the model collection
### 2.1 Tolerance study
	execute_Tolerances.py
	plotHistogram.py
	plotBoxPlot.py

### 2.2 Linear solver study
	execute_LinearSolvers.py
	plotScatter.py

### 2.3	Non-linear solver study
	execute_NonlinearSolvers.py
	(no plotting script yet)

### 2.4 Multistep method study
	execute_SolAlg.py
	plotScatter2.py
	plotScatter3.py


## 3 Predictor model
### 3.1 Get the input data (by determination of the kinetic rate law) for the logistic regression
	Input_Data.py

### 3.2 Predictor model with/without cross-validation
	Predictor.py
	PredictorCV.py
	PredictorCV_2.py

### 3.3 Divide all categorical Input values into more sections
	DivComb.py 

### 3.4 Plot different results
	plotAdamsBDF.py
	plotAdBf.py
	plotPrediction.py
