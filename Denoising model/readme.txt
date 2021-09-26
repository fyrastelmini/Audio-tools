Drive link:
https://drive.google.com/drive/folders/11k8yrJFs2G8DIRZeYXKo3sqB7fXLIEX7?usp=sharing
Datasets: this version contains the dataset i generated from ARP files, the folders labeled with 0 at the end contain a smaller portion of the dataset used for
colab training, do not train using them
Training loop: the file DCunet_train.ipynb that is in this directory is already set correctly and ready for training, just place it within the main directory
               training arguments: most are self explanatory, but you need to know that there are 4 versions of this model (naivedcunet16/naivedcunet20/dcunet16/dcunet20)
               these versions are ordered by complexity
               you can chose the version to train by modifying the "parser.add_argument" cell
Testing model: use model_test.py, make sure the "parser.add_argument("--model"...)" corresponds to the one used in training, place files to test under the directory 
               "/datasets/fn". Output will be under "/Model_pred/".
The results i got out of this model were not satisfying, but its because i couldnt train on a large dataset, there is the possibility of the model performing better
with the whole dataset
