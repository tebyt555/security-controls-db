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
        
    # Write a _headers file for Cloudflare/Netlify/Vercel compatibility if ever migrated,
    # though GitHub Pages handles CORS permissively for raw static files by default.
    # We also add an index.html so the root URL doesn't throw a 404.
    with open('dist/index.html', 'w') as f:
        f.write("<html><body><h1>Security Controls API</h1><p>Query <a href='./controls-db.json'>/controls-db.json</a></p></body></html>")
        
    print(f"✅ Successfully compiled {len(db)} controls to {output_path}")

if __name__ == "__main__":
    compile_database()