from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='video_images_creator',
    version='0.4.64',
    description= "Create videos from images using the 'video_images_creator' package.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Nikhil Sharma',
    author_email='nikhilsharma972@gmail.com',
    license='BSD 2-clause',
    packages=['video_images_creator'],
    package_dir={"": "src"},
    package_data={"video_images_creator": ["*.ttf", "video-music.wav", "instantvideoaudio.wav", "audionew.wav", "thanks.wav", "background_music.wav", "intro_outro_v6.mp4", '*.jpg', '*.jpeg', '*.png', 'third_anim_assets', 'third_anim_assets/*.png', 'transition_assets', 'transition_assets/*.png', 'intro_outro_assets', 'intro_outro_assets/*.png', 'intro_outro_assets/*.txt']},
    install_requires=['opencv-python', 'numpy', 'pillow', 'azure-cognitiveservices-speech==1.37.0','pydub','requests'],
    classifiers=[
        'Development Status :: 1 - Planning',
    ],
)


