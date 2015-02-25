import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.evaluation.NominalPrediction;
import weka.classifiers.rules.DecisionTable;
import weka.classifiers.rules.PART;
import weka.classifiers.trees.DecisionStump;
import weka.classifiers.trees.J48;
import weka.core.Instances;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.classifiers.evaluation.NominalPrediction;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import weka.core.converters.CSVLoader;
import weka.filters.*;
import weka.filters.unsupervised.attribute.NumericToNominal;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
 
public class predict {
    
	/*
    public static BufferedReader readDataFile(String filename){
	BufferedReader inputReader = null;
	try {
	    inputReader = new BufferedReader(new FileReader(filename));
	} 
	catch (FileNotFoundException ex) {
	    System.err.println("File not found: " + filename);
	}
	return inputReader;
    }
 
    public static Evaluation classify(Classifier model,Instances trainingSet, Instances testingSet) throws Exception {
	
	Evaluation evaluation = new Evaluation(trainingSet);
	model.buildClassifier(trainingSet);
	evaluation.evaluateModel(model, testingSet);

	return evaluation;
    }
 
    
    public static double calculateAccuracy(FastVector predictions) {
	double correct = 0;
	for (int i = 0; i < predictions.size(); i++) {
	    NominalPrediction np = (NominalPrediction) predictions.elementAt(i);
	    if (np.predicted() == np.actual()) {
		correct++;
	    }
	} 
	return 100 * correct / predictions.size();
	}
 
    public static Instances[][] crossValidationSplit(Instances data, int numberOfFolds) {
	Instances[][] split = new Instances[2][numberOfFolds];
 
	for (int i = 0; i < numberOfFolds; i++) {
	    split[0][i] = data.trainCV(numberOfFolds, i);
	    split[1][i] = data.testCV(numberOfFolds, i);
	}
 
	return split;
	}*/
 
    public static void main(String[] args) throws Exception 
    {
    	FileWriter writer = new FileWriter("preds.csv");
    	CSVLoader loader = new CSVLoader();
    	loader.setSource(new File("map_testdata.csv"));
    	Instances data = loader.getDataSet();
    	// setting class attribute
    	NumericToNominal convert= new NumericToNominal();
        String[] options= new String[2];
        options[0]="-R";
        options[1]="last";
        convert.setOptions(options);
        convert.setInputFormat(data);
        data = Filter.useFilter(data, convert);

    	data.setClassIndex(data.numAttributes() - 1);
       
    	/*
		// Do 10-split cross validation
		Instances[][] split = crossValidationSplit(data, 10);
 
		// Separate split into training and testing arrays
		Instances[] trainingSplits = split[0];
		Instances[] testingSplits = split[1];
    	 */
	
	//You can change the input model here.
    	RandomForest classifier = (RandomForest) weka.core.SerializationHelper.read(new FileInputStream("decforest2.model"));
    	for (int i = 0; i < data.numInstances(); i++) {
    	double pred = classifier.classifyInstance(data.instance(i));
	    System.out.print("ID: " + data.instance(i).value(0));
	    System.out.print(", actual: " + data.classAttribute().value((int) data.instance(i).classValue()));
	    try{
	    	writer.append(data.classAttribute().value((int) pred));
	    	writer.append('\n');
	    }	
	    catch(IOException e){
	    	e.printStackTrace();
	    }
    }
    	writer.flush();
	writer.close();	
    }
}
