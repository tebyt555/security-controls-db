import os
import json
import frontmatter

def compile_database():
    db = []
    # Walk through the controls directory
    for root, dirs, files in os.walk('controls'):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                
                # Parse the file
                post = frontmatter.load(filepath)
                
                # Merge frontmatter and markdown body into one dictionary
                control_data = post.metadata
                control_data['guidance_markdown'] = post.content
                
                db.append(control_data)
                
    # Create output directory if it doesn't exist
    os.makedirs('dist', exist_ok=True)
    
    # Write the compiled JSON
    output_path = 'dist/controls-db.json'
    with open(output_path, 'w') as f:
        json.dump(db, f, indent=2)
        
    print(f"✅ Successfully compiled {len(db)} controls to {output_path}")

if __name__ == "__main__":
    compile_database()