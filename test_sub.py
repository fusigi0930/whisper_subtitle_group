import subtitle

def main():
    st = subtitle.Subtitle()
    st.set_lang("jp")
    st.process("百姓01.mp4")
    st.store_to_srt()
    st.close()

if __name__ == "__main__":
    main()