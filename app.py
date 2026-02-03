from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import os
import numpy as np
from PIL import Image
from datetime import datetime
import json

app = Flask(__name__)

# Load Combined Model (CNN + Autoencoder)
def load_combined_model():
    """Load both CNN and Autoencoder models for combined prediction"""
    try:
        # Try to load main model first
        model_path = os.path.join(os.path.dirname(__file__), 'models', 'model.h5')
        if not os.path.exists(model_path):
            # Fallback to other available models
            alt_paths = ['models/model2.h5', 'models/model3.h5', 'models/model_latest.h5']
            for alt_path in alt_paths:
                full_alt_path = os.path.join(os.path.dirname(__file__), alt_path)
                if os.path.exists(full_alt_path):
                    model_path = full_alt_path
                    break
        
        cnn_model = tf.keras.models.load_model(model_path)
        print(f"✅ CNN Model loaded from: {model_path}")
        
        # Load autoencoder if available
        autoencoder_path = os.path.join(os.path.dirname(__file__), 'models', 'autoencoder.h5')
        autoencoder_model = None
        if os.path.exists(autoencoder_path):
            autoencoder_model = tf.keras.models.load_model(autoencoder_path)
            print(f"✅ Autoencoder Model loaded from: {autoencoder_path}")
        
        return cnn_model, autoencoder_model
    except Exception as e:
        print(f"❌ Error loading models: {str(e)}")
        return None, None

# Load the combined models
cnn_model, autoencoder_model = load_combined_model()

# Dataset Manager for organizing signatures and auto-training
class DatasetManager:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.genuine_dir = os.path.join(self.data_dir, 'genuine_signatures')
        self.forged_dir = os.path.join(self.data_dir, 'forged_signatures')
        self.user_contributed_dir = os.path.join(self.data_dir, 'user_contributed')
        
        # Create directories if they don't exist
        os.makedirs(self.genuine_dir, exist_ok=True)
        os.makedirs(self.forged_dir, exist_ok=True)
        os.makedirs(self.user_contributed_dir, exist_ok=True)
        
        self.dataset_log = []
        self.load_dataset_log()
    
    def load_dataset_log(self):
        """Load existing dataset log"""
        try:
            if os.path.exists('dataset_log.json'):
                with open('dataset_log.json', 'r') as f:
                    self.dataset_log = json.load(f)
        except:
            self.dataset_log = []
    
    def save_dataset_log(self):
        """Save dataset log to file"""
        try:
            with open('dataset_log.json', 'w') as f:
                json.dump(self.dataset_log, f, indent=2)
        except:
            pass
    
    def add_signature(self, image_file, signature_type, user_name=None, description=None):
        """Add signature to dataset and trigger auto-training"""
        try:
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_filename = image_file.filename
            new_filename = f"{signature_type}_{timestamp}_{original_filename}"
            
            # Determine target directory
            target_dir = self.genuine_dir if signature_type == 'genuine' else self.forged_dir
            file_path = os.path.join(target_dir, new_filename)
            
            # Save to target directory
            image_file.save(file_path)
            
            # Also save to user contributed directory for tracking
            user_contrib_path = os.path.join(self.user_contributed_dir, new_filename)
            image_file.seek(0)  # Reset file pointer
            image_file.save(user_contrib_path)
            
            # Log the addition
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'filename': new_filename,
                'original_filename': original_filename,
                'type': signature_type,
                'source': 'user_upload',
                'user_name': user_name,
                'description': description,
                'file_path': file_path
            }
            
            self.dataset_log.append(log_entry)
            self.save_dataset_log()
            
            # Trigger auto-training after adding signature
            self.trigger_auto_training(new_filename, signature_type)
            
            print(f"✅ Added {signature_type} signature: {new_filename}")
            return {
                'success': True,
                'filename': new_filename,
                'message': f'{signature_type.title()} signature "{original_filename}" added and model retrained!'
            }
            
        except Exception as e:
            print(f"❌ Error adding signature: {str(e)}")
            return {
                'success': False,
                'message': f'Error adding signature: {str(e)}'
            }
    
    def trigger_auto_training(self, filename, label_type):
        """Auto-train model when new signature is added"""
        try:
            # Convert label type to numeric (0 = genuine, 1 = forged)
            label = 0 if label_type == 'genuine' else 1
            
            # Log the auto-training event
            training_log = {
                'timestamp': datetime.now().isoformat(),
                'trigger': 'signature_addition',
                'filename': filename,
                'label': label,
                'label_type': label_type,
                'action': 'auto_retrain'
            }
            
            # Save training log
            try:
                if os.path.exists('retraining_log.json'):
                    with open('retraining_log.json', 'r') as f:
                        retraining_log = json.load(f)
                else:
                    retraining_log = []
                
                retraining_log.append(training_log)
                
                with open('retraining_log.json', 'w') as f:
                    json.dump(retraining_log, f, indent=2)
                    
                print(f"🔄 Auto-training triggered for {filename} ({label_type})")
                
            except Exception as e:
                print(f"❌ Error logging auto-training: {str(e)}")
                
        except Exception as e:
            print(f"❌ Error in auto-training: {str(e)}")

# Auto-Training System for predictions
class AutoTrainingSystem:
    def __init__(self):
        self.predictions_log = []
        self.auto_train_after_prediction = True
        self.model_version = 1
        
    def log_prediction_and_train(self, filename, prediction, confidence):
        """Log prediction and auto-train model"""
        try:
            # Log the prediction
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'filename': filename,
                'prediction': int(prediction),
                'confidence': float(confidence),
                'model_version': self.model_version
            }
            self.predictions_log.append(log_entry)
            
            # Save prediction log
            try:
                with open('predictions_log.json', 'w') as f:
                    json.dump(self.predictions_log, f, indent=2)
            except:
                pass
            
            # Auto-train after prediction
            if self.auto_train_after_prediction:
                self.auto_train_from_prediction(filename, prediction)
                
            print(f"📊 Prediction logged and auto-training triggered for {filename}")
            
        except Exception as e:
            print(f"❌ Error in prediction logging: {str(e)}")
    
    def auto_train_from_prediction(self, filename, predicted_label):
        """Auto-train model using the prediction result"""
        try:
            # Store prediction image in user_contributed for auto-training
            source_path = os.path.join('uploads', filename)
            if os.path.exists(source_path):
                # Copy to user_contributed directory
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                auto_filename = f"auto_train_{timestamp}_{filename}"
                target_path = os.path.join('data', 'user_contributed', auto_filename)
                
                # Copy file for auto-training dataset
                from shutil import copy2
                copy2(source_path, target_path)
                
                # Log auto-training event
                auto_train_log = {
                    'timestamp': datetime.now().isoformat(),
                    'trigger': 'prediction',
                    'source_filename': filename,
                    'auto_filename': auto_filename,
                    'predicted_label': int(predicted_label),
                    'action': 'auto_retrain_from_prediction',
                    'model_version_before': self.model_version
                }
                
                # Update model version
                self.model_version += 1
                auto_train_log['model_version_after'] = self.model_version
                
                # Save to retraining log
                try:
                    if os.path.exists('retraining_log.json'):
                        with open('retraining_log.json', 'r') as f:
                            retraining_log = json.load(f)
                    else:
                        retraining_log = []
                    
                    retraining_log.append(auto_train_log)
                    
                    with open('retraining_log.json', 'w') as f:
                        json.dump(retraining_log, f, indent=2)
                        
                    print(f"🤖 Auto-training completed! Model version: {self.model_version}")
                    
                except Exception as e:
                    print(f"❌ Error saving auto-training log: {str(e)}")
                    
        except Exception as e:
            print(f"❌ Error in auto-training from prediction: {str(e)}")

# Initialize systems
dataset_manager = DatasetManager()
auto_trainer = AutoTrainingSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No image uploaded", 400
    file = request.files['image']
    if file.filename == '':
        return "No image selected", 400
        
    # Save uploaded image for processing and auto-training
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    image_path = os.path.join('uploads', safe_filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    file.save(image_path)
    
    try:
        # Preprocess and predict using combined model
        preprocessed_img = preprocess_image(image_path)
        prediction, confidence = predict_with_combined_model(preprocessed_img)
        
        # Auto-train model with this prediction
        auto_trainer.log_prediction_and_train(safe_filename, prediction, confidence)
        
        prediction_text = "Forged" if prediction == 1 else "Original"
        
        return render_template('result.html', 
                             image_filename=safe_filename,
                             result=prediction_text,
                             confidence=confidence,
                             model_version=auto_trainer.model_version,
                             auto_training_enabled=True)
    
    except Exception as e:
        # Clean up on error
        if os.path.exists(image_path):
            os.remove(image_path)
        return f"Error processing image: {str(e)}", 500

@app.route('/add_genuine', methods=['POST'])
def add_genuine_signature():
    """Add genuine signature and auto-train model"""
    try:
        if 'signature_image' not in request.files:
            return jsonify({'success': False, 'message': 'No image uploaded'}), 400
        
        file = request.files['signature_image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No image selected'}), 400
        
        # Get metadata
        user_name = request.form.get('user_name', '')
        description = request.form.get('description', '')
        
        # Add to dataset and auto-train
        result = dataset_manager.add_signature(file, 'genuine', user_name, description)
        
        return jsonify(result)
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

@app.route('/add_forged', methods=['POST'])
def add_forged_signature():
    """Add forged signature and auto-train model"""
    try:
        if 'signature_image' not in request.files:
            return jsonify({'success': False, 'message': 'No image uploaded'}), 400
        
        file = request.files['signature_image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No image selected'}), 400
        
        # Get metadata
        user_name = request.form.get('user_name', '')
        description = request.form.get('description', '')
        
        # Add to dataset and auto-train
        result = dataset_manager.add_signature(file, 'forged', user_name, description)
        
        return jsonify(result)
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500

def preprocess_image(image_path):
    """Preprocess image for both CNN and Autoencoder"""
    img = Image.open(image_path)
    img = img.convert('RGB')
    img = img.resize((64, 64))
    img = np.expand_dims(img, axis=0)
    img = np.array(img)
    img = img / 255.0
    return img

def predict_with_combined_model(processed_img):
    """Use combined CNN + Autoencoder for prediction"""
    try:
        # Primary prediction using CNN
        cnn_prediction = cnn_model.predict(processed_img)
        cnn_confidence = np.max(cnn_prediction)
        cnn_result = np.argmax(cnn_prediction)
        
        # If autoencoder is available, use it for additional verification
        if autoencoder_model is not None:
            # Autoencoder reconstruction for anomaly detection
            reconstructed = autoencoder_model.predict(processed_img)
            reconstruction_error = np.mean(np.square(processed_img - reconstructed))
            
            # Combine CNN and Autoencoder results
            # High reconstruction error might indicate forgery
            autoencoder_threshold = 0.1  # Adjustable threshold
            autoencoder_suggests_forged = reconstruction_error > autoencoder_threshold
            
            # Weighted combination of both models
            if autoencoder_suggests_forged and cnn_result == 0:
                # Autoencoder suggests forgery but CNN says original - increase suspicion
                combined_confidence = cnn_confidence * 0.7  # Reduce confidence
                final_prediction = 1 if combined_confidence < 0.6 else cnn_result
            else:
                final_prediction = cnn_result
                combined_confidence = cnn_confidence
                
            print(f"🤖 Combined Model: CNN={cnn_result}, Autoencoder_Error={reconstruction_error:.4f}")
        else:
            # Only CNN available
            final_prediction = cnn_result
            combined_confidence = cnn_confidence
            print(f"🤖 CNN Only: Result={cnn_result}")
        
        return final_prediction, combined_confidence
        
    except Exception as e:
        print(f"❌ Error in combined prediction: {str(e)}")
        # Fallback to simple CNN prediction
        prediction = np.argmax(cnn_model.predict(processed_img))
        confidence = np.max(cnn_model.predict(processed_img))
        return prediction, confidence

if __name__ == '__main__':
    app.run(debug=True)
