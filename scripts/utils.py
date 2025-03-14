import numpy as np
from datasets import load_from_disk, DatasetDict
from transformers import (
    Wav2Vec2CTCTokenizer,
    Wav2Vec2FeatureExtractor,
    Wav2Vec2Processor,
)

def compute_metrics(pred, processor, wer):
    """Compute Word Error Rate (WER) metric."""
    
    pred_logits = pred.predictions
    pred_ids = np.argmax(pred_logits, axis=-1)

    pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id

    pred_str = processor.batch_decode(pred_ids)
    # We do not want to group tokens when computing the metrics
    label_str = processor.batch_decode(pred.label_ids, group_tokens=False)

    wer_score = wer(hypothesis=pred_str, reference=label_str)

    return {"wer": wer_score}

def setup_processor(model_name, vocab_path="./data/vocab.json"):
    """Set up the processor with tokenizer and feature extractor."""
    # Initialize tokenizer
    tokenizer = Wav2Vec2CTCTokenizer(
        vocab_path, 
        unk_token="[UNK]", 
        pad_token="[PAD]", 
        word_delimiter_token="|"
    )
    
    # Initialize feature extractor
    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
    
    # Combine into processor
    processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
    
    return processor, feature_extractor.sampling_rate

def load_data(data_path, split = 'All', sample_size=None):
    """Load and prepare the Basque Common Voice dataset."""
    # Load the dataset
    if split == 'All':
        data = load_from_disk(data_path)
        
    
    elif split == 'test':
        data = load_from_disk(data_path, split='test')
        data = data['test']

    if sample_size != None:
        data = data.select(range(sample_size))

    print(data)
    return data
