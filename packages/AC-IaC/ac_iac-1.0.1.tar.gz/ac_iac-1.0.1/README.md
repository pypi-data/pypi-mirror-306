# Argument Components - Identification and Classification
This package provides a command line tool to find MajorClaims, Claims, and Premises on argumentative essays, as defined by Stab and Gurevych in their 2017 paper.
## Inference
The tool `AC-IaC` takes one or more text files and finds MajorClaims, Claims, and Premises on them. 
The results are returned in Brat-Standoff-Format. 
If a directory is provided to the tool, it will recursively find all txt files in that and all the sub-directories.
This input structure will then be rebuilt in the output.
For the inference, **a trained model needs to be provided**. 
I may have the correct models available on Hugging-Face under my username Theoreticallyhugo, which you could use for quick and dirty testing.
However, for proper use you need to train your own model, using the tool `AC-IaC-train`, as described in the [training](#Training) section.
If you want to test how the files would be structured in the ouput, you can use the dry option.
## Training
The tool `AC-IaC-train` uses the original dataset of essays, annotated by Stab and Gurevych to train the models needed for inference.
Use `AC-IaC-train -h` to learn about the arguments that can be used.
### use for inference
You **always need to specify and ouput path**, which will house the model files.
If you have a Hugging-Face account, you can upload the models to Hugging-Face repos. This is recommended.
If you don't want the models to be uploaded, set the corresponding option.
Per default this tool will train both models, but it can be instructed to train just one of them.
### use for validation
The tool supports setting a seed, the number of epochs, and running 5-fold-cross-validation. The evaluation data can be found in the output directory.
The default number of epochs should always be good for use with inference.
## dev-structure
- command_line.py is the entry point for the module. `AC-IaC` and `AC-IaC-train` point to the functions `inference` and `train_wrapper` respectively.
- ./inference/ is the directory that houses everything inference related
- ./training/ is the directory that houses everything training related
