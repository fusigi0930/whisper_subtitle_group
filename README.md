# whisper_subtitle_group
the subtitle group by using whisper

# initial environment

## Linux

```shell
# python 3.9
sudo apt install python3.9
sudo apt install python3-testresources ffmpeg
sudo apt install libpython3.9-dev portaudio19-dev pavucontrol espeak libmpv-dev git git-lfs
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools
git lfs install

# in whisper_tutor
python -m venv env
source env/bin/activate
pip install -r requirements_linux.txt
```

# run
the command that create the subtitle file (.srt) from the video file

```shell
python st_group.py --voice jp --lang zh --file <file>
```