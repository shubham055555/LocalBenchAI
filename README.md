# LocalBench AI

LocalBench AI is a local Large Language Model (LLM) benchmarking system designed to evaluate and compare locally running AI models on real hardware.

It measures model performance across:

- Answer quality
- Inference latency
- Token throughput
- RAM usage
- VRAM usage
- Overall performance

The project is designed for resource-constrained systems where running large cloud-based models may not always be practical.

---

## Project Overview

LocalBench AI provides an automated benchmarking pipeline for locally running LLMs using **Ollama**.

The system sends the same benchmark questions to multiple local models, records hardware and inference metrics, evaluates generated answers, and produces a final weighted scorecard.

The project also includes an interactive **Streamlit** dashboard for visualizing benchmark results.

---

## Core Pipeline

```text
                    Benchmark Dataset
                           |
                           v
                    Ollama Runtime
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        Qwen3 1.7B      Phi-3        Llama 3
             |             |             |
             +-------------+-------------+
                           |
                           v
                    Benchmark Runner
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          Latency      Tokens/sec     Memory
                                        |
                                  +-----+-----+
                                  |           |
                                  v           v
                                 RAM         VRAM
                                  |
                                  v
                         Quality Evaluator
                                  |
                                  v
                          Final Scorecard
                                  |
                                  v
                       Streamlit Dashboard
```

---

## Architecture

The system consists of several major components.

### 1. Benchmark Dataset
The benchmark contains 40 AI and machine learning questions. All models receive the same questions to maintain a consistent comparison.

### 2. Ollama Runtime
Ollama provides the local inference runtime used to execute the selected language models.

### 3. Local Models
The benchmark currently evaluates:
- Qwen3 1.7B
- Phi-3
- Llama 3

### 4. Benchmark Runner
The benchmark runner executes the same questions against each configured model and records:
- Response latency
- Generated tokens
- Token throughput
- RAM usage
- VRAM usage
- Request status

### 5. Quality Evaluator
Generated answers are evaluated against expected concepts defined in the evaluation rubric.

### 6. Final Scorecard
Performance and quality metrics are normalized and combined using weighted scoring.

### 7. Streamlit Dashboard
The dashboard provides an interactive interface for exploring model performance and benchmark results.

---

## Features

### Automated Benchmarking
Run the same benchmark dataset against multiple locally running LLMs.

```text
40 Questions
     x
3 Models
     =
120 Requests
```

### Multi-Model Comparison
Compare multiple local models using the same questions, metrics, and scoring methodology.

### Quality Evaluation
Evaluate generated answers against expected concepts.

### Performance Measurement
Measure:
- Latency
- Generated tokens
- Tokens per second
- RAM usage
- VRAM usage

### Weighted Scoring
Combine quality, speed, and resource efficiency into a single overall score.

### Visualization
Generate charts for:
- Quality
- Throughput
- Latency
- VRAM
- Overall score

### Interactive Dashboard
Explore benchmark results using a Streamlit dashboard.

---

## Benchmark Dataset

The final benchmark contains:

- **40 Questions**
- **3 Models**
- **120 Total Requests**

The benchmark covers AI and machine learning concepts including:

- ML Fundamentals
- Supervised Learning
- Model Generalization
- Unsupervised Learning
- Optimization
- Neural Networks
- Evaluation Metrics
- Data
- Deep Learning
- AI Concepts

---

## Models Tested

The benchmark currently evaluates three locally running models through Ollama.

| Model | Purpose |
|---|---|
| Qwen3 1.7B | Efficient local inference |
| Phi-3 | Compact local model comparison |
| Llama 3 | Larger model quality comparison |

---

## Metrics

### Quality
Each generated answer is evaluated against expected concepts. The evaluator produces a quality score on a 0–5 scale, which is converted into a percentage for final comparison.

### Latency
Measures the time required to generate a response. Lower latency is better.

```text
Latency = Response completion time
```

### Token Throughput
Measures generated tokens per second. Higher throughput is better.

```text
Tokens/sec = Generated Tokens / Generation Time
```

### RAM Usage
System RAM usage is recorded before and after model inference.

### VRAM Usage
GPU memory usage is recorded during inference. Lower VRAM usage is considered more resource efficient.

---

## Weighted Scoring

The final score combines three major dimensions:

| Dimension | Weight |
|---|---|
| Quality | 50% |
| Speed | 30% |
| Resource Efficiency | 20% |

The final score is calculated as:

```text
Final Score =
    Quality × 0.50
  + Speed × 0.30
  + Resource Efficiency × 0.20
```

All components are normalized to a 0–100 scale.

---

## Final Benchmark Results

The final benchmark consisted of:

```text
40 Questions
     x
3 Models
     =
120 Inference Requests
```

All 120 requests completed successfully.

### Final Scorecard

| Rank | Model | Quality | Tokens/sec | Avg Latency | VRAM | Overall |
|---|---|---|---|---|---|---|
| 1 | Qwen3 1.7B | 93.8% | 86.01 | 16.13s | 2231 MB | 96.92 |
| 2 | Phi-3 | 85.7% | 16.44 | 20.15s | 2822 MB | 49.60 |
| 3 | Llama 3 | 90.8% | 6.39 | 70.26s | 2855 MB | 47.65 |

### Benchmark Winners

| Category | Winner | Result |
|---|---|---|
| Best Overall | Qwen3 1.7B | 96.92 / 100 |
| Best Quality | Qwen3 1.7B | 93.8% |
| Best Token Throughput | Qwen3 1.7B | 86.01 tokens/sec |
| Best Latency | Qwen3 1.7B | 16.13 seconds |
| Best VRAM Efficiency | Qwen3 1.7B | 2231 MB |

---

## Key Findings

The benchmark demonstrates significant differences between local LLMs when running on resource-constrained hardware.

- **Qwen3 1.7B** achieved the highest measured quality score of 93.8%, while also achieving the highest token throughput and lowest average latency among the tested models.
- **Llama 3** achieved a strong quality score of 90.8%, but its average throughput was substantially lower at 6.39 tokens/sec and its average latency was 70.26 seconds.
- **Phi-3** achieved 85.7% quality with 16.44 tokens/sec average throughput and 20.15 seconds average latency.

Under the scoring methodology used by LocalBench AI, Qwen3 1.7B achieved the highest overall score.

**Therefore, for the tested hardware and benchmark workload, Qwen3 1.7B provided the best measured quality-performance-resource trade-off among the evaluated models.**

---

## Hardware Context

The benchmark was performed on a system with:

- **GPU:** NVIDIA GeForce RTX 3050
- **VRAM:** 4 GB
- **System RAM:** approximately 16 GB

Local inference performance depends heavily on hardware and runtime configuration. Results may differ on other systems.

---

## Benchmark Methodology

Each model receives the same benchmark questions. For every request, LocalBench AI records performance information.

```text
Question
   |
   v
Local Model
   |
   +---- Response
   |
   +---- Latency
   |
   +---- Generated Tokens
   |
   +---- Tokens/sec
   |
   +---- RAM
   |
   +---- VRAM
   |
   v
Saved Benchmark Result
```

After the performance benchmark completes, generated answers are evaluated using the expected concept rubric. The quality scores are then combined with normalized performance metrics to generate the final scorecard.

---

## Generated Artifacts

### Raw Benchmark Results
`benchmark/results/benchmark_results.json`
Contains performance measurements for individual benchmark requests.

### Quality Results
`benchmark/results/quality_results.json`
Contains quality evaluation results for model answers.

### Final Scorecard
`benchmark/results/final_scorecard.json`
Contains normalized metrics, weighted scores, rankings, and benchmark winners.

### Benchmark Charts
Generated charts are stored in:
`benchmark/results/charts/`

Available charts:
- Quality comparison
- Throughput comparison
- Latency comparison
- VRAM comparison
- Overall score comparison

---

## Visualization

| Chart | Description |
|---|---|
| `charts/quality_comparison.png` | Quality Comparison |
| `charts/throughput_comparison.png` | Throughput Comparison |
| `charts/latency_comparison.png` | Latency Comparison |
| `charts/vram_comparison.png` | VRAM Comparison |
| `charts/overall_score.png` | Overall Score |

---

## Interactive Dashboard

LocalBench AI includes an interactive Streamlit dashboard.

The dashboard provides:

- Model rankings
- Quality comparison
- Token throughput comparison
- Latency comparison
- VRAM usage comparison
- Overall score comparison
- Benchmark statistics
- Scoring methodology

Start the dashboard with:

```bash
streamlit run dashboard.py
```

The dashboard reads the existing benchmark results and does not execute the benchmark again.

---

## Project Structure

```text
LocalBenchAI/
│
├── app.py
├── dashboard.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── docs/
│   └── architecture.png
│
└── benchmark/
    │
    ├── runner.py
    ├── evaluator.py
    ├── final_report.py
    ├── charts.py
    │
    ├── questions.json
    ├── evaluation_rubric.json
    │
    └── results/
        │
        ├── benchmark_results.json
        ├── quality_results.json
        ├── final_scorecard.json
        │
        └── charts/
            ├── quality_comparison.png
            ├── throughput_comparison.png
            ├── latency_comparison.png
            ├── vram_comparison.png
            └── overall_score.png
```

---

## Technology Stack

- Python
- Ollama
- Streamlit
- Pandas
- Matplotlib
- psutil
- JSON

---

## Requirements

- Python 3.11+
- Ollama
- Local LLM models
- NVIDIA GPU recommended for GPU acceleration
- Windows, Linux, or macOS

The benchmark can also be adapted for CPU-only systems.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shubham055555/LocalBenchAI.git
cd LocalBenchAI
```

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv .venv
```

Activate the environment:

```bash
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Ollama Setup

Make sure Ollama is installed and running.

Check the installation:

```bash
ollama --version
```

Check installed models:

```bash
ollama list
```

Example:

```text
qwen3:1.7b
phi3:latest
llama3:latest
```

Test a model:

```bash
ollama run qwen3:1.7b
```

---

## Usage

### Run the Local AI Application

```bash
python app.py
```

This starts the local AI application and allows interaction with a locally running model through Ollama.

### Run the Benchmark

```bash
python benchmark/runner.py
```

The benchmark runner evaluates the configured models using the benchmark dataset.

Results are saved to:
`benchmark/results/benchmark_results.json`

### Evaluate Answer Quality

After the benchmark completes:

```bash
python benchmark/evaluator.py
```

The evaluator uses:
`benchmark/evaluation_rubric.json`

Quality results are saved to:
`benchmark/results/quality_results.json`

### Generate Final Scorecard

```bash
python benchmark/final_report.py
```

Output:
`benchmark/results/final_scorecard.json`

### Generate Charts

```bash
python benchmark/charts.py
```

Charts are generated in:
`benchmark/results/charts/`

### Start the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will be available at:
`http://localhost:8501`

Open the URL in your browser.

---

## Reproducibility

The benchmark pipeline is designed to make model comparisons repeatable. The same:

- Questions
- Models
- Evaluation rubric
- Performance metrics
- Scoring methodology

can be reused for future experiments.

However, exact results may vary depending on:

- Hardware
- Background processes
- Model version
- Model quantization
- Ollama version
- GPU memory availability
- CPU load
- System RAM availability

---

## Limitations

### Dataset Size
The benchmark contains 40 questions. A larger and more diverse dataset would provide stronger statistical confidence.

### Quality Evaluation
The current quality evaluator uses expected concepts. This provides a lightweight automated evaluation mechanism but does not completely replace expert human evaluation or a stronger LLM-as-a-Judge system.

### Hardware Dependence
Performance depends heavily on the hardware and software environment. Therefore, the numerical rankings should not be interpreted as universal rankings of the models.

### Resource Measurements
RAM and VRAM values are system-level observations during inference and should not be interpreted as exact model memory footprints.

---

## Future Improvements

- Larger benchmark datasets
- LLM-as-a-Judge evaluation
- Human evaluation
- Streaming latency measurement
- Cold-start vs warm-start benchmarking
- CPU vs GPU comparison
- Multiple quantization comparisons
- Power consumption measurement
- More local models
- Statistical confidence intervals
- Experiment history tracking
- Automatic benchmark reports
- Web-based model comparison
- Model recommendation system

---

## Why LocalBench AI?

Cloud-based AI APIs are convenient, but local inference introduces different engineering constraints.

A model that performs well in the cloud may not be the best choice for a local machine with limited:

- GPU memory
- System memory
- Compute capacity
- Power budget

LocalBench AI focuses on answering a practical question:

> Which local LLM provides the best balance between quality, speed, and hardware resource usage on a given machine?

---

## Engineering Insight

The benchmark demonstrates that model selection is not simply about choosing the model with the highest raw quality.

A useful local model must also consider:

```text
Quality
+
Latency
+
Throughput
+
Memory Usage
```

For the tested environment, Qwen3 1.7B achieved the strongest overall balance according to the defined scoring methodology.

---

## Project Status

- [x] Local Ollama integration
- [x] Multiple local model support
- [x] Automated benchmark runner
- [x] 40-question benchmark
- [x] 120 inference requests
- [x] Latency measurement
- [x] Token throughput measurement
- [x] RAM measurement
- [x] VRAM measurement
- [x] Automated quality evaluation
- [x] Weighted model scoring
- [x] Final scorecard
- [x] Benchmark charts
- [x] Interactive Streamlit dashboard
- [x] Architecture documentation
- [x] GitHub-ready README

---

## License

MIT License

## Author

Shubham

Built as a local AI/ML engineering project focused on practical LLM benchmarking, hardware-aware evaluation, and local model selection.
