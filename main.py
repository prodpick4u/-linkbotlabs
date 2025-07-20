
from utils.blog_generator import generate_blog_post
from utils.video_generator import create_video
from utils.youtube_upload import upload_video

def main():
    blog, products = generate_blog_post("electric toothbrushes")
    video_path = create_video(products, voice="female")
    upload_video(video_path, blog["title"], blog["description"])

if __name__ == "__main__":
    main()
