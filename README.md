# Gisting for Software Engineering Tasks

This repository is focused on experimenting with prompt compression techniques for software engineering tasks, based on the "Gist Tokens" approach. The goal is to optimize prompt efficiency while maintaining or improving the quality of output in various code generation scenarios.

## Project Overview

This project aims to:
- Implement a gist token compression model to reduce the size of prompts for code generation tasks.
- Test and evaluate the performance of compressed prompts on benchmark datasets like MBPP (Multi-modal Benchmarks for Programming Proficiency) and HumanEval.

## Repository Structure

- `src/`: Contains the main source code, including the compression script and model configuration.
- `data/`: Includes datasets used for testing and benchmarking.
- `load_data.py`: Script for loading the dataset, running the compression model, and generating the CSV output.
- `output_compressed_with_passk.xlsx`: Contains results from compressing the first set of prompts, including performance metrics like `pass@1`, `pass@3`, and `pass@5`.

## Usage

### Running the Compression Script

To compress a set of prompts using the gist token model, you can run:

```bash
python -m src.compress --model_name_or_path /path/to/model --instruction "Your instruction here"
