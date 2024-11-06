# CapibaraENT CLI

![Capibara SSBD Model](./capibara_model/src/public/3BSSBD.webp)

CapibaraENT is a command-line tool for training, evaluating, and deploying Capibara-based language models, optimized for TPUs and featuring hyperparameter optimization.

## Features

- Training and evaluation of Capibara models
- Built-in TPU support
- Hyperparameter optimization
- Model deployment
- Performance measurement
- Docker container execution (optional)
- Integration with Weights & Biases for experiment tracking
- **New layers and sub-models**: Support for the latest modeling layers and advanced sub-models.

## Requirements

- Python 3.7+
- JAX (for TPU optimization)
- TensorFlow
- Weights & Biases
- Docker (optional, for container execution)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/anachroni-io/capibaraent-cli.git
   cd capibaraent-cli
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Weights & Biases:

   ```bash
   wandb login
   ```

## Usage

The CapibaraENT CLI offers various options for working with Capibara models:

```bash
python capibaraent_cli.py [options]
```

### Available options

- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--train`: Train the model
- `--evaluate`: Evaluate the model
- `--optimize`: Perform hyperparameter optimization
- `--use-docker`: Run the model inside Docker (optional, commented)
- `--deploy`: Deploy the model
- `--measure-performance`: Measure the model's performance
- `--model`: Path to the model YAML file (for deserialization)
- `--new-layer`: (optional) Activate new modeling layers
- `--sub-model`: (optional) Specify sub-models to use

### Usage Examples

1. Train a model:

   ```bash
   python capibaraent_cli.py --train
   ```

2. Evaluate a model:

   ```bash
   python capibaraent_cli.py --evaluate
   ```

3. Perform hyperparameter optimization:

   ```bash
   python optimize_hyperparameters.py
   ```

4. Deploy a model:

   ```bash
   python capibaraent_cli.py --deploy
   ```

5. Measure model performance:

   ```bash
   python capibaraent_cli.py --measure-performance
   ```

6. Run a model in Docker (optional, if Docker is set up):

   ```bash
   python capibaraent_cli.py --use-docker
   ```

## Configuration

Model configuration is handled through environment variables and YAML files. Key configuration parameters include:

- `CAPIBARA_LEARNING_RATE`
- `CAPIBARA_BATCH_SIZE`
- `CAPIBARA_MAX_LENGTH`
- `CAPIBARA_USE_TPU`
- `WANDB_PROJECT`
- `WANDB_ENTITY`
- `CAPIBARA_NEW_LAYER` (new layer)
- `CAPIBARA_SUB_MODEL` (sub-model)

### Example `.env` file

```env
CAPIBARA_LEARNING_RATE=0.001
CAPIBARA_BATCH_SIZE=32
CAPIBARA_MAX_LENGTH=512
CAPIBARA_USE_TPU=True
WANDB_PROJECT=my_project
WANDB_ENTITY=my_entity
CAPIBARA_NEW_LAYER=True
CAPIBARA_SUB_MODEL=my_sub_model
```

For a full list of configuration options, refer to the `.env.example` file.

## Hyperparameter Optimization

To perform hyperparameter optimization:

1. Ensure your Weights & Biases project is set up.
2. Run the optimization script:

   ```bash
   python optimize_hyperparameters.py
   ```

3. View the results in your Weights & Biases dashboard.

## Development

To contribute to the project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Marco Durán - <marco@anachroni.co>

Project Link: [https://github.com/anachroni-io/capibaraent-cli](https://github.com/anachroni-io/capibaraent-cli)
