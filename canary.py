# === Load models ===
modelcanary = ASRModel.from_pretrained(model_name="nvidia/canary-1b-v2")
modelcanary.eval()
modelcanary.to("cuda")

#model.to(torch.float32)
#model.change_attention_model("rel_pos_local_attn", [256,256])
#model.change_subsampling_conv_chunking_factor(1)  
modelcanary.to(torch.bfloat16)

# Transcribe
def def_canary(filename, modelcanary, src_lang, tgt_lang):
    try:

        # Transcribe
        start = time.time()        
        results = modelcanary.transcribe([filename], timestamps=True, source_lang=src_lang, target_lang=tgt_lang)

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

        print({"status": "success", "task": "transcribe-c", "time": round(time.time() - start, 2)})
        print("\n")
        return words, round(time.time() - start, 2)

    except Exception as e:
        print({"status": "error", "task": "transcribe-c", "error": str(e)})
        return [{"error": str(e)}], 0

