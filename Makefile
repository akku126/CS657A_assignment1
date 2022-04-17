run:
	pip install numpy
	pip install pandas
	pip install nltk
	pip install unidecode
	unzip 21111005-ir-systems
	cd 2111 && sh Question4.sh $(ARGS)
	
clean:
	rm -rf BM25.txt
	rm -rf boolean.txt
	rm -rf tf_df.txt
	

