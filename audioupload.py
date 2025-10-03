# Upload an audio file from a URL and save it locally
def def_audioupload(idn, file):

    # Create target folder if it doesn't exist
    folder = os.path.join("_temp", idn)
    os.makedirs(folder, exist_ok=True)  

    # Full path for the downloaded file
    filepath = os.path.join(folder, f"{idn}.wav")
    
    # Start timer
    start = time.time()
    result = {"status": "error", "task": "download", "time": 0}
    
    try:
        # Download the file from the given URL
        wget.download(file, filepath)
        result["status"] = "success"
    except Exception as e:
        # If download fails, keep status as error
        result["status"] = "error"
        result["error"] = str(e)
    finally:
        # Record total time taken
        result["time"] = round(time.time() - start, 2)
    
    # Print JSON result
    print("\n" + json.dumps(result, ensure_ascii=False))


# Cut an audio file into chunks with optional overlap
def def_audiocut(idn, file, length, chunk, lengthback, name):

    # Create output folder if it doesn't exist
    out_dir = f"_temp/{idn}"
    os.makedirs(out_dir, exist_ok=True)
    
    # Load the audio file
    audio = AudioSegment.from_file(file)
    
    # Calculate step size between segments (chunk length minus overlap)
    step = chunk - lengthback
    start = 0
    part = 1

    # Initialize result dictionary for JSON output
    result = {"status": "success", "task": f"cut-{name}", "time": 0}
    segments = {"segments": []}  # Stores info about each cut segment
    start_time = time.time()

    try:
        # Loop through audio and create segments
        while start < length:
            end = start + chunk
            if end > length:
                end = length
            segment = audio[start*1000:end*1000]  # Convert seconds to milliseconds
            out_path = f"{out_dir}/{idn}--{name}-{part}.wav"
            segment.export(out_path, format="wav")  # Save segment as WAV

            # Save segment info
            segments["segments"].append({"file": out_path, "start": start, "end": end})

            # Move to next segment
            start += step
            part += 1
    except Exception as e:
        # Catch any errors during cutting
        result["status"] = "error"
        result["error"] = str(e)
    finally:
        # Record total time taken
        result["time"] = round(time.time() - start_time, 2)

        # Print JSON result of the operation
        print(json.dumps(result, ensure_ascii=False))

        # Return info about all segments
        return segments
