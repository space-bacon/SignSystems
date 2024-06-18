# Sign Systems Categorization Project

## Overview

This project categorizes a given keyword, phrase, or PDF into various sign systems and subcategories to analyze the influence of each sign system. Additionally, it deconstructs the input into a signifier chain. The project uses both simple string matching and GPT-4 to provide an in-depth analysis and detailed descriptions.

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

### Additional Sign Systems
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

1. **Input**: The input keyword, phrase, or PDF is read from `input.txt` or `input.pdf`.
2. **Categorization**: The keyword is categorized using:
   - Simple string matching
   - GPT-4 API
3. **Combination**: The results from both methods are combined and normalized.
4. **Output**: An overview, detailed descriptions, and a signifier chain are generated and saved to `output.txt`.

## Calculation of Weights

The weights for each sign system are calculated using the following steps:

1. **Simple String Matching**: The input is analyzed for the presence of specific terms related to each sign system. The occurrences of these terms contribute to an initial weight for each category.
2. **GPT-4 Analysis**: The input is processed by GPT-4, which provides a categorization and assigns preliminary weights based on its understanding of the input's context and relevance to each sign system.
3. **Combination of Results**: The weights from simple string matching and GPT-4 analysis are combined. The total weight for each sign system is the sum of its initial weight from string matching and its weight assigned by GPT-4.
4. **Normalization**: The combined weights are normalized to ensure they sum to 100%, providing a proportional representation of the influence of each sign system.

This dual approach ensures both a heuristic and an AI-driven analysis of the input, providing a comprehensive and balanced categorization.

## Usage

1. Place the keyword or phrase in `input.txt` or use `input.pdf` for multimodal categorization.
2. Run the script.
3. The results will be printed to the console and saved in `output.txt`.

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



