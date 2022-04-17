Dependencies:

- csv	:  to manage data
- pandas : for dataset handling
- numpy : support for calculations
- math :  for mathematical operations
- nltk : for tokenization, stemming and using stopwords
- collections : for python dictionary
- unidecode : to convert into ASCII characters
- pickle : to save data objects
- re : for regular expression
- math : for mathematical operations
- string : for string manipulation


I have automated those installs but if any other library is missing install them by writing pip install library_name in the command line.
(for any query i am assuming there will be atleast one word which is present in the corpus otherwise my system will return no files)

Preprocessing:

In the first question i have done preprocesing by 
- Removing new lines and tabs
- Removing_extra whitespace
- Converting unicode data into ASCII characters
- Removing links
- Removing Code
- Removing wikipedia references
- Removing punctuations
- Removing stopwords
- Performing tokenization and stemming

The preprocessing code takes around 15 minutes. 

Query is processed within seconds.

Total expected time = 18-20 mins approximately

Please put the "english-corpora" folder in the same directory and then run it.

How to run:

1. Unzip 21111005-assignment1.zip
2. Place 'english-corpora' folder in this directory
3.run Question1.sh 
4. unzip 21111005-ir-systems directory. 
4.Put the query questions in the 21111005-ir-systems directory
(make sure it is written in a text file) then open the current directory in the terminal and type "make run ARGS=(your_file_name_.txt)" this 
command will first install all the packages and then preprocess/clean data,then run the scripts inside it and the make three text files in the 21111005-ir-systems.
