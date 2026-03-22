# Simple Coding Agent

This is based on the Boot.Dev course "Build an AI Agent". 
It uses a Google Gemini API to create application that can work as a basic coding agent. 

In addition to just calling the API and making it do something, it also takes care of security. The most important part being that it restricts the folder on which the application can act. 

I am planning on doing some extensions on this when I have free time. Particularly I would love to replace the Gemini API with a local Ollama model. 


## Calculator App

This is the main demo application used by the lesson. The application is given free access to the calculator folder and allowed to list files, read files, execute python code and write to files only in this folder. 

`main.py` is the entry point for a simple command-line calculator application.

## Usage

To run the calculator, execute `main.py` with a mathematical expression as a command-line argument.

```bash
python main.py "<expression>"
```

### Example

```bash
python main.py "3 + 5 * (10 - 2) / 2"
```

This will output the result of the expression in a JSON format.

## Error Handling

The application includes basic error handling for invalid expressions.

## Modules

- `pkg.calculator`: Contains the `Calculator` class responsible for evaluating mathematical expressions.
- `pkg.render`: Contains the `format_json_output` function for formatting the output.
