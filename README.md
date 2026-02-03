# 🖊️ Signature Verification System using CNN & Autoencoder

A deep learning-based signature verification system that combines Convolutional Neural Networks (CNN) with Autoencoders to classify signatures as genuine or forged.

## 🌟 Features

- **Hybrid Architecture**: Combines CNN and Autoencoder for robust feature learning
- **Web Interface**: User-friendly Flask web application for signature verification
- **Real-time Predictions**: Upload and verify signatures instantly
- **Dataset Management**: Automatic dataset organization and model retraining
- **Multiple Models**: Support for different pre-trained models
- **Interactive Jupyter Notebook**: Complete training pipeline and experimentation

## 🏗️ Architecture

The system uses a hybrid approach:

1. **Encoder**: Extracts meaningful features from signature images
2. **Decoder**: Reconstructs images for unsupervised learning  
3. **Classifier**: Uses encoded features for genuine/forged classification

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- TensorFlow 2.13.0
- Flask 2.3.3

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/K-ARIVAZHAGAN/-SIGNATURE_VERIFICATION_USING_AUTOENCODER-CNN.git
   cd -SIGNATURE_VERIFICATION_USING_AUTOENCODER-CNN
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
├── app.py                              # Flask web application
├── Signature_verification_system.ipynb # Training notebook
├── requirements.txt                    # Python dependencies
├── models/                             # Trained model files
│   ├── model.h5                       # Main CNN model
│   ├── autoencoder.h5                 # Autoencoder model
│   ├── model_latest.h5               # Latest trained model
│   └── ...
├── data/                              # Dataset directory
│   ├── genuine_signatures/           # Genuine signature samples
│   ├── forged_signatures/            # Forged signature samples
│   ├── Sigcomp 2009 train/          # SIGCOMP 2009 dataset
│   └── user_contributed/            # User uploaded signatures
├── templates/                        # HTML templates
│   ├── index.html                   # Main interface
│   ├── result.html                  # Prediction results
│   └── upload.html                  # Upload interface
├── static/                          # CSS and static files
├── uploads/                         # Temporary upload directory
└── logs/                           # Application logs
    ├── predictions_log.json        # Prediction history
    ├── dataset_log.json           # Dataset changes
    └── retraining_log.json        # Retraining history
```

## 🔧 Usage

### Web Interface

1. **Verify Signature**: Upload a signature image to check if it's genuine or forged
2. **Add Genuine Signature**: Contribute genuine signatures to improve the model
3. **Add Forged Signature**: Contribute forged signatures for better training
4. **View Results**: Get detailed prediction results with confidence scores

### Jupyter Notebook

Open `Signature_verification_system.ipynb` to:
- Train new models
- Experiment with different architectures
- Analyze model performance
- Visualize results

## 📊 Dataset

The system uses multiple datasets:

- **SIGCOMP 2009**: Standard signature verification competition dataset
- **Custom Dataset**: Collected genuine and forged signatures
- **User Contributions**: Signatures uploaded through the web interface

### Supported Image Formats
- PNG, JPG, JPEG
- Recommended size: 224x224 pixels
- Grayscale or RGB

## 🤖 Model Details

### CNN Architecture
- Convolutional layers for feature extraction
- Batch normalization and dropout for regularization
- Global average pooling
- Dense classification layers

### Autoencoder Architecture
- Encoder: Compresses input to latent representation
- Decoder: Reconstructs original image
- Bottleneck layer: Forces learning of essential features

### Training Parameters
- Optimizer: Adam
- Loss: Binary crossentropy (classification) + MSE (reconstruction)
- Metrics: Accuracy, Precision, Recall
- Batch Size: 32
- Epochs: 100+

## 📈 Performance

The model achieves:
- **Accuracy**: ~95%+ on test data
- **Precision**: High precision for genuine signatures
- **Recall**: Balanced recall for both classes
- **F1-Score**: Optimized for practical deployment

## 🔄 Auto-Retraining

The system includes automatic retraining capabilities:
- Monitors new data additions
- Triggers retraining when sufficient new samples are available
- Saves model versions with timestamps
- Logs all training activities
- WE ARE WORKING ON THAT MODULE THERE IS SEVERAL BUGS TO DEBUG ! BUT OTHER THINGS WORKS WELL! THANKYOU!

## 🌐 API Endpoints

- `GET /`: Main interface
- `POST /predict`: Signature verification
- `POST /add_genuine`: Add genuine signature
- `POST /add_forged`: Add forged signature
- `GET /retrain`: Trigger model retraining

## 🛠️ Development

### Adding New Features

1. **Custom Preprocessing**: Modify image preprocessing in `app.py`
2. **Model Architecture**: Experiment in the Jupyter notebook
3. **UI Improvements**: Update templates in `templates/`
4. **API Extensions**: Add new endpoints in `app.py`

### Training New Models

1. Open `Signature_verification_system.ipynb`
2. Prepare your dataset in the `data/` directory
3. Run the training cells
4. Save the model to `models/`

## 📋 Requirements

- Flask==2.3.3
- tensorflow==2.13.0
- Pillow==10.0.0
- numpy==1.24.3
- matplotlib==3.7.2
- scikit-learn==1.3.0
- pandas==2.0.3
- jupyter==1.0.0
- ipykernel==6.25.0

## 🚀 Deployment

### Local Deployment
```bash
python app.py
```

### Docker Deployment
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Cloud Deployment
- Deploy to Heroku, AWS, or Google Cloud
- Configure environment variables
- Set up model storage (S3, GCS)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**K. ARIVAZHAGAN**
- GitHub: [@K-ARIVAZHAGAN](https://github.com/K-ARIVAZHAGAN)
- Project: [Signature Verification System](https://github.com/K-ARIVAZHAGAN/-SIGNATURE_VERIFICATION_USING_AUTOENCODER-CNN)

## 🙏 Acknowledgments

- SIGCOMP 2009 competition for the signature dataset
- TensorFlow and Keras communities
- Flask framework for web interface
- Contributors and testers

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/K-ARIVAZHAGAN/-SIGNATURE_VERIFICATION_USING_AUTOENCODER-CNN/issues) page
2. Create a new issue with detailed description
3. Include error logs and system information

## 🔮 Future Enhancements

- [ ] Real-time signature capture
- [ ] Mobile app integration
- [ ] Advanced augmentation techniques
- [ ] Multi-language support
- [ ] Blockchain-based verification
- [ ] API rate limiting and authentication
- [ ] Advanced analytics dashboard

---

⭐ If you find this project useful, please give it a star!
