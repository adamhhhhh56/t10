# === Load models ===
modelparakeet = ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v2")
modelparakeet.eval()

# 1) Optimize
modelparakeet.to("cuda")
modelparakeet.to(torch.float32)
if 500 > 480 : 
    try:
        print("Applying long audio settings: Local Attention and Chunking.")
        modelparakeet.change_attention_model("rel_pos_local_attn", [256,256])
        modelparakeet.change_subsampling_conv_chunking_factor(1)  
        long_audio_settings_applied = True
    except Exception as setting_e:
        print(f"Warning: Failed to apply long audio settings: {setting_e}")
        
modelparakeet.to(torch.bfloat16)

# Configure decoder for word-level timestamps
decoding_cfg = copy.deepcopy(modelparakeet.cfg.decoding)
with open_dict(decoding_cfg):
    decoding_cfg.compute_timestamps = True
    decoding_cfg.rnnt_timestamp_type = "word"
modelparakeet.change_decoding_strategy(decoding_cfg)

# Transcribe
def def_parakeet(filename, modelparakeet):
    try:
        
        # Transcribe
        start = time.time()
        results = modelparakeet.transcribe([filename], timestamps=True)

        # Collection and output of results
        words = []
        if isinstance(results, list) and results:
            hyp = results[0]
            if "word" in hyp.timestamp:
                for w in hyp.timestamp["word"]:
                    words.append({
                        "word":  w["word"],
                        "start": w["start"],
                        "end":   w["end"]
                    })

        print({"status": "success", "task": "transcribe-p", "time": round(time.time() - start, 2)})
        print("\n")
        return words, round(time.time() - start, 2)

    except Exception as e:
        print({"status": "error", "task": "transcribe-p", "error": str(e)})
        print("\n")
        return [{"error": str(e)}], 0

