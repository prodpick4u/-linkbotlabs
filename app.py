from flask import Flask, request, render_template_string
import os
import subprocess
import tempfile
import shutil

app = Flask(__name__)

# Simple home page with a basic form (optional, since you already have a form on your demo.html)
@app.route('/')
def home():
    return '''
    <h2>Prodpick4u One-Time Demo Backend</h2>
    <p>POST your keys to /run to start automation.</p>
    '''

@app.route('/run', methods=['POST'])
def run_demo():
    # Read keys from form POST data
    rapidapi_key = request.form.get('rapidapi_key')
    apify_token = request.form.get('apify_token')
    youtube_key = request.form.get('youtube_key')
    affiliate_tag = request.form.get('affiliate_tag')

    # Validate keys
    if not all([rapidapi_key, apify_token, youtube_key, affiliate_tag]):
        return "❌ Missing one or more API keys or affiliate tag. Please fill all fields.", 400

    # Create a temporary working directory for this run
    temp_dir = tempfile.mkdtemp()

    try:
        # Copy your automation files to temp_dir or mount your code there in Replit

        # Set environment variables for subprocess
        env = os.environ.copy()
        env['RAPIDAPI_KEY'] = rapidapi_key
        env['APIFY_TOKEN'] = apify_token
        env['YOUTUBE_API_KEY'] = youtube_key
        env['AFFILIATE_TAG'] = affiliate_tag

        # Run your main.py script from temp_dir or current dir
        # Adjust the command if your script requires arguments or specific paths
        result = subprocess.run(
            ['python3', 'main.py'],
            cwd='.',  # or temp_dir if you copy files there
            env=env,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes max
        )

        if result.returncode != 0:
            return f"❌ Automation failed:<br><pre>{result.stderr}</pre>", 500

        # On success, you can read generated files (e.g. blog posts) and return a success message
        # Example: read a generated blog HTML file (adjust path accordingly)
        output_preview = ""
        try:
            with open('docs/post-beauty.html', 'r', encoding='utf-8') as f:
                output_preview = f.read()
        except Exception as e:
            output_preview = "Could not load generated output preview."

        return render_template_string('''
            <h2>✅ Automation Completed Successfully!</h2>
            <p>Your blog post and video scripts have been generated.</p>
            <p><a href="/download/demo.zip">Download full output ZIP (coming soon)</a></p>
            <hr>
            <h3>Sample Generated Blog Post Preview:</h3>
            <div style="border:1px solid #ccc; padding:10px; max-height:400px; overflow:auto;">
              {{ output_preview | safe }}
            </div>
        ''', output_preview=output_preview)

    except subprocess.TimeoutExpired:
        return "❌ Automation timed out after 5 minutes.", 500
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
