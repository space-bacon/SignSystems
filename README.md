# SignSystems
Sign System Categorization 

# Sign Systems Categorization Project

## Overview

This project categorizes a given keyword, phrase or pdf into various sign systems and subcategories to analyze the influence of each sign system. The project uses both simple string matching and GPT-4 to provide an in-depth analysis and detailed descriptions.

## Sign Systems and Subcategories

The project categorizes the input into the following sign systems and their respective subcategories:

### Biological Sign Systems
- Genetic Sign Systems
  - DNA
  - RNA
  - Protein Synthesis
  - Epigenetics
- Cellular Sign Systems
  - Signal Transduction
  - Receptor-Ligand Interactions
  - Intracellular Communication
  - Intercellular Communication
- Ecological Sign Systems
  - Symbiosis
  - Pollination
  - Seed Dispersal
  - Animal Behavior
- Evolutionary Sign Systems
  - Natural Selection
  - Coevolution
  - Speciation

### Human Sign Systems
- Linguistic Sign Systems
  - Phonology
  - Morphology
  - Syntax
  - Semantics
  - Pragmatics
- Nonverbal Sign Systems
  - Gestures
  - Facial Expressions
  - Body Language
  - Proxemics
- Cultural Sign Systems
  - Symbols
  - Rituals
  - Art
  - Myths
- Technological Sign Systems
  - Digital Communication
  - Internet of Things
  - Artificial Intelligence

### Animal Sign Systems
- Vocalizations
  - Birds
  - Mammals
  - Amphibians
  - Insects
- Chemical Communication
  - Pheromones
  - Scent Marking
  - Alarm Signals
  - Trail Markers
- Visual Signals
  - Coloration
  - Bioluminescence
  - Postures
  - Movements
- Tactile Signals
  - Grooming
  - Touch
  - Vibrations

### Artificial Sign Systems
- Formal Languages
  - Mathematical Symbols
  - Programming Languages
  - Logical Notation
  - Chemical Formulae
- Road Signs
  - Regulatory Signs
  - Warning Signs
  - Informational Signs
  - Guide Signs
- Maritime Signals
  - Flags
  - Lights
  - Sound Signals
  - Buoys
- Aviation Signals
  - Air Traffic Control
  - Navigation Lights
  - Ground Signals
  - In-Flight Signals

### Semiotic Theories
- Structural Semiotics
- Peircean Semiotics
- Saussurean Semiotics
- Biosemiotics
- Cognitive Semiotics
- Cultural Semiotics

### Subfields of Semiotics
- Semiotic Anthropology
- Comics Semiotics
- Computational Semiotics
- Cultural and Literary Semiotics
- Cybersemiotics
- Design Semiotics
- Ethnosemiotics
- Film Semiotics
- Finite Semiotics
- Gregorian Chant Semiology
- Hylosemiotics
- Law and Semiotics
- Marketing Semiotics
- Music Semiotics
- Organizational Semiotics
- Pictorial Semiotics
- Semiotics of Music Videos
- Social Semiotics
- Structuralism and Post-Structuralism
- Theatre Semiotics
- Urban Semiotics
- Visual Semiotics
- Semiotics of Photography
- Artificial Intelligence Semiotics
- Semiotics of Mathematics

## Process

1. **Input**: The input keyword or phrase is read from `input.txt`. For multimodal categorization use `input.pdf`. 
2. **Categorization**: The keyword is categorized using:
   - Simple string matching
   - GPT-4 API
3. **Combination**: The results from both methods are combined and normalized.
4. **Output**: An overview and detailed descriptions are generated and saved to `output.txt`.
5. **Project Structure**: The categorized sign systems are organized into directories with `readme.md` files containing definitions.
6. **Zip Archive**: The project structure is zipped into `Sign_Systems_Project.zip`.

## Usage

1. Place the keyword or phrase in `input.txt`.
2. Run the script.
3. The results will be printed to the console and saved in `output.txt`.
4. The project structure will be created and zipped.

## Requirements

- Python 3
- `openai` package
- GPT-4 API key

## Detailed Descriptions

Each sign system and subcategory is provided with a detailed definition to help understand the context and relevance of the categorization. For example:

- **DNA**: The molecule that carries genetic information in all living organisms and many viruses.
- **RNA**: A molecule involved in decoding, regulation, and expression of genes.
- **Protein Synthesis**: The process by which cells build proteins, involving transcription and translation.

## Note

Ensure you have the `openai` package installed and a valid API key set in the script.

