import os
import json
import uuid

def main():
    print("Hello from mitm-amp!")
    print("=" * 50)
    
    # Handle thread_id cache
    cache_file = "thread_cache.json"
    
    if os.path.exists(cache_file):
        # Read existing thread_id from cache
        with open(cache_file, 'r') as f:
            data = json.load(f)
            thread_id = data.get('thread_id')
            print(f"Found existing thread_id: {thread_id}")
    else:
        # Generate new thread_id and save to cache
        thread_id = f"T-{str(uuid.uuid4())}"
        data = {'thread_id': thread_id}
        
        with open(cache_file, 'w') as f:
            json.dump(data, f)
            
        print(f"Generated new thread_id: {thread_id}")
    
    print("=" * 50)
    
    # Read and display comments
    if os.path.exists("comments.txt"):
        print("Reading PR comments:")
        with open("comments.txt", "r") as f:
            content = f.read()
            print(content)
    else:
        print("No comments.txt found")
        
    print("=" * 50)
    return thread_id


if __name__ == "__main__":
    main()
