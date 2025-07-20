import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from blog_generator import generate_blog_post

if __name__ == "__main__":
    generate_blog_post()