import subtitle
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--voice", help = "set voice languge", default="jp")
    parser.add_argument("-l", "--lang", help = "set output srt file langue", default="zh")
    parser.add_argument("-f", "--file", help = "video file")
    args = parser.parse_args()

    st = subtitle.Subtitle()
    st.set_lang(args.voice)
    st.process(args.file)
    st.store_to_srt()
    st.store_to_srt(args.lange)
    st.close()

if __name__ == "__main__":
    main()