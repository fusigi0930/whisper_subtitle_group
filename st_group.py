import subtitle
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--voice", help = "set voice languge", default="jp")
    parser.add_argument("-l", "--lang", help = "set output srt file langue", default="zh")
    parser.add_argument("-f", "--file", help = "file")
    args = parser.parse_args()

    st = subtitle.Subtitle()
    st.set_lang(args.voice)
    if args.file.split(".")[-1] == "srt":
        st.store_to_srt_from_srt(args.file, args.lang)
    else:
        st.process(args.file)
        st.store_to_srt()
        st.store_to_srt(args.lang)

    st.close()

if __name__ == "__main__":
    main()